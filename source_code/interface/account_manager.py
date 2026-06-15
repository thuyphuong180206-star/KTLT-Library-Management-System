"""
MÔ-ĐUN QUẢN LÝ TÀI KHOẢN VÀ PHÂN QUYỀN TRÊN CONSOLE (INTERFACE LAYER - ACCOUNT INTERFACE)
Nhiệm vụ: Hiển thị các biểu mẫu (form) đăng nhập, đăng ký thẻ độc giả, đổi mật khẩu bảo mật qua màn hình dòng lệnh.
Quy tắc kiến trúc: Nhận tham chiếu mảng người dùng hệ thống từ RAM, phối hợp gọi hàm từ validator.py để lọc lỗi cú pháp gõ phím.

Các hàm bắt buộc phải viết trực tiếp:
    - show_login_form(user_list: list[User]) -> User | None:
        + Xử lý: Dùng lệnh input() hứng tài khoản và mật khẩu. Chạy vòng lặp duyệt mảng RAM user_list để so khớp.
        + Kết quả trả về: Tham chiếu đối tượng User nếu thông tin chính xác phục vụ phân luồng Menu chính; trả về None nếu sai tài khoản.
    - show_register_form(user_list: list[User]) -> bool:
        + Xử lý: Biểu mẫu tạo thẻ độc giả. Nhận chuỗi họ tên, tên tài khoản, mật khẩu. Gọi validator để kiểm tra chuỗi rỗng.
          Nếu hợp lệ, tự động sinh mã user_id theo mẫu `^U\d{5}$`, khởi tạo thực thể User (mức ưu tiên mặc định "Standard", role="reader"),
          gọi phương thức `.append()` trực tiếp vào mảng RAM user_list. Trả về True nếu tác vụ thành công.
"""
