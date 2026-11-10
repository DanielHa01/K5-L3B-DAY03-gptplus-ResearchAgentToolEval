# Báo cáo cá nhân — Trịnh Minh Đức — 2A202604078

## 1. Thông tin thành viên

- Họ tên: **Trịnh Minh Đức**.
- MSSV: **2A202604078**.
- Email: 26ai.ductm3@vinuni.edu.vn
- Phạm vi phụ trách: **Step 1 đến Step 3 — baseline, phân tích lỗi, tối ưu prompt/tool declaration và ghi bằng chứng v0–v3**.

## 2. Phần việc phụ trách

Tôi phụ trách phần đo baseline và chuỗi thử nghiệm cải tiến hành vi gọi tool của research agent, với sự hỗ trợ của Codex/ChatGPT. Công việc tập trung vào:

- **Step 1:** sử dụng bộ base eval cố định để có số đo v0, kiểm tra tính hợp lệ của run và phân tích từng case fail.
- **Step 2:** từ lỗi thực tế, đặt một giả thuyết và thay đổi riêng một phần của prompt hoặc schema để kiểm chứng.
- **Step 3:** hoàn thành chuỗi v1, v2, v3; lưu run JSON, hash, giả thuyết, metric trước/sau và các bản input tương ứng.

Provider/model dùng trong bốn run base: **OpenRouter / `openai/gpt-4o-mini`**.

## 3. Đóng góp cụ thể

### 3.1. Step 1 — Baseline và phân tích lỗi

Baseline v0 sử dụng prompt/tool declaration nguyên bản của starter và bộ `data/eval_base.json`. Run có **20 case, đo đủ 20/20, 0 lỗi provider**, đạt **13/20 case — 65%**. Kết quả được ghi vào `artifacts/version_log.csv` để làm mốc so sánh.

Phân tích 7 case fail dựa trên `actual_tool_calls`, `failures` và `observed_mismatch`:

| Case | Loại lỗi phân tích | Hành vi thực tế / dấu hiệu nguyên nhân |
|---|---|---|
| R03_web_news_routing | `wrong_arg_value` | Gọi đúng `lookup` nhưng truyền `query="AI news"` thay vì `"AI"` theo expect. Cần làm rõ việc tách chủ đề tìm kiếm khỏi các tham số loại tin và thời gian. |
| R08_out_of_scope | `out_of_scope` | Gọi `send` cho yêu cầu giải tích phân, trong khi expect là không gọi tool. Starter chưa phân định phạm vi rõ và còn ép chọn tool. |
| R10_missing_handle | `missing_info` | Tự chọn tài khoản `sama` dù người dùng chưa nêu tài khoản. Prompt gốc trực tiếp khuyến khích đoán thông tin thiếu. |
| R11_missing_url | `missing_info` | Tự đặt URL `https://example.com/article` thay vì hỏi lại đường dẫn. |
| R12_confirm_before_send | `wrong_boundary` | Gọi `send` ngay thay vì hỏi xác nhận. Đây là lỗi lựa chọn hành động của model; lời gọi không chứng minh đã gửi Telegram thành công. |
| R13_parallel_web_and_tweets | `wrong_arg_value` | Đã gọi cả `lookup` và `social_search`, nhưng query của `lookup` không khớp expect và thiếu `topic="news"`. |
| R14_out_of_scope_coding | `out_of_scope` | Gọi `send` để trả nội dung code Fibonacci, trong khi expect là không gọi tool. |

R03 và R13 được dataset gắn `case_failure_type="wrong_tool"`, nhưng `observed_mismatch` của run là `wrong_arg_value`. Phần phân tích phân biệt nhãn thiết kế case với lỗi quan sát thực tế; nội dung case gốc được giữ nguyên.

### 3.2. Step 2 — Kiểm chứng giả thuyết hỏi lại khi thiếu dữ liệu

Giả thuyết đầu tiên: thay chỉ dẫn đoán tài khoản/URL bằng quy tắc gọi `clarify(response_type="text")` sẽ giúp agent hỏi lại khi thiếu đầu vào bắt buộc, đồng thời giữ thông tin đã có trong hội thoại.

