# Báo cáo cá nhân — HoVaTen-MSSV

Đổi tên file theo quy tắc `MSSV_HoTen.md`.

Ví dụ: `20241234_NguyenVanAn.md`.

## 1. Thông tin thành viên

- Họ tên: Đặng Khắc Hoàng Minh
- MSSV: 2A202604082
- Email: 26ai.minhdkh@vinuni.edu.vn

## 2. Phần việc phụ trách
Step 4:  Viết eval của nhóm
...
Viết đúng 10 case vào data/eval_group.json: 5 single turn (query) + 5 multi turn (turns). Ít nhất 1 case kiểm tra model có route tới tool mới của nhóm.

Mỗi case cần có:

id
phase: luôn là "B"
query hoặc turns
failure_type: một trong wrong_tool, wrong_arg_value, wrong_boundary, unnecessary_tool, out_of_scope, missing_info
expect: tool_calls hoặc no_tool
metadata.what_it_tests
## 3. Đóng góp cụ thể
- Viết đúng 10 case vào data/eval_group.json
- 5 single turn (query) + 5 multi turn (turns).
...

## 4. Bằng chứng

- File/commit/PR: 9c17ab038d129094d9b01a6d3aa775bcf79c2c2c
- AI/công cụ đã dùng và cách tự kiểm tra kết quả: Dùng Codex để tạo các case

## 5. Tự đánh giá
Tôi thấy tôi đã hoàn thành được công việc đúng thời hạn được team giao.
...
