"""
Mô-đun quản lý tài khoản (Account Manager)
Nhiệm vụ: Xử lý đăng nhập hệ thống và tạo tài khoản bạn đọc mới.
Các hàm:
    - login(user_array)
        Nhận user_id và password từ bàn phím.
        Tìm trong UserArray, so khớp password.
        Trả về: User nếu đúng, None nếu sai.
        Không giới hạn số lần thử.

    - create_reader(user_array)
        Chỉ admin được gọi hàm này.
        Nhập user_id (MSSV hoặc mã GV) → gọi validate_user_id()
        để tự động xác định reader_type.
        Kiểm tra user_id chưa tồn tại trong UserArray.
        Nhập fullname, password → tạo User mới → append vào UserArray.
        Trả về: (bool, str) — (thành công, thông báo)
Import: interface.validator, objects.users.User
Import bởi: interface.menu, main
"""
from objects.users import User
from interface import validator

def show_login_form(user_list: list[User]) -> User | None:
    """
    Xử lý biểu mẫu đăng nhập.
    Duyệt mảng RAM user_list để so khớp thông tin.
    """
    print("\n" + "=" * 50)
    print("🔑 ĐĂNG NHẬP HỆ THỐNG".center(50))
    print("=" * 50)

    # Class User sử dụng user_id làm định danh đăng nhập chính
    account_input = input("Tài khoản (Mã hệ thống cấp): ").strip()
    password_input = input("Mật khẩu: ").strip()

    # Chạy vòng lặp duyệt mảng RAM để so khớp
    for user in user_list:
        if user.user_id == account_input and user.password == password_input:
            if not user.is_active():
                print("\n[!] Lỗi: Tài khoản của bạn đã bị khóa hoặc vô hiệu hóa.")
                return None
            return user

    print("\n[!] Đăng nhập thất bại: Sai tài khoản hoặc mật khẩu.")
    return None


def show_register_form(user_list: list[User]) -> bool:
    """
    Xử lý biểu mẫu tạo thẻ độc giả mới.
    Kiểm tra dữ liệu rỗng bằng validator, sinh mã ^U\d{5}$ và khởi tạo User.
    """
    print("\n" + "=" * 50)
    print("📝 ĐĂNG KÝ THẺ ĐỘC GIẢ MỚI".center(50))
    print("=" * 50)

    fullname = input("Họ và tên đầy đủ: ").strip()
    password = input("Mật khẩu: ").strip()
    
    print("\nPhân loại bạn đọc:")
    print("  1. Sinh viên")
    print("  2. Giảng viên")
    type_choice = input("👉 Chọn (1 hoặc 2): ").strip()

    # 1. Gọi validator để kiểm tra chuỗi rỗng
    if not validator.validate_book_payload({"fullname": fullname, "password": password}):
        # Tận dụng hàm quét rỗng của validator (có thể viết thêm hàm validate_not_empty riêng trong validator.py)
        # Giả định validator có hàm check rỗng mảng:
        print("\n[!] Lỗi: Các thông tin bắt buộc không được để trống.")
        return False

    if type_choice not in ['1', '2']:
        print("\n[!] Lỗi: Lựa chọn phân loại không hợp lệ.")
        return False

    reader_type = "student" if type_choice == '1' else "lecturer"

    # 2. Tự động sinh mã user_id theo mẫu ^U\d{5}$
    max_id = 0
    for user in user_list:
        if user.user_id.startswith('U') and user.user_id[1:].isdigit():
            current_num = int(user.user_id[1:])
            if current_num > max_id:
                max_id = current_num

    new_id_num = max_id + 1
    new_user_id = f"U{new_id_num:05d}"

    # 3. Khởi tạo thực thể User
    # Sử dụng role="user" thay vì "reader" để khớp với VALID_ROLES trong class User
    new_user = User(
        user_id=new_user_id,
        fullname=fullname,
        password=password,
        role="user", 
        reader_type=reader_type,
        status="active"
    )

    # 4. Gọi phương thức .append() trực tiếp vào mảng RAM
    user_list.append(new_user)

    print("\n[✓] Đăng ký thành công!")
    print(f"    Họ tên: {new_user.fullname}")
    print("-" * 50)
    print(f"⚠️ MÃ TÀI KHOẢN ĐĂNG NHẬP CỦA BẠN LÀ: {new_user.user_id}")
    print("    (Hãy ghi nhớ mã này để truy cập hệ thống)")
    
    return True


def show_change_password_form(current_user: User) -> bool:
    """
    Xử lý biểu mẫu đổi mật khẩu bảo mật qua màn hình dòng lệnh.
    """
    print("\n" + "=" * 50)
    print("🛡️ ĐỔI MẬT KHẨU BẢO MẬT".center(50))
    print("=" * 50)
    
    old_password = input("Nhập mật khẩu hiện tại: ").strip()
    
    if old_password != current_user.password:
        print("\n[!] Lỗi: Mật khẩu hiện tại không chính xác.")
        return False
        
    new_password = input("Nhập mật khẩu mới: ").strip()
    confirm_password = input("Xác nhận mật khẩu mới: ").strip()
    
    # Gọi validator kiểm tra rỗng
    if not new_password or not confirm_password:
        print("\n[!] Lỗi: Mật khẩu mới không được để trống.")
        return False
        
    if new_password != confirm_password:
        print("\n[!] Lỗi: Mật khẩu xác nhận không khớp.")
        return False
        
    # Cập nhật trực tiếp vào đối tượng RAM
    current_user.password = new_password
    print("\n[✓] Đổi mật khẩu thành công! Lần đăng nhập sau vui lòng sử dụng mật khẩu mới.")
    return True
