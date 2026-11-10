# Phân công 5 người — Research Agent Tool Eval

Tài liệu này chia phần việc còn lại của repo cho 5 thành viên, tạm gọi là TV1–TV5. Mỗi người nhận **20/100 điểm khối lượng ước tính**, đã tính cả code, test, eval, báo cáo và phối hợp. Đây là đơn vị lập kế hoạch nội bộ, không phải điểm chấm của bài lab; giả định các thành viên có kinh nghiệm tương đương.

## 1. Căn cứ và hiện trạng đã kiểm tra

Đã đọc `README.md`, `TOOL-SETUP.md`, các artifact, toàn bộ code agent/chat/eval/provider/tool, `TOOL.md`, company policy, unit test và các mẫu bằng chứng trong `samples/`.

| Hạng mục | Hiện trạng trong repo |
|---|---|
| Agent và provider | Có `agent.py`, `chat.py`, `run_eval.py`; có adapter cho OpenRouter, OpenAI, Anthropic, Gemini, Ollama |
| Tool có sẵn | 10 tool đã được khai báo và đăng ký; 6 core, 4 bonus |
| Prompt | Cố ý có chỉ dẫn xấu: đoán dữ liệu thiếu, tự gửi, ép làm một bước |
| Tool declaration | Có schema nhưng mô tả còn mơ hồ, cần bổ sung routing và quy ước args |
| Base eval | 20 case: 14 single turn, 6 multi turn |
| Group eval | `data/eval_group.json` đang có 0 case |
| Extension eval | Có sẵn 10 case tùy chọn |
| Unit test | Đã chạy `python -m pytest -q` trong `starter_v0/`: **62 passed, 17 skipped**, không có test fail |
| UI | Chưa có app UI; `requirements.txt` chưa khai báo Streamlit |
| Version và báo cáo | `version_log.csv` chỉ có header; `REPORT.md` vẫn là mẫu |
| Bằng chứng thật | Chưa có file trong `runs/`, `transcripts/`, `analysis/`; mẫu ở `samples/` là mock |
| Setup live | Repo có `.env.example`; chưa kiểm chứng provider/API thật trong lần rà soát này |

### Các yêu cầu cần thống nhất trước khi làm

1. **Viết 10 group eval case: 5 single turn + 5 multi turn.** Scope của README và REPORT B3 yêu cầu 10, dù Step 4 và Submit còn ghi tối thiểu 5. Kế hoạch này dùng mức 10 để đáp ứng đầy đủ.
2. **UI là bắt buộc**, theo Scope và checklist của README. Việc mẫu REPORT B5 xếp UI cùng bonus không làm mất yêu cầu này.
3. **Ít nhất 1 tool thực sự mới**, có code, `TOOL.md`, registry, schema, ít nhất 3 unit test và ít nhất 1 group eval case kiểm tra routing. Bốn tool bonus có sẵn không được tính là tool mới của nhóm.
4. **Baseline v0 và ít nhất 3 vòng tối ưu v1, v2, v3** bằng provider thật. Mỗi vòng có một giả thuyết, run JSON, hash và metric trước/sau. Có thể cần thêm vòng nếu còn lỗi.
5. **Giữ base eval nguyên nội dung.** Ưu tiên giữ nguyên tên tool để giảm công việc đồng bộ. Nếu rename, phải cập nhật tất cả registry/schema/eval liên quan, gồm cả group eval và frontmatter của tool.
6. **Hoàn thành cả 17 test stub** để đạt `0 failed, 0 skipped` trong kế hoạch này. README Step 4b gọi phần điền stub là challenge, nhưng checklist Testing lại yêu cầu 0 skipped; đây là lựa chọn đáp ứng mức đầy đủ của cả hai phần.
7. **REPORT Phần A trước 16:30**, có link dùng thử, tool và câu hỏi mẫu. Phần B hoàn thiện để nộp; README đặt checkpoint 17:30. Các giờ này là mốc của đề lab, chưa được gán thành deadline ngày cụ thể.