Thay đổi được giới hạn ở một đoạn trong `artifacts/system_prompt.md`, tạo version **v1**. Kết quả thực đo:

- Cả R10 và R11 chuyển sang gọi `clarify`; R10 pass.
- R11 vẫn fail vì model bỏ qua tham số `response_type` trong lời gọi, dù hàm Python có giá trị mặc định `text`.
- Case accuracy tăng **65% → 90%**; cả 13 case từng pass ở v0 tiếp tục pass.

Các case khác cũng thay đổi kết quả trong lần chạy v1. Cần phép đo bổ sung để kết luận về độ ổn định và tác động riêng của quy tắc hỏi lại.

### 3.3. Step 3 — Hoàn thành chuỗi thử nghiệm v1–v3

| Version | Thay đổi riêng của vòng | Giả thuyết | Case accuracy trước → sau |
|---|---|---|---:|
| v1 | Thay đoạn đoán dữ liệu thiếu trong prompt | Buộc hỏi lại sẽ tránh tự đặt tài khoản/URL và giữ ngữ cảnh đa lượt | 65% → 90% |
| v2 | Thêm `response_type` vào `clarify.parameters.required` trong `tools.yaml` | Schema yêu cầu rõ tham số sẽ giảm việc model bỏ sót kiểu câu hỏi | 90% → 95% |
| v3 | Thay đoạn yêu cầu gửi ngay trong prompt | Yêu cầu hỏi xác nhận `yes_no` và chờ phê duyệt nội dung/đích gửi sẽ sửa lỗi boundary | 95% → 85% |

**v2:** R11 truyền rõ `response_type="text"` và pass; cả 18 case từng pass ở v1 tiếp tục pass. Đây là version có điểm cao nhất trong bốn lần đo.

**v3:** giả thuyết chưa được ủng hộ trong lần đo này. R12 vẫn hỏi dữ liệu thiếu bằng `text` thay vì `yes_no`; R13 thiếu `topic="news"`; M02 chọn `social_search` thay vì giữ `lookup` theo ngữ cảnh. Hai case cuối từng pass ở v2. Kết quả giảm được ghi nguyên vào version log.

| Version | Case pass | Case accuracy | Tool routing | Argument accuracy | Multi-turn accuracy | Run JSON |
|---|---:|---:|---:|---:|---:|---|
| v0 | 13/20 | 65% | 75% | 65% | 100% | [Run v0](../../starter_v0/runs/v0_B_base_openrouter_20261110T173956757517.json) |
| v1 | 18/20 | 90% | 100% | 90% | 100% | [Run v1](../../starter_v0/runs/v1_B_base_openrouter_20261110T175728553731.json) |
| v2 | 19/20 | 95% | 100% | 95% | 100% | [Run v2](../../starter_v0/runs/v2_B_base_openrouter_20261110T180649154815.json) |
| v3 | 17/20 | 85% | 95% | 85% | 83.33% | [Run v3](../../starter_v0/runs/v3_B_base_openrouter_20261110T180928571868.json) |

Cả bốn run đều có `provider_error_cases=0` và `measured_cases=total_cases=20`. Các cột metric trước/sau trong version log dùng `case_accuracy` dạng 0–1. Mỗi version có thay đổi hash đúng với artifact đã sửa và có snapshot input để đối chiếu.

## 4. Bằng chứng

### File và dữ liệu kiểm chứng

