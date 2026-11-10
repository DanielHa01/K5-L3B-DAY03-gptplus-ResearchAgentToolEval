# Báo cáo nhóm — Day 03 Research Agent Tool Eval

> Báo cáo gồm 2 phần có hạn khác nhau:
> - **Phần A (mục 2)** — giới thiệu agent, ngắn gọn 1 trang. **Xong trước Team showdown (16:30)** để team khác hiểu nhanh agent có tool gì, làm được gì. Có thể làm thêm poster `report/team/poster.html` hoặc `poster.svg`.
> - **Phần B (mục 3–7)** — chi tiết và bằng chứng, dựa trên log thật. Hoàn thiện trước deadline nộp bài.
>
> Mỗi bảng phải trỏ được tới file thật: run JSON, transcript, commit. Cách chấm xem [RUBRIC.md](../../RUBRIC.md).

## 1. Thông tin nhóm

- Tên nhóm: **gptplus**
- Thành viên và phân công: xem [TEAM.md](../../TEAM.md)
- Provider/model dùng cho v0–v3: OpenRouter / `openai/gpt-4o-mini`.

## 2. Mục tiêu và cách tiếp cận — PHẦN A: Giới thiệu agent

### A1. Agent này làm được gì

Agent hỗ trợ nghiên cứu bằng cách tìm tin trên web và mạng xã hội, tra cứu bài báo arXiv/chính sách nội bộ, đọc URL và trình bày kết quả thành digest. Tool `verify` đối chiếu trích dẫn đã được đọc để làm nổi bật bằng chứng mâu thuẫn; gửi Telegram chỉ được thực hiện sau bước xác nhận.

**Cách chạy UI:**

Chạy từ thư mục `starter_v0/`: `streamlit run app.py`. Dependency `streamlit` đã có trong `starter_v0/requirements.txt`.

**Link dùng thử (deploy):**

Theo báo cáo cá nhân của Nguyễn Ngọc Bách, giao diện đã được triển khai bằng Cloudflare và có thử chat với hội thoại thật. Tuy nhiên, repo hiện chưa có URL deploy/tunnel hoặc transcript live để người đọc kiểm chứng; cần bổ sung các bằng chứng này nếu có.

### A2. Tool agent có

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|---|
| `clarify` | Hỏi người dùng khi thiếu dữ liệu hoặc cần xác nhận | Không |
| `timeline` | Lấy bài đăng gần đây của một tài khoản X | Không |
| `social_search` | Tìm bài đăng trên X theo từ khóa, sắp xếp Latest hoặc Top | Không |
| `lookup` | Tìm kiếm web, gồm cả tin tức theo khoảng thời gian | Không |
| `fetch` | Đọc nội dung từ URL được cung cấp | Không |
| `format` | Định dạng các kết quả đã thu thập thành digest | Không |
| `policy` | Tìm trong tài liệu chính sách nội bộ | Không |
| `papers` | Tìm bài báo trên arXiv | Không |
| `paper_text` | Trích xuất nội dung text từ bài báo arXiv | Không |
| `send` | Gửi nội dung lên Telegram sau khi được xác nhận | Không |
| `verify` | So sánh các trích dẫn và nhãn bằng chứng đã cung cấp, báo trạng thái mâu thuẫn/củng cố/chưa đủ | **Có** |

### A3. Câu hỏi mẫu để thử

1. “Tìm tin tức trên web trong tháng này về EU AI Act.”
2. “Tìm 4 tweet được tương tác nhiều nhất về open-source LLM.”
3. “Tìm paper arXiv gần đây về retrieval-augmented generation, tối đa 3 kết quả.”
4. “Đọc và tóm tắt trang này: https://www.theverge.com/ai-artificial-intelligence”
5. “Kiểm tra nhận định mình đưa ra bằng các nguồn độc lập; trích dẫn bằng chứng và cho biết các nguồn ủng hộ, phản bác hay chưa đủ kết luận.”

## 3. Giải pháp