## 2. Bảng phân công và cân bằng khối lượng

| Thành viên | Vai trò | Phần việc chính | Khối lượng |
|---|---|---|---:|
| TV1 | Lead kỹ thuật, setup và tích hợp | Setup/provider 5đ; baseline v0 4đ; tích hợp và kiểm tra gói nộp 5đ; 3 test lookup/fetch 2đ; 2 eval case 2đ; tổng hợp báo cáo 2đ | **20đ** |
| TV2 | Prompt và tool declaration | Tối ưu prompt/schema qua v1–v3 10đ; version log và B1/B2 5đ; 1 test clarify 1đ; 2 eval case 2đ; review routing 2đ | **20đ** |
| TV3 | Tool mới và định dạng kết quả | Implement tool mới 8đ; tài liệu/registry/schema 3đ; 6 test mới/format 5đ; 2 eval case 2đ; A2 và bằng chứng tool mới 2đ | **20đ** |
| TV4 | Eval, QA và phân tích | Chạy v1–v3/group 6đ; tổng hợp/kiểm tra bộ group eval 3đ; 5 test timeline/social/policy 4đ; phân tích log và kiểm tra thủ công 3đ; 2 eval case 2đ; B3 và kết quả test 2đ | **20đ** |
| TV5 | UI, triển khai và demo | UI 8đ; link dùng thử và live chat 5đ; 2 test send 1đ; 2 eval case 2đ; A3/B4/link demo 2đ; kiểm tra UI với bản tích hợp 2đ | **20đ** |

Số test khác nhau vì UI, tối ưu prompt và tool mới có độ khó khác nhau. Mỗi người đều tự viết **1 single-turn case + 1 multi-turn case**, có đầu ra kiểm chứng được và đóng góp báo cáo. Phần điều phối của lead đã nằm trong 20đ của TV1.

## 3. Công việc và nghiệm thu từng người

### TV1 — Lead kỹ thuật, setup, baseline, tích hợp

**Phạm vi:** `requirements.txt`, setup môi trường, kiểm tra provider/runtime, run v0, tích hợp các nhánh và gói nộp.

- Tạo môi trường Python, cài dependencies; cấu hình provider và các key Tavily/Firecrawl/RapidAPI trên máy chạy chung. Bổ sung dependency UI theo nhu cầu TV5.
- Chốt một provider/model để so sánh các version; chạy preflight và smoke test các API đọc dữ liệu. Preflight provider chỉ chứng minh model có structured tool call, chưa chứng minh từng API tool hoạt động.
- Chạy **v0 trước khi sửa prompt/tool declaration**, lưu run thật, chuyển failure và hash cho TV2/TV4, giữ snapshot tương ứng bằng Git.
- Hoàn thành 3 stub: lookup không truyền timeframe; fetch mapping response; fetch cắt markdown ở 4.000 ký tự.
- Điều phối tích hợp; kiểm tra tool mới, UI và artifact cùng chạy trên một bản cuối; xử lý lỗi runtime cản trở việc chạy và ghi lại thay đổi nếu có.
- Tổng hợp REPORT từ nội dung do từng người cung cấp, viết A1 và phần B6 về setup/tích hợp; kiểm tra danh sách file nộp.

**Nghiệm thu:** provider và API đọc đã smoke test; có run v0 và snapshot gốc; 3 test phụ trách pass; bản tích hợp cuối có đủ artifact và bằng chứng thật. `.env` và API key không nằm trong gói nộp.

### TV2 — Prompt, routing, args, versioning

**Phạm vi:** `artifacts/system_prompt.md`, `artifacts/tools.yaml`, `artifacts/version_log.csv`; nội dung REPORT B1/B2 và phần prompt của B6.

