# Kế hoạch Đối ngoại năm học 2026–2027 · CLB Ngoại khoa Trưng Vương

App một trang để theo dõi các đầu việc đối ngoại của CLB trong năm học: ai phụ trách, hạn, trạng thái, quyết định, biên bản họp, cùng bốn bảng làm việc. Chạy hoàn toàn trong trình duyệt; không có máy chủ, không cần đăng nhập.

## Dùng

Mở `index.html` (bấm đúp trên máy tính, hoặc mở địa chỉ web nếu đã đặt lên GitHub Pages).

| Mục | Để làm gì |
|---|---|
| Tổng quan | Tiến độ các đầu việc, timeline chương trình, việc quá hạn và sắp đến hạn |
| Họp | Đi lần lượt từng đầu việc: người phụ trách, hạn, quyết định, ghi chú, bảng liên quan; cuối cùng xuất biên bản |
| Đầu việc | Xem và sửa chi tiết từng đầu việc |
| Chương trình | Bảng chương trình ngoài CLB: tháng, ngày chính, trưởng ban, chỉ tiêu học viên, bản kế hoạch chuẩn; timeline theo tháng |
| Fanpage | Danh mục loại bài đăng và lịch đăng bài |
| Đối tác | CLB học thuật và đơn vị muốn hợp tác |
| Áo CLB | Góp ý áo năm trước theo từng nhà; các phương án áo mới |
| Phân công | Bảng tất cả việc cụ thể, lọc theo người, trạng thái, quá hạn |
| Lịch | Các hạn, ngày chính của chương trình, ngày đăng bài, xếp theo tháng |
| Nhân sự | Danh sách tên để gợi ý khi phân công |
| Lưu trữ | Xuất biên bản (Word, PDF, Markdown), các bảng (CSV), sao lưu và khôi phục |

## Dữ liệu nằm ở đâu

Tên người, hạn, ghi chú, nội dung các bảng **chỉ lưu trong trình duyệt của máy đang dùng**. Kho mã chỉ chứa khung kế hoạch.

- Mỗi địa chỉ mở app (tệp trên máy, hoặc địa chỉ web) có kho dữ liệu riêng. Nên dùng cố định một cách mở.
- App này dùng kho dữ liệu riêng, không lẫn với app kế hoạch nội bộ dù cùng địa chỉ web gốc.
- Chuyển sang máy khác hoặc gửi cho người cùng quản lý: **Lưu trữ → Sao lưu dữ liệu**, rồi bên kia **Khôi phục từ tệp sao lưu**.
- Nên sao lưu sau mỗi cuộc họp.

## Sửa khung kế hoạch

- Khi khung gốc có thêm đầu việc mới, máy đã có dữ liệu tự nhận thêm đầu việc đó lúc mở app, giữ nguyên dữ liệu cũ; đầu việc người dùng đã xóa không bị thêm lại.

- Sửa nhỏ: ngay trong app, mục “Sửa khung đầu việc” ở cuối mỗi đầu việc; các bảng thêm, xóa dòng trực tiếp.
- Sửa khung gốc: sửa `nguon/ke-hoach.json` hoặc `nguon/app.src.html`, rồi chạy `python dong_goi.py`. Lệnh này tạo lại `index.html` và bản kế hoạch Markdown ở thư mục cha. Khung gốc mới chỉ áp dụng cho máy chưa có dữ liệu, hoặc sau khi bấm “Đặt lại về khung gốc”.
- Mã app tách từ app kế hoạch nội bộ (`../../KẾ HOẠCH NỘI BỘ/app-ke-hoach/`), thêm phần bảng, timeline và cấu hình tên app trong `ke-hoach.json` (mục `app`, `bang`).
