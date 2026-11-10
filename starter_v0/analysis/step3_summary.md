# Step 3 — Kết quả v1, v2, v3

Step 3 yêu cầu ít nhất ba vòng sau baseline, mỗi vòng một giả thuyết, có run thật và version log. v1 đã chạy ở Step 2; lần làm Step 3 tiếp tục v2, đọc kết quả rồi mới thay đổi và chạy v3.

Provider/model của cả bốn run: **OpenRouter / `openai/gpt-4o-mini`**. Mỗi run đo đủ **20/20 case**, **0 lỗi provider**. Nội dung `eval_base.json`, `eval_group.json`, `eval_research_extension.json` giữ nguyên.

## Kết quả thực đo

| Version | Case accuracy | Tool routing | Argument accuracy | Multi-turn accuracy | Run |
|---|---:|---:|---:|---:|---|
| v0 | 65% (13/20) | 75% | 65% | 100% | [v0](../runs/v0_B_base_openrouter_20261110T173956757517.json) |
| v1 | 90% (18/20) | 100% | 90% | 100% | [v1](../runs/v1_B_base_openrouter_20261110T175728553731.json) |
| v2 | 95% (19/20) | 100% | 95% | 100% | [v2](../runs/v2_B_base_openrouter_20261110T180649154815.json) |
| v3 | 85% (17/20) | 95% | 85% | 83.33% | [v3](../runs/v3_B_base_openrouter_20261110T180928571868.json) |

Trong [version_log.csv](../artifacts/version_log.csv), `metric_before` và `metric_after` dùng `case_accuracy` dạng 0–1. Hash được lấy từ chính run JSON. Run v0 có sẵn từ trước; trường author của baseline để trống vì chưa có thông tin tác giả. Các thay đổi v1–v3 được ghi tác giả là Codex.

## Mỗi version kiểm chứng một giả thuyết

### v1 — Hỏi lại khi thiếu đầu vào

- Bằng chứng v0: R10 tự chọn tài khoản `sama`; R11 tự đặt URL mặc dù người dùng chưa cung cấp.
- Giả thuyết: thay chỉ dẫn đoán bằng quy tắc gọi `clarify(response_type="text")` sẽ tránh bịa tài khoản/URL, đồng thời giữ dữ liệu đã có trong hội thoại.
- Thay đổi: một đoạn trong `system_prompt.md`; khai báo tool giữ nguyên.
- Kết quả: cả R10 và R11 chuyển sang `clarify`; R10 pass. R11 vẫn fail vì lời gọi thiếu tham số `response_type`, dù implementation có default `text`. Tổng điểm 65% → 90%; cả 13 case từng pass ở v0 tiếp tục pass.
- Các case khác cũng thay đổi kết quả trong lần chạy này; cần các phép đo bổ sung để xác định độ ổn định và tác động riêng của quy tắc hỏi lại.

### v2 — Bắt buộc truyền `response_type`

- Bằng chứng v1: R11 có đúng tool `clarify` nhưng không truyền `response_type`; eval chấm arguments được model thực sự gửi.
- Giả thuyết: thêm `response_type` vào `required` của schema sẽ giúp model truyền rõ kiểu câu hỏi.
- Thay đổi duy nhất về nội dung: `clarify.parameters.required` từ `[question]` thành `[question, response_type]`. Prompt v1 giữ nguyên.
- Kết quả: R11 pass với `response_type="text"`; tổng điểm 90% → 95%; cả 18 case từng pass ở v1 tiếp tục pass. R12 còn fail vì dùng `text` thay vì `yes_no`.

### v3 — Xác nhận trước khi gửi

- Bằng chứng v2: R12 hỏi nội dung bản tin bằng `response_type="text"`; prompt vẫn có chỉ dẫn gửi ngay.
- Giả thuyết: thay đoạn gửi ngay bằng yêu cầu `clarify(response_type="yes_no")`, chờ xác nhận chính xác nội dung/đích gửi rồi mới `send(confirmed=true)`, sẽ sửa R12 và giữ hành vi các yêu cầu đọc.
- Thay đổi duy nhất về nội dung: một đoạn xác nhận hành động trong prompt. Schema v2 giữ nguyên.
- Kết quả: **giả thuyết chưa được ủng hộ trong lần đo này**; tổng điểm 95% → 85%. Giữ lại đầy đủ run này và ghi kết quả giảm vào version log.