- Phân tích failure thực tế của v0; phân biệt lỗi tool, args, thiếu thông tin, ranh giới hành động và gọi thừa.
- Sửa lần lượt các chỉ dẫn xấu của starter; xác định khi nào hỏi lại, khi nào trả lời trực tiếp, khi nào cần nhiều tool và cách xử lý lượt sửa yêu cầu.
- Viết mô tả tool rõ công dụng, khi dùng/khi không dùng; làm rõ handle không có `@`, `topic=news`, timeframe, `Top|Latest`, `limit` và điều kiện `send(confirmed=true)`.
- Với mỗi vòng v1–v3: nhận log từ TV4, nêu **một giả thuyết**, tạo thay đổi có thể quy về giả thuyết đó, bàn giao snapshot để chạy và ghi metric/hash/run path vào CSV.
- Hoàn thành stub clarify với `response_type="choice"`, options và `awaiting_user`.
- Review mong đợi routing của 10 group case trước khi chạy; cung cấp bảng B1/B2 dựa trên log thật.

**Nghiệm thu:** có v0–v3 và thông tin truy vết đầy đủ; từng vòng có giả thuyết và kết quả thực đo; schema khớp signature code; 1 test clarify pass. Không mặc định mọi lần sửa đều cải thiện điểm.

### TV3 — Một tool mới hoàn chỉnh và format

**Phạm vi:** `tools/<tool_moi>/tool.py`, `TOOL.md`, đăng ký trong `tools/__init__.py`, phần schema chuyển TV2 tích hợp; 3 stub tool mới và 3 stub format.

**Đề xuất để chốt nhanh:** tool `rss_read(feed_url, limit)` đọc RSS/Atom public và trả `items` với `title`, `url`, `source`, `summary` để dùng tiếp với `format`. Đây là hướng triển khai đề xuất của kế hoạch, không phải yêu cầu riêng của đề bài. Chọn feed và smoke test trước khi đưa vào demo.

- Chốt tên, signature, schema, output và ranh giới routing ngay đầu buổi để TV2/TV4 không phải chờ code hoàn chỉnh. Nếu chọn `rss_read`, phân biệt rõ yêu cầu đọc RSS/Atom với đọc bài HTML bằng `fetch`.
- Implement tool thật; xử lý URL/input sai, lỗi HTTP và lỗi parse bằng error dict; bảo đảm giới hạn số item và nguồn kết quả.
- Viết `TOOL.md` theo contract, gồm frontmatter và ví dụ; đăng ký implementation; chuyển schema cho TV2 áp dụng.
- Thay 3 stub tool mới bằng test thực: happy path, input không hợp lệ, lỗi HTTP/timeout/parse trả error dict. Mock HTTP hoàn toàn.
- Hoàn thành 3 stub format: nhóm section, đánh số thread, input `None`/rỗng.
- Viết A2 liệt kê toàn bộ tool của bản cuối, đánh dấu tool mới; cung cấp bằng chứng cho B5.

**Nghiệm thu:** tool có implementation và tài liệu, xuất hiện trong registry/schema/UI, contract test xanh; ít nhất 3 test cho tool mới và 3 test format pass; group eval có case gọi đúng tool mới. Đề xuất thêm test nếu có nhánh lỗi quan trọng chưa được kiểm tra.

### TV4 — Eval, QA, phân tích bằng chứng

**Phạm vi:** `data/eval_group.json`, các run sau baseline, `analysis/*.csv`, tổng hợp unit test; REPORT B3 và phần test của B5.

- Nhận 2 case từ mỗi người, tổng hợp thành đúng **10 case: 5 single + 5 multi**, ID duy nhất, `phase="B"`, failure type hợp lệ, `expect` và `metadata.what_it_tests` rõ ràng.
- Mỗi multi-turn case phải có chuyển biến thực: bổ sung dữ liệu, sửa args, đổi nguồn hoặc thay đổi ý định. Harness dùng lịch sử làm ngữ cảnh để chấm hành động ở lượt cuối.
- Chạy base eval cho từng snapshot v1/v2/v3 và group eval cho bản tích hợp cuối; chuyển log ngay cho TV2 để quyết định thay đổi tiếp theo.
- Hoàn thành 5 stub: timeline limit/bỏ item thiếu ID; social_search truyền search_type; policy query rỗng, lọc area, tách instruction-like text sang `untrusted_text`.
- Dùng `scripts/parse_runs.py` xuất CSV; đối chiếu failure, tool result và metric. Tổng hợp thay đổi test từ các thành viên và chạy toàn suite đến 0 failed, 0 skipped.
- Kiểm tra thủ công câu trả lời và live transcript ở những chỗ harness chưa chấm được; điền B3 và số liệu test/bug vào B5.