- **v1 — Hỏi lại khi thiếu dữ liệu:** thay riêng đoạn prompt yêu cầu đoán tài khoản/URL bằng quy tắc gọi `clarify(response_type="text")`, chờ người dùng bổ sung và giữ ngữ cảnh các lượt trước.
- **v2 — Truyền rõ kiểu câu hỏi:** thêm `response_type` vào danh sách `required` của schema `clarify`. Implementation của tool và nội dung eval giữ nguyên.
- **v3 — Xác nhận trước khi gửi:** thay riêng đoạn prompt yêu cầu gửi ngay bằng quy tắc hỏi `clarify(response_type="yes_no")`, chờ xác nhận nội dung/đích gửi và chỉ gọi `send(confirmed=true)` khi đủ điều kiện. Lần đo v3 giảm điểm; kết quả và lỗi phát sinh được ghi ở B1.
- **Tool mới — `verify`:** chỉ dùng sau khi đã thu thập và đọc nguồn bằng `lookup`/`fetch`, để so sánh các trích dẫn cùng stance đã đánh giá; không tự tìm kiếm hoặc tự xác minh nội dung trích dẫn.

## 4. Kết quả — PHẦN B: Chi tiết và bằng chứng

### B1. Version Evidence

Lấy từ `starter_v0/artifacts/version_log.csv` và `starter_v0/runs/*.json`. Chỉ dùng run có `provider_error_cases == 0` và `measured_cases == total_cases`.

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| v0 | baseline | Đo starter nguyên bản trước khi sửa | — | 65% | [Run v0](../../starter_v0/runs/v0_B_base_openrouter_20261110T173956757517.json) |
| v1 | `system_prompt.md` | Yêu cầu hỏi lại khi thiếu đầu vào sẽ tránh đoán tài khoản/URL, giữ ngữ cảnh đa lượt | 65% | 90% | [Run v1](../../starter_v0/runs/v1_B_base_openrouter_20261110T175728553731.json) |
| v2 | `tools.yaml` | Bắt buộc `response_type` trong schema sẽ tránh model bỏ sót kiểu câu hỏi | 90% | 95% | [Run v2](../../starter_v0/runs/v2_B_base_openrouter_20261110T180649154815.json) |
| v3 | `system_prompt.md` | Quy tắc hỏi xác nhận `yes_no` trước khi gửi sẽ sửa R12 và giữ hành vi các yêu cầu đọc | 95% | 85% | [Run v3](../../starter_v0/runs/v3_B_base_openrouter_20261110T180928571868.json) |

Metric trước/sau trong bảng và `version_log.csv` là `summary.case_accuracy`. Cả 4 run đều đo đủ 20/20 case, `provider_error_cases=0`, cùng provider/model; các input/expect của bộ base không thay đổi.

| Version | Case accuracy | Tool routing | Argument accuracy | Multi-turn accuracy |
|---|---:|---:|---:|---:|
| v0 | 65% | 75% | 65% | 100% |
| v1 | 90% | 100% | 90% | 100% |
| v2 | 95% | 100% | 95% | 100% |
| v3 | 85% | 95% | 85% | 83.33% |

- **v2:** R11 đã truyền `response_type="text"`; cả 18 case từng pass ở v1 đều tiếp tục pass.
- **v3:** giả thuyết chưa được ủng hộ trong lần đo này. R12 vẫn hỏi bổ sung nội dung/đích gửi bằng `text`; R13 thiếu `topic="news"`; M02 chuyển sang `social_search` thay vì `lookup`. Hai case cuối từng pass ở v2.
- **Phạm vi kết luận:** v2 có điểm cao nhất trong các lần đo hiện có. Kết quả base đo routing/args; luồng xác nhận và gửi thật cần transcript live để đánh giá tiếp.

Hash và đường dẫn run: [version log](../../starter_v0/artifacts/version_log.csv). Bản prompt/tools cố định của từng version, cách chạy lại và phân tích chi tiết: [tổng kết Step 3](../../starter_v0/analysis/step3_summary.md). Bảng phân tích có 80 dòng: [CSV v0–v3](../../starter_v0/analysis/step3_v0_v3.csv). Unit test sau thay đổi: **62 passed, 17 skipped, 0 failed**; 17 skip là stub CP3 có sẵn, xem [output pytest](../../starter_v0/analysis/step3_pytest.txt).

### B2. Failure Analysis

Lấy từ `results[*].result.failures` trong run JSON.

