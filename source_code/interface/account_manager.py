"""
Mô-đun quản lý tài khoản (Account Manager)
Nhiệm vụ: Xử lý đăng nhập hệ thống và tạo tài khoản bạn đọc mới.
"""

from interface import validator
from objects.users import User

def login(user_array) -> User | str | None:
    """
    Xử lý biểu mẫu đăng nhập hệ thống.
    Nhận user_id và password từ bàn phím. Tìm trong UserArray, so khớp password.
    Trả về: Đối tượng User nếu đúng, None nếu sai, hoặc "EXIT_SIGNAL" nếu muốn thoát.
    """
    print("\n" + "=" * 50)
    print("🔑 ĐĂNG NHẬP HỆ THỐNG".center(50))
    print("=" * 50)

    user_id_input = input("Tài khoản (Mã số / '0' hoặc 'exit' để thoát): ").strip()
    
    # Bắt tín hiệu thoát đẩy về cho main.py xử lý lưu file
    if user_id_input.lower() in ['0', 'exit']:
        return "EXIT_SIGNAL"

    password_input = input("Mật khẩu: ").strip()

    # Sử dụng phương thức get_by_id() của cấu trúc dữ liệu tự build UserArray
    user = user_array.get_by_id(user_id_input)

    # Kiểm tra tồn tại và so khớp mật khẩu
    if user is not None and user.password == password_input:
        return user

    print("\n[!] Đăng nhập thất bại: Sai tài khoản hoặc mật khẩu.")
    return None


def create_reader(user_array) -> tuple[bool, str]:
    """
    Xử lý biểu mẫu tạo tài khoản bạn đọc mới (Chỉ dành cho Admin/Thủ thư thao tác).
    Nhập user_id -> xác định reader_type -> kiểm tra trùng lặp -> tạo User.
    Trả về: (thành công: bool, thông báo: str)
    """
    print("\n" + "=" * 50)
    print("📝 TẠO TÀI KHOẢN BẠN ĐỌC MỚI".center(50))
    print("=" * 50)

    # 1. Nhập Mã định danh và gọi màng lọc Regex để tự động phân loại
    user_id = input("Nhập Mã độc giả (MSSV hoặc Mã Giảng viên): ").strip()
    
    reader_type = validator.validate_user_id(user_id)
    if reader_type is None:
        # Nếu None, validator đã tự in dòng báo lỗi định dạng ra màn hình rồi
        return False, "Định dạng mã độc giả không hợp lệ."

    # 2. Kiểm tra mã độc giả đã tồn tại trong mảng RAM chưa
    existing_user = user_array.get_by_id(user_id)
    if existing_user is not None:
        print(f"\n[!] Lỗi: Mã độc giả '{user_id}' đã tồn tại trong hệ thống (Họ tên: {existing_user.fullname}).")
        return False, "Mã độc giả đã tồn tại."

    # 3. Thu thập thông tin cá nhân cơ bản
    fullname = input("Họ và tên đầy đủ: ").strip()
    password = input("Mật khẩu bảo mật: ").strip()

    # 4. Kiểm tra rỗng và check độ dài mật khẩu (gọi validator)
    if not validator.validate_non_empty({"fullname": fullname, "password": password}):
        # validator.validate_non_empty đã tự in cảnh báo rỗng
        return False, "Trường thông tin bị bỏ trống."
        
    if not validator.validate_password(password):
        # validator.validate_password đã tự in cảnh báo độ dài
        return False, "Mật khẩu không đạt yêu cầu bảo mật."

    # 5. Khởi tạo thực thể User với thông số chính xác
    new_user = User(
        user_id=user_id,
        fullname=fullname,
        password=password,
        role="user",
        reader_type=reader_type
    )

    # 6. Đẩy thẳng vào cuối mảng UserArray O(1)
    user_array.append(new_user)

    # Thông báo thành công
    str_type = "Sinh viên" if reader_type == "student" else "Giảng viên"
    print(f"\n[✓] Cấp thẻ thành công!")
    print(f"    Họ tên   : {new_user.fullname}")
    print(f"    Tài khoản: {new_user.user_id} ({str_type})")
    print(f"    Hạn mức  : {new_user.borrow_limit} cuốn / {new_user.borrow_duration} ngày")
    
    return True, "Tạo tài khoản bạn đọc thành công."