**Nghiệm thu:** đủ 10 case hợp lệ, không chỉnh nội dung base eval; có run và CSV phân tích; báo cả 4 accuracy, số case đo được và provider errors; 5 test phụ trách pass; toàn suite không fail/skip.

### TV5 — UI, link dùng thử, live demo

**Phạm vi:** UI mới, đề xuất `starter_v0/app.py` bằng Streamlit; tích hợp `chat.py`; transcript, link demo; REPORT A3/B4 và phần UI của B5.

- Dựng UI chat, giữ lịch sử theo session, hiển thị kết quả có nguồn và trạng thái gọi tool/lỗi.
- Tận dụng `run_model_tool_loop()` trong `chat.py` để thực hiện nhiều vòng tool và dừng khi `awaiting_user`; giữ logic dùng chung với CLI.
- Lưu transcript thật, có provider/model/version/hash và các tool event; kiểm tra câu trả lời sau lượt bổ sung thông tin vẫn dùng đúng ngữ cảnh.
- Tạo link dùng thử bằng cách triển khai phù hợp hoặc tunnel theo README; kiểm tra mở được từ máy khác và giữ phiên chạy trong demo.
- Chạy `chat.py` **ít nhất 3 lượt live có transcript**: yêu cầu research thường; yêu cầu thiếu thông tin; lượt bổ sung. Kiểm tra riêng yêu cầu gửi sẽ hỏi xác nhận. Gửi Telegram thật và transcript xác nhận trước khi gửi thuộc phần bonus nếu nhóm triển khai.
- Hoàn thành 2 stub send bằng mock: đã confirmed thì POST đúng; thiếu env thì error và không request.
- Soạn 3–5 câu hỏi demo, điền link/A3/B4; kiểm tra UI với prompt/schema/tool mới của bản cuối.

**Nghiệm thu:** UI dùng provider thật, chạy đa lượt và tool mới; link mở từ máy khác; có transcript CLI thật từ ít nhất 3 lượt; 2 test send pass. Giao diện hiển thị lỗi API đúng thực tế.

## 4. Chia đều 10 group eval case

Đây là thiết kế case để từng người viết JSON, chưa phải case đã được thêm hay kết quả đã chạy.

| Người viết | Single-turn case | Multi-turn case |
|---|---|---|
| TV1 | G01S: Tin một chủ đề trong tháng → `lookup`, news/month | G01M: Giữ chủ đề, đổi thời gian ngày → tuần; lượt cuối dùng week |
| TV2 | G02S: Yêu cầu đọc bài nhưng thiếu URL → `clarify(text)` | G02M: Thiếu tài khoản → cung cấp handle → sửa số bài; giữ đúng handle và số mới |
| TV3 | G03S: Đọc RSS/Atom cụ thể → tool mới, đúng URL/limit | G03M: Đã cung cấp feed → sửa limit; gọi tool mới với URL cũ và limit mới |
| TV4 | G04S: Tìm tweet phổ biến theo chủ đề → `social_search(Top)` | G04M: Giữ chủ đề, chuyển tìm web news sang social Latest |
| TV5 | G05S: Yêu cầu đăng Telegram chưa xác nhận → `clarify(yes_no)` | G05M: Đang chuẩn bị gửi, user hủy và chỉ hỏi khả năng agent → không gọi tool |