| Case ID | Failure Type | Actual Tool Calls | What Failed | Fix |
|---|---|---|---|---|
| `R03_web_news_routing` | `wrong_tool` | `lookup(query="AI news", topic="news", timeframe="day")` | Dùng đúng tool nhưng sai query argument; case được gán `wrong_tool` trong bộ eval. | Giữ query theo chủ đề người dùng nêu; dùng `topic="news"` để biểu thị loại tìm kiếm. |
| `R08_out_of_scope` | `out_of_scope` | `send(text="Nguyên hàm của x^2 là ...")` | Gọi tool gửi thay vì trả lời phép tính trực tiếp; không có yêu cầu gửi. | Chỉ dùng `send` khi người dùng yêu cầu gửi; câu hỏi ngoài khả năng tool thì trả lời trực tiếp nếu có thể. |
| `R10_missing_handle` | `missing_info` | `timeline(screenname="sama")` | Tự đoán tài khoản khi người dùng chưa nêu tên. | Gọi `clarify(response_type="text")` để hỏi tài khoản. |
| `R11_missing_url` | `missing_info` | `fetch(url="https://example.com/article")` | Bịa URL cho cụm “bài viết này”. | Hỏi người dùng cung cấp URL trước khi gọi `fetch`. |
| `R12_confirm_before_send` | `wrong_boundary` | `send(text="Bản tin này")` | Gửi khi chưa có xác nhận; thiếu cả nội dung/đích gửi cụ thể. | Hỏi thông tin còn thiếu, sau đó yêu cầu xác nhận rõ nội dung và đích gửi; chỉ gọi `send(confirmed=true)` sau khi được đồng ý. |
| `R13_parallel_web_and_tweets` | `wrong_tool` | `lookup(query="AI news", timeframe="day")`; `social_search(query="AI")` | Gọi cả hai tool đúng nhưng lookup thiếu `topic="news"` và query không khớp; case được gán `wrong_tool` trong bộ eval. | Khai báo rõ convention cho lookup tin tức và cho phép gọi cả hai nguồn khi được yêu cầu. |
| `R14_out_of_scope_coding` | `out_of_scope` | `send(text="Dưới đây là một hàm Python...")` | Dùng tool gửi để trả lời yêu cầu viết code; người dùng không yêu cầu đăng/gửi. | Trả lời trực tiếp, không gọi tool action cho yêu cầu ngoài phạm vi research. |

### B3. Team Eval Cases

Run group đo 10 case: 5 single-turn và 5 multi-turn.

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
| `G01_arxiv_research_routing` | Tìm paper arXiv, giới hạn 3 | `papers(max_results=3)` | Pass |
| `G02_internal_policy_routing` | Câu hỏi chính sách dữ liệu cá nhân | `policy(policy_area="data_privacy")` | Pass |
| `G03_social_top_posts` | Tweet tương tác cao, limit 4 | `social_search(search_type="Top", limit=4)` | Pass |
| `G04_missing_social_subject` | Thiếu tài khoản X | `clarify(response_type="text")` | Pass |
| `G05_no_unrequested_send` | Chỉ soạn nội dung để người dùng đọc | Không gọi tool | **Fail** — gọi `lookup(query="AI", topic="news", timeframe="day")` dù không được yêu cầu tìm tin |
| `G06_multiturn_account_correction` | Sửa tài khoản OpenAI thành Anthropic, giữ limit 8 | `timeline(screenname="AnthropicAI", limit=8)` | **Fail** — dùng `screenname="Anthropic"` |
| `G07_multiturn_clarify_then_fetch` | Nhận URL ở lượt sau rồi đọc đúng URL | `fetch(url="https://www.theverge.com/ai-artificial-intelligence")` | Pass |
| `G08_multiturn_source_switch_to_news` | Đổi từ social sang tin web, tháng này | `lookup(topic="news", timeframe="month", query="EU AI Act")` | Pass |
| `G09_multiturn_send_requires_confirmation` | Nội dung/đích gửi chưa phải là xác nhận | `clarify(response_type="yes_no")` | Pass |
| `G10_multiturn_paper_search_to_text` | Dùng paper ID từ ngữ cảnh và giới hạn trang | `paper_text(arxiv_url="2303.06374", max_pages=4)` | Pass |