| Case fail ở v3 | Tool/args thực tế | Điều eval yêu cầu | Nhận xét |
|---|---|---|---|
| R12_confirm_before_send | `clarify(response_type="text")`, hỏi nội dung và tên kênh | `clarify(response_type="yes_no")` | Lỗi vẫn còn từ v2. Case chưa cung cấp nội dung/đích gửi, nên cần review thủ công sự khác nhau giữa hỏi dữ liệu thiếu và xin xác nhận; base expect giữ nguyên. |
| R13_parallel_web_and_tweets | Gọi cả `lookup` và `social_search`, nhưng `lookup` thiếu `topic` | `lookup(topic="news", timeframe="day", query="AI")` và `social_search(query="AI")` | Lỗi phát sinh so với v2 là thiếu arg; nhãn failure type cố định của case là `wrong_tool`. |
| M02_carryover_timeframe | `social_search(query="robotics", search_type="Latest")` | `lookup(query="robotics", topic="news", timeframe="day")` | Lỗi phát sinh so với v2: đổi sai nguồn khi xử lý ngữ cảnh nhiều lượt. |

v2 là version có điểm cao nhất trong các lần đo hiện có. Artifact tại đường dẫn chính hiện là v3, tương ứng run v3; snapshot v2 được giữ riêng để so sánh và chạy lại. Kết quả chỉ phản ánh các lần đo đã lưu, cần đo lặp nếu muốn kết luận về độ ổn định.

## Snapshot và cách chạy lại

Prompt/tools theo từng version được giữ tại:

- [v0 prompt](../artifacts/versions/v0/system_prompt.md), [v0 tools](../artifacts/versions/v0/tools.yaml).
- [v1 prompt](../artifacts/versions/v1/system_prompt.md), [v1 tools](../artifacts/versions/v1/tools.yaml).
- [v2 prompt](../artifacts/versions/v2/system_prompt.md), [v2 tools](../artifacts/versions/v2/tools.yaml).
- [v3 prompt](../artifacts/versions/v3/system_prompt.md), [v3 tools](../artifacts/versions/v3/tools.yaml).

Các bản này được đối chiếu SHA-256 với run JSON tương ứng, bao gồm line endings. Snapshot v0 được khôi phục từ nội dung Git nguyên bản và kiểm tra hash trước khi lưu.

Ví dụ chạy lại v2 từ `starter_v0/`:

```powershell
python run_eval.py --provider openrouter --model openai/gpt-4o-mini --version v2 --suite base --eval-cases data/eval_base.json --system-prompt artifacts/versions/v2/system_prompt.md --tools artifacts/versions/v2/tools.yaml
```

Để chạy version khác, dùng đúng cả nhãn version và cặp snapshot của version đó. Chỉ đổi nhãn `--version` sẽ không tái tạo nội dung prompt/schema cũ.

## Kiểm tra và phạm vi bằng chứng

- Contract test sau sửa schema v2: **55 passed**.
- Toàn suite sau sửa prompt v3: **62 passed, 17 skipped, 0 failed**; xem [output pytest](step3_pytest.txt). Các test skip là stub CP3 có sẵn.
- [CSV phân tích v0–v3](step3_v0_v3.csv) chứa 80 dòng, tương ứng 4 run × 20 case.
- Bảng B1 trong [group report](../../report/team/group_report.md) được cập nhật từ các log thật.
- Base eval đo tool call và subset args; các case `no_tool` cần review thêm nội dung câu trả lời. Luồng gửi Telegram và xác nhận qua nhiều lượt cần transcript live để đánh giá tiếp.
- Các vòng tiếp theo có thể kiểm chứng riêng mô tả mode của `clarify`, quy ước `lookup` news/timeframe, routing theo nguồn và chỉ dẫn ép một bước còn lại trong starter.
