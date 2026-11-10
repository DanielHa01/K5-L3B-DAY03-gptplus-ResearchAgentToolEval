# Báo cáo nhóm — Day 03 Research Agent Tool Eval

> Báo cáo gồm 2 phần có hạn khác nhau:
> - **Phần A (mục 2)** — giới thiệu agent, ngắn gọn 1 trang. **Xong trước Team showdown (16:30)** để team khác hiểu nhanh agent có tool gì, làm được gì. Có thể làm thêm poster `report/team/poster.html` hoặc `poster.svg`.
> - **Phần B (mục 3–7)** — chi tiết và bằng chứng, dựa trên log thật. Hoàn thiện trước deadline nộp bài.
>
> Mỗi bảng phải trỏ được tới file thật: run JSON, transcript, commit. Cách chấm xem [RUBRIC.md](../../RUBRIC.md).

## 1. Thông tin nhóm

- Tên nhóm:
- Thành viên và phân công: xem [TEAM.md](../../TEAM.md)
- Provider/model dùng cho v0–v3: OpenRouter / `openai/gpt-4o-mini`.

## 2. Mục tiêu và cách tiếp cận — PHẦN A: Giới thiệu agent

### A1. Agent này làm được gì

> 1–2 câu mô tả agent dùng để làm gì (cho team khác hiểu nhanh).

Ví dụ: "Research agent: tìm tin theo từ khóa / theo tài khoản, đọc URL, tổng hợp thành digest, và gửi lên Telegram khi được xác nhận."

**Cách chạy UI:**

> Lệnh chạy UI (ví dụ `streamlit run app.py`) và dependency đã thêm vào `starter_v0/requirements.txt`.

**Link dùng thử (deploy):**

> Dán link public để team khác mở thử ngay. Cách deploy nhanh bằng Cloudflare Tunnel xem README. Nếu deploy Vercel/Streamlit Cloud thì dán link đó.
>
> URL:

### A2. Tool agent có

> Liệt kê các tool agent đang dùng (gồm tool mới nhóm tự thêm). Mỗi tool 1 dòng: tên + làm được gì.

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|---|
| clarify | hỏi lại người dùng khi thiếu thông tin | không |
|  |  |  |
|  |  |  |

### A3. Câu hỏi mẫu để thử

> 3–5 câu hỏi/yêu cầu mẫu để team khác tự thử agent ngay.

1.
2.
3.

## 3. Giải pháp

> Tóm tắt các thay đổi chính trong `starter_v0/artifacts/system_prompt.md` và `starter_v0/artifacts/tools.yaml`, và tool mới nhóm viết (tên, làm gì, khi nào agent nên gọi).

- **v1 — Hỏi lại khi thiếu dữ liệu:** thay riêng đoạn prompt yêu cầu đoán tài khoản/URL bằng quy tắc gọi `clarify(response_type="text")`, chờ người dùng bổ sung và giữ ngữ cảnh các lượt trước.
- **v2 — Truyền rõ kiểu câu hỏi:** thêm `response_type` vào danh sách `required` của schema `clarify`. Implementation của tool và nội dung eval giữ nguyên.
- **v3 — Xác nhận trước khi gửi:** thay riêng đoạn prompt yêu cầu gửi ngay bằng quy tắc hỏi `clarify(response_type="yes_no")`, chờ xác nhận nội dung/đích gửi và chỉ gọi `send(confirmed=true)` khi đủ điều kiện. Lần đo v3 giảm điểm; kết quả và lỗi phát sinh được ghi ở B1.

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
|  |  |  |  |  |

### B3. Team Eval Cases

Liệt kê đúng 10 case trong `starter_v0/data/eval_group.json` (5 single turn + 5 multi turn).

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
|  |  |  |  |

### B4. Live Chat Evidence

Lấy từ `starter_v0/transcripts/*.transcript.json`.

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
|  |  |  |  |  |

### B5a. Required Evidence — Tool mới, unit test, UI

| Item | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Tool mới (`tools/<tên>/`) |  |  |  |
| Unit test tool mới (≥ 3 test/tool) | `pytest` output (0 failed) |  |  |
| UI (lệnh chạy + link dùng thử) |  |  |  |

Tool unit tests: số test đã viết, và một ví dụ lỗi mà unit test bắt được nhưng eval không bắt được.

### B5. Bonus Evidence

Chỉ điền nếu nhóm làm bonus (ghi riêng, tối đa 10 điểm). Tool có sẵn (`send`, `policy`, `papers`, `paper_text`) không tự được bonus.

| Bonus | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Small Local Model | xem B7 |  |  |
| Hơn 3 tool mới (≥ 4) |  |  |  |
| `send` gửi thật lên Telegram sau xác nhận | transcript |  |  |
| Test challenge (0 skipped / regression test) | `pytest` output |  |  |

Test challenge: số bug tìm được trong tool có sẵn (nếu có), cách sửa, và test regression tương ứng.

### B7. Small Local Model Challenge (bonus)

Chỉ điền nếu nhóm làm bonus này.

| Version | Model (provider) | Prompt/Tools | case_accuracy | tool_routing | argument | multiturn | Run File |
|---|---|---|---|---|---|---|---|
| v3 | (cloud) | v3 |  |  |  |  |  |
| v3-<model> | (ollama) | v3 |  |  |  |  |  |
| v3-<model> | (ollama) | v3 |  |  |  |  |  |
| v4-local |  |  |  |  |  |  |  |
| v5-local |  |  |  |  |  |  |  |

Lỗi đặc thù của model nhỏ (đếm từ run JSON):

| Failure Pattern | Count | Example Case | Fix Tried | Helped? |
|---|---|---|---|---|
| wrong / hallucinated tool |  |  |  |  |
| invalid JSON args (`_invalid_json_arguments`) |  |  |  |  |
| no tool call / answered directly |  |  |  |  |
| missed `clarify` |  |  |  |  |
| repeated / unnecessary calls |  |  |  |  |

- Cái gì giúp model nhỏ gọi tool đúng hơn nhất? Bằng chứng?
- Bản prompt tối ưu cho local chạy trên model cloud thì sao?
- Khi nào nhóm sẽ chọn model local thay vì cloud cho agent này?

## 5. Khó khăn và cách xử lý

> Khó khăn chính và cách nhóm xử lý. Nếu gặp lỗi kỹ thuật (provider lỗi, hết quota API, tool không chạy), mô tả lỗi và dẫn bằng chứng: run JSON, log, ảnh chụp.

-

## 6. Tổng hợp đóng góp

Chi tiết đóng góp của từng thành viên nằm trong [TEAM.md](../../TEAM.md) và các báo cáo cá nhân `report/team/MSSV_HoTen.md`.

## 7. Hạn chế và hướng cải thiện — B6. Reflection

- Fix nào thuộc `system_prompt.md`?
- Fix nào thuộc `tools.yaml`?
- Failure nào cần review thủ công thay vì chấm tự động?
- Nếu có thêm một vòng, nhóm sẽ thử giả thuyết nào?

## 8. Tài liệu tham khảo

-