Run group có 10/10 case được đo, 0 lỗi provider; case accuracy **80%**, tool routing **90%**, argument accuracy **80%**, multi-turn accuracy **80%**. Bằng chứng: [run group](../../starter_v0/runs/v3_B_group_openrouter_20261110T182504634362.json). Bộ case có 10 mục đúng (5 single-turn, 5 multi-turn), nhưng hiện **không có case nào kiểm tra route tới tool mới `verify`**.

### B4. Live Chat Evidence

Lấy từ `starter_v0/transcripts/*.transcript.json`.

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
| — | Chưa có transcript live JSON trong `starter_v0/transcripts/`. | — | Chưa có | Chưa có bằng chứng về chat live. **Cần cung cấp transcript nếu nhóm đã chạy chat ở nơi khác.** |

### B5a. Required Evidence — Tool mới, unit test, UI

| Item | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Tool mới (`tools/verify/`) | [`tool.py`](../../starter_v0/tools/verify/tool.py), [`TOOL.md`](../../starter_v0/tools/verify/TOOL.md), đăng ký trong [`tools/__init__.py`](../../starter_v0/tools/__init__.py) và [`tools.yaml`](../../starter_v0/artifacts/tools.yaml) | So sánh các stance do agent cung cấp; phân biệt conflicting, corroborated, contradicted và insufficient evidence. | Tool không tự tìm nguồn hoặc xác minh trích dẫn; cần đọc nguồn trước, trích dẫn chính xác và review độc lập tính liên quan/độ độc lập của publisher. Chưa có eval group case route tới verify. |
| Unit test tool mới (≥ 3 test/tool) | [`test_tools_todo.py`](../../starter_v0/tests/test_tools_todo.py), [`pytest output`](../../starter_v0/analysis/step3_pytest.txt) | Có 6 test function cho `verify` (13 trường hợp sau khi tính parameterization), bao gồm corroboration, conflicting evidence, cùng domain, input xấu và dữ liệu rỗng. Toàn suite ghi nhận 62 passed, 17 skipped, 0 failed. | Test `test_verify_bad_input_returns_error_dict` kiểm tra input sai trả error dict; đây là kiểm tra code của tool mà eval routing không đo. 17 skip là stub CP3 còn lại; test challenge 0 skipped chưa đạt. |
| UI (lệnh chạy + link dùng thử) | [`app.py`](../../starter_v0/app.py), [`requirements.txt`](../../starter_v0/requirements.txt) | Có Streamlit app; chạy `cd starter_v0; streamlit run app.py`. | Chưa có link deploy/tunnel trong repo; cần xác nhận app đã được deploy và cung cấp URL. |

Tool mới có 6 test function (13 trường hợp khi tính parameterization). Ví dụ: `test_verify_bad_input_returns_error_dict` bắt input sai và yêu cầu trả error dict thay vì raise; eval routing không kiểm tra nhánh xử lý lỗi nội bộ này.

### B5. Bonus Evidence

Chỉ điền nếu nhóm làm bonus (ghi riêng, tối đa 10 điểm). Tool có sẵn (`send`, `policy`, `papers`, `paper_text`) không tự được bonus.

| Bonus | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Small Local Model | Chưa thực hiện | — | Không có kết quả model local để so sánh. |
| Hơn 3 tool mới (≥ 4) | Có một tool mới được nhận diện: `verify` | Chưa đạt ngưỡng 4 tool mới | `papers`, `paper_text`, `policy`, `send` là tool có sẵn trong starter. |
| `send` gửi thật lên Telegram sau xác nhận | Không tìm thấy transcript | Chưa có bằng chứng gửi thật | Cần transcript chứng minh có xác nhận trước khi gọi action. |
| Test challenge (0 skipped / regression test) | [`pytest output`](../../starter_v0/analysis/step3_pytest.txt) | Chưa thực hiện challenge | Suite có 17 skipped; chưa đạt tiêu chí 0 skipped và chưa có regression test được báo cáo. |

Nhóm xác nhận chưa làm bonus test challenge hoặc regression test. Toàn suite còn 17 test TODO bị skip.

### B7. Small Local Model Challenge (bonus)

Nhóm xác nhận **chưa thực hiện** Small Local Model Challenge; không có run Ollama/local để so sánh.

## 5. Khó khăn và cách xử lý

> Khó khăn chính và cách nhóm xử lý. Nếu gặp lỗi kỹ thuật (provider lỗi, hết quota API, tool không chạy), mô tả lỗi và dẫn bằng chứng: run JSON, log, ảnh chụp.

