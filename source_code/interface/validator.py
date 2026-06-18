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
import re
from typing import Optional

# ==========================================
# 1. VALIDATOR CHO NGƯỜI DÙNG & TÀI KHOẢN
# ==========================================

def validate_user_id(user_id: str) -> Optional[str]:
    """
    Phân loại mã định danh bằng Regex.
    Trả về: 'student' (MSSV), 'lecturer' (Mã GV), hoặc None nếu sai.
    """
    user_id = user_id.strip()
    if re.fullmatch(r"\d{8,9}", user_id):
        return "student"
    if re.fullmatch(r"002\.\d{3}\.\d{5}", user_id):
        return "lecturer"
        
    print("\n[!] Lỗi: Định dạng mã độc giả không hợp lệ.")
    print("    - Sinh viên: Chỉ gồm 8 đến 9 chữ số (Ví dụ: 20231234).")
    print("    - Giảng viên: Phải theo định dạng 002.xxx.xxxxx (Ví dụ: 002.123.45678).")
    return None

def validate_password(password: str) -> bool:
    """Kiểm tra độ mạnh của mật khẩu (tối thiểu 6 ký tự)."""
    if len(password.strip()) < 6:
        print("\n[!] Lỗi: Mật khẩu quá ngắn. Cần tối thiểu 6 ký tự để đảm bảo an toàn.")
        return False
    return True

def validate_person_name(name: str) -> bool:
    """
    Kiểm tra tên người (Tác giả / Tên độc giả).
    Chỉ cho phép chữ cái (hỗ trợ Tiếng Việt) và khoảng trắng, giới hạn 2-50 ký tự.
    """
    name = name.strip()
    # Regex hỗ trợ chữ cái tiếng Việt và khoảng trắng
    if not re.fullmatch(r"^[A-Za-zÀ-ỹ\s]{2,50}$", name):
        print("\n[!] Lỗi: Tên/Tác giả chỉ được chứa chữ cái và khoảng trắng (2-50 ký tự).")
        return False
    return True

# ==========================================
# 2. VALIDATOR CHO SÁCH & KHO
# ==========================================

def validate_book_id(book_id: str) -> bool:
    """
    Kiểm tra định dạng Mã sách.
    Quy tắc: Phải bắt đầu bằng chữ 'B' (hoặc 'b') theo sau là 3-4 chữ số (VD: B001, B1024).
    """
    book_id = book_id.strip().upper()
    if not re.fullmatch(r"B\d{3,4}", book_id):
        print("\n[!] Lỗi: Mã sách phải bắt đầu bằng chữ 'B' kèm theo 3-4 chữ số (Ví dụ: B001, B102).")
        return False
    return True

def validate_quantity(qty_str: str) -> bool:
    """Kiểm tra chuỗi số lượng có phải là số nguyên dương hay không."""
    qty_str = str(qty_str).strip()
    if qty_str.isdigit() and int(qty_str) >= 0:
        return True
    print("\n[!] Lỗi: Số lượng phải là một số nguyên dương không âm.")
    return False

# ==========================================
# 3. VALIDATOR CHUNG (GENERAL)
# ==========================================

def validate_non_empty(fields: dict) -> bool:
    """Kiểm tra một tập hợp các trường dữ liệu xem có bị rỗng không."""
    for key, value in fields.items():
        if not str(value).strip():
            print(f"\n[!] Lỗi: Trường dữ liệu '{key}' không được bỏ trống.")
            return False
    return True

def validate_text_length(text: str, field_name: str, max_len: int = 50) -> bool:
    """
    Giới hạn độ dài chuỗi để tránh việc nhập rác làm vỡ giao diện ASCII.
    """
    if len(text.strip()) > max_len:
        print(f"\n[!] Lỗi: {field_name} quá dài (Tối đa {max_len} ký tự).")
        return False
    return True