- [Version log v0–v3](../../starter_v0/artifacts/version_log.csv): artifact đã sửa, giả thuyết, hash prompt/tools, metric trước/sau và đường dẫn run.
- [System prompt](../../starter_v0/artifacts/system_prompt.md) và [tool declarations](../../starter_v0/artifacts/tools.yaml): các file cấu hình hành vi agent.
- Snapshot đúng nội dung dùng trong các run: [v0 prompt](../../starter_v0/artifacts/versions/v0/system_prompt.md), [v0 tools](../../starter_v0/artifacts/versions/v0/tools.yaml); [v1 prompt](../../starter_v0/artifacts/versions/v1/system_prompt.md), [v1 tools](../../starter_v0/artifacts/versions/v1/tools.yaml); [v2 prompt](../../starter_v0/artifacts/versions/v2/system_prompt.md), [v2 tools](../../starter_v0/artifacts/versions/v2/tools.yaml); [v3 prompt](../../starter_v0/artifacts/versions/v3/system_prompt.md), [v3 tools](../../starter_v0/artifacts/versions/v3/tools.yaml).
- [CSV phân tích 80 dòng](../../starter_v0/analysis/step3_v0_v3.csv): kết quả từng case của 4 run × 20 case.
- [Tổng kết Step 3](../../starter_v0/analysis/step3_summary.md) và [bảng B1 báo cáo nhóm](group_report.md): giải thích thay đổi và kết quả từng vòng.
- [Contract test](../../starter_v0/tests/test_tool_contract.py) và [output pytest tại thời điểm chốt Step 3](../../starter_v0/analysis/step3_pytest.txt): kiểm tra schema/registry/code và bằng chứng test lịch sử.

Các run và snapshot lịch sử là căn cứ cho số liệu Step 1–3; file cấu hình ở đường dẫn chính có thể được cập nhật tiếp trong các phần việc sau. Báo cáo sử dụng các file/run cụ thể làm bằng chứng, không nhận toàn bộ nội dung của một commit dùng chung là đóng góp cá nhân.

### AI/công cụ đã dùng và cách kiểm tra

- **Codex/ChatGPT:** hỗ trợ đọc yêu cầu, phân tích run JSON, đề xuất giả thuyết, sửa prompt/schema, thực thi lệnh eval/test và tổng hợp tài liệu. Cột `author` của các vòng v1–v3 trong version log ghi `Codex`; sự hỗ trợ này được công khai trong báo cáo.
- **Python và OpenRouter:** chạy bộ base eval bằng API thật, ghi kết quả từng case cùng tool call/tool result.
- **Git:** đối chiếu thay đổi giữa các bản và lưu nội dung để truy vết. Không sửa lịch sử commit để thay bằng chứng.
- **pytest:** kiểm tra contract sau thay đổi schema. Tại thời điểm Step 3, contract suite có 55 test pass; toàn suite có 62 pass, 17 skip và 0 fail. Đây là số liệu lịch sử của Step 3; các stub CP3 được xử lý ở phần việc tiếp theo.

Cách kiểm chứng đã áp dụng trong quá trình thực hiện với AI hỗ trợ:

1. Đọc số liệu trực tiếp từ `summary` và lỗi từ `results[*].result`, rồi đối chiếu với CSV/bảng kết quả.
2. Chỉ dùng run đo đủ case, không có lỗi provider; giữ cùng provider/model và bộ base để so sánh.
3. Đối chiếu SHA-256 của snapshot với `prompt_hash`/`tools_hash` trong run JSON và version log.
4. Kiểm tra khác biệt từng vòng: v1 thay một đoạn prompt; v2 thay một danh sách `required`; v3 thay một đoạn xác nhận gửi.
5. Đọc cả tool call và args để nhận diện lỗi; với các case không gọi tool hoặc xác nhận hành động, cần review thêm nội dung trả lời và hội thoại live.

## 5. Tự đánh giá

Đánh giá trong mục này dựa trên kết quả và artifact đã có:

- **Phần đã có bằng chứng:** baseline v0 hợp lệ, phân tích 7 case fail, chuỗi v1–v3 với mỗi vòng một giả thuyết, version log, run JSON và snapshot tương ứng.
- **Kết quả đạt được:** v2 đạt 95%, cao hơn baseline 30 điểm phần trăm trong các lần đo hiện có. Việc bắt buộc `response_type` đã sửa được lỗi bỏ sót tham số ở R11 trong lần chạy v2.
- **Hạn chế:** v3 giảm xuống 85%, lỗi xác nhận R12 chưa được giải quyết trong base eval và xuất hiện hai lỗi ở các yêu cầu đọc. Một lần đo trên 20 case chưa đủ để kết luận về độ ổn định trên các yêu cầu khác.