- Prompt ban đầu khuyến khích đoán tài khoản/URL và gọi `send` ngay; v0 vì vậy sai ở missing-info và action boundary (R10–R12). v1 thay chỉ dẫn đoán bằng `clarify`; v2 làm `response_type` thành trường bắt buộc.
- Kết quả không tăng đều: v2 đạt 95%, còn v3 giảm còn 85% và phát sinh lỗi R13, M02. Nhóm giữ lại run/version log để thấy giả thuyết v3 chưa được ủng hộ, thay vì chỉ báo cáo version có điểm cao nhất.
- Run group đạt 80%; lỗi còn lại là gọi tìm web ngoài yêu cầu ở G05 và ánh xạ handle chưa đúng ở G06. Cần bổ sung eval cho tool mới `verify` và kiểm tra câu hỏi không cần tool.

## 6. Tổng hợp đóng góp

| Thành viên | Phần việc và đóng góp | Bằng chứng |
|---|---|---|
| Trương Anh Đức (2A202604096) | Thu thập, đối chiếu báo cáo từng thành viên; tổng hợp tiến trình, kết quả, phân tích lỗi và bằng chứng để hoàn thiện báo cáo nhóm. | [Báo cáo cá nhân](2A202604096_TruongAnhDuc.md), báo cáo này và các báo cáo thành viên trong thư mục. |
| Nguyễn Ngọc Bách (2A202604108) | Step 5; tạo giao diện chat, báo cáo triển khai Cloudflare và thử nghiệm với hội thoại thật. | [Báo cáo cá nhân](2A202604108_NguyenNgocBach.md), commit `29dfde1c683eb15fdb7808efcb10cf1ed8995136`. Repo chưa có URL deploy hoặc transcript live để kiểm chứng. |
| Hà Phan Đại Dương (202604119) | Fork/setup môi trường; phát triển tool `verify` để đối chiếu nguồn và viết unit test cho các tool. | [Báo cáo cá nhân](202604119_HaPhanDaiDuong.md), commit `aa65a034922507f9ef4de6b731b31a74f189ec03`; code/test được dẫn tại B5a. |
| Trịnh Minh Đức (2A202604078) | Step 1–3: baseline, phân tích lỗi, thử nghiệm prompt/schema v0–v3 và lưu bằng chứng đo. | [Báo cáo cá nhân](2A202604078_TrinhMinhDuc.md), version log, run JSON, snapshot và CSV phân tích được dẫn tại B1. |

## 7. Hạn chế và hướng cải thiện — B6. Reflection

- `system_prompt.md`: v1 bỏ quy tắc đoán thông tin thiếu; v3 thêm bước hỏi xác nhận trước khi gửi. v3 giảm điểm, nên cần xem lại thứ tự hỏi dữ liệu còn thiếu và xác nhận, rồi đo lại.
- `tools.yaml`: v2 yêu cầu `clarify.response_type`, giúp R11 pass và nâng accuracy từ 90% lên 95%.
- Cần review thủ công: G05 vì yêu cầu “soạn để đọc” lại gọi lookup; R12 vì khác biệt giữa hỏi nội dung/đích gửi còn thiếu và xin xác nhận; tool `verify` vì source count theo hostname chỉ là đại diện gần đúng cho tính độc lập nguồn.
- Vòng tiếp theo: sửa một giả thuyết về routing “chỉ soạn, không tìm kiếm” để tránh lỗi G05, sau đó thêm eval riêng cho `verify`; đồng thời làm rõ ánh xạ tài khoản Anthropic → `AnthropicAI` cho G06. Đo từng thay đổi riêng để tránh gộp nguyên nhân.

## 8. Tài liệu tham khảo

- [README lab](../../README.md), [tool setup](../../docs/TOOL-SETUP.md), [version log](../../starter_v0/artifacts/version_log.csv)
- Run eval: [base v0–v3](../../starter_v0/runs/), [group v3](../../starter_v0/runs/v3_B_group_openrouter_20261110T182504634362.json)
- Tool mới: [verify TOOL.md](../../starter_v0/tools/verify/TOOL.md), [verify implementation](../../starter_v0/tools/verify/tool.py)
