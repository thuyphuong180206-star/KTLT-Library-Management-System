"""
Mô-đun xác thực dữ liệu đầu vào (Input Validator)
Nhiệm vụ: Kiểm tra và lọc dữ liệu thô từ bàn phím trước khi chuyển xuống logic layer.
Ràng buộc: Hàm trả về True nếu hợp lệ, False nếu không — có in thông báo lỗi ra màn hình.
Các hàm:
    - validate_user_id(user_id)
        Dùng regex phân biệt MSSV và mã giảng viên:
            MSSV:       r"^\d{8,9}$"            → trả về "student"
            Mã GV:      r"^002\.\d{3}\.\d{5}$"  → trả về "lecturer"
            Không hợp lệ                         → trả về None

    - validate_non_empty(fields)
        Kiểm tra tất cả giá trị trong dict không được rỗng sau khi strip().
        Trả về: bool

    - validate_quantity(qty_str)
        Kiểm tra chuỗi có thể ép kiểu int và giá trị > 0.
        Trả về: bool

    - validate_password(password)
        Kiểm tra mật khẩu không rỗng và tối thiểu 6 ký tự.
        Trả về: bool
Import bởi: interface.account_manager, interface.menu
"""