TV4 kiểm tra format, TV2 review routing, mỗi tác giả sửa case của mình khi review phát hiện mơ hồ. Mỗi người cung cấp thêm 1–2 câu giải thích case đó đo lỗi gì và vì sao expected behavior hợp lý.

## 5. Thứ tự bàn giao và kiểm soát thay đổi

1. **TV1 chạy v0 trên prompt/schema nguyên bản.** Trong lúc đó TV3 thiết kế tool, TV5 dựng UI; TV2/TV4 đọc requirements và thiết kế case/test.
2. TV1 bàn giao v0 cho TV2/TV4. TV2 có thể chuẩn bị sửa prompt; TV3 bàn giao contract tool sớm để UI/eval làm song song.
3. Để so sánh rõ ràng, kế hoạch ưu tiên tích hợp tool mới trong một version riêng, ví dụ **`v0-tool`**, chạy base để ghi tác động của việc thêm tool. Sau đó giữ ổn định tập tool trong v1–v3. Ghi version bổ sung này vào CSV/REPORT.
4. TV2 bàn giao snapshot cho TV4 chạy; TV4 trả log; TV2 phân tích rồi mới chốt thay đổi tiếp theo. Nếu thêm/sửa tool hoặc runtime trong quá trình này, ghi thành thay đổi riêng, chạy lại phần liên quan và giữ bằng chứng.
5. Mỗi run dùng prompt/schema cố định và snapshot Git tương ứng. UI có thể phát triển song song; so sánh model dùng cùng provider/model và cùng bộ base case.
6. TV1 tích hợp bản cuối; TV4 chạy base/group và unit test; TV5 kiểm tra UI/CLI và lưu transcript với đúng version cuối. Bằng chứng dùng bản cũ phải ghi đúng nhãn bản cũ.

**Đầu mối cho file dùng chung:** TV2 tích hợp `tools.yaml` và ghi `version_log.csv`; TV3 tích hợp registry; TV4 tích hợp `eval_group.json` và các section test của từng người; TV1 tổng hợp REPORT. Các thành viên bàn giao patch/nội dung của phần mình để tránh ghi đè.

Mỗi checkpoint rà lại tải công việc. Người xong trước nhận một task review/test/tích hợp chưa xong từ người đang quá tải; ghi lại việc chuyển giao để giữ tổng khối lượng quanh 20đ/người.

## 6. Checkpoint theo đề lab

| Mốc của README | Kết quả cần có | Đầu mối |
|---|---|---|
| 15:00 | Provider chạy, baseline v0; UI có khung hoạt động | TV1 + TV5 |
| 15:30 | Tool mới hoạt động; bắt đầu có kết quả cải tiến v1; theo dõi riêng lần thêm tool | TV2 + TV3 + TV4 |
| 16:00 | 10 group case đã tổng hợp; v2 có log; UI dùng được luồng research | TV2 + TV4 + TV5 |
| Trước 16:30 | REPORT A hoàn chỉnh: A1, A2, A3, link dùng thử; bản demo đã smoke test | TV1 tổng hợp, cả nhóm bàn giao phần mình |
| 16:30 | Team showdown: demo, ghi nhận lỗi thực tế | TV5 demo; cả nhóm theo dõi |
| 17:30 | v3 có log; test xanh; report B và gói nộp hoàn chỉnh | Cả 5 người theo phần đã giao |

Nếu áp dụng ngoài buổi lab, giữ nguyên thứ tự phụ thuộc và chuyển các checkpoint thành mốc tương đối theo giờ bắt đầu thực tế.

## 7. Cách đọc kết quả để nghiệm thu đúng

- Eval chấm tên tool và **subset args được khai báo trong expect**. Tool có thể chạy lỗi API nhưng routing vẫn PASS; phải đọc cả `tool_results`, chạy unit test và smoke test thật.
- Với `no_tool`, harness hiện chỉ kiểm tra không có tool call, chưa đánh giá nội dung từ chối/trả lời đúng. TV4 kiểm tra thủ công và ghi nhận xét.
- Multi-turn eval gộp lượt trước thành context, chưa chứng minh toàn bộ cuộc hội thoại hỏi lại/xác nhận chạy đúng. Transcript live của TV5 là bằng chứng bổ sung.
- Các case cần tool dùng `tool_choice="required"` trong eval, còn chat live dùng lựa chọn tự động. Kiểm tra live để biết agent có tự chọn tool khi cần hay không.
- Provider errors bị loại khỏi mẫu số accuracy trong `summarize()`. Báo cả `measured_cases` và `provider_error_cases` để hiểu đúng điểm số.
- Mẫu trong `samples/` chỉ tham khảo format; số liệu, hash, run path và transcript đưa vào báo cáo phải từ lần chạy thật.

## 8. Gói nộp và phần tùy chọn

TV1 đối chiếu các mục sau, từng chủ phần cung cấp bằng chứng:

- [ ] `artifacts/system_prompt.md`, `tools.yaml` cuối cùng; còn ít nhất 5 tool và tool mới được đăng ký đầy đủ.
- [ ] `artifacts/version_log.csv` có v0, v1, v2, v3; có version thêm tool và các version bổ sung nếu thực hiện.
- [ ] `artifacts/REPORT.md` có Phần A/B; không để trống số liệu bắt buộc hay dùng số liệu mẫu.
- [ ] `data/eval_group.json` có 5 single + 5 multi; có routing case cho tool mới.
- [ ] Tool mới có `tool.py`, `TOOL.md`, registry, schema và ít nhất 3 unit test.
- [ ] `pytest` báo 0 failed, 0 skipped; không xóa test hoặc chuyển sang xfail để che lỗi.
- [ ] Có `runs/*.json`, `transcripts/*.transcript.json`; kế hoạch này cũng xuất `analysis/*.csv` để dùng cho báo cáo.
- [ ] Có code UI, dependencies, hướng dẫn chạy và link dùng thử đã kiểm tra.
- [ ] API key, `.env` và dữ liệu bí mật không có trong artifact nộp.

**Bonus chỉ bắt đầu sau khi phần bắt buộc ổn định:** Telegram gửi thật có xác nhận; extension eval cho policy/arXiv; poster HTML/SVG; Small Local Model Challenge. Nếu làm local challenge, phải có ít nhất 2 model kích thước khác nhau, không quá 8B, ít nhất 2 vòng tối ưu local, kiểm tra ngược trên cloud và REPORT B7 có log.

Điều kiện bonus “UI + hơn 3 tool mới” nghĩa là **ít nhất 4 tool mới do nhóm viết**. Kế hoạch chính chỉ cam kết 1 tool mới. Nếu chọn bonus này, phải lập thêm vòng công việc được chia đều, bao gồm test/tài liệu/registry/schema/eval cho từng tool.

## 9. Lệnh vận hành tham chiếu

Chạy từ `starter_v0/`, sau khi setup môi trường. Đây là lệnh giao cho nhóm thực hiện; lần rà soát hiện tại chỉ chạy unit test offline.

```powershell
python scripts/preflight_provider.py --provider openrouter
python -m pytest -q
python run_eval.py --provider openrouter --version v0 --suite base --eval-cases data/eval_base.json
# Chạy v1/v2/v3 trên đúng snapshot của từng version; chỉ đổi --version là chưa đủ.
python run_eval.py --provider openrouter --version v3 --suite base --eval-cases data/eval_base.json
python run_eval.py --provider openrouter --version v3 --suite group --eval-cases data/eval_group.json
python scripts/parse_runs.py runs/ --output analysis/base_runs.csv
python chat.py --provider openrouter --version v3
# Sau khi TV5 tạo app.py và bổ sung dependency:
streamlit run app.py
```

Nếu nhóm chọn provider/model khác, cập nhật nhất quán trong lệnh chạy và báo cáo. Dùng đúng nhãn version của bản tích hợp cuối khi tạo log và transcript.
