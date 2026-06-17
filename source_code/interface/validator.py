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

def validate_user_id(user_id: str) -> str | None:
    """
    Phân loại mã định danh bằng Regex.
    Trả về: 'student' (nếu là MSSV), 'lecturer' (nếu là Mã GV), hoặc None nếu sai định dạng.
    """
    user_id = user_id.strip()
    
    # Regex cho Sinh viên: Chuỗi có đúng 8 hoặc 9 chữ số (VD: 20211234)
    if re.match(r"^\d{8,9}$", user_id):
        return "student"
        
    # Regex cho Giảng viên: Bắt đầu bằng 002. tiếp theo 3 số, dấu . và 5 số (VD: 002.123.45678)
    if re.match(r"^002\.\d{3}\.\d{5}$", user_id):
        return "lecturer"
        
    # Nếu không khớp cái nào ở trên -> Báo lỗi
    print("\n[!] Lỗi: Định dạng mã độc giả không hợp lệ.")
    print("    - Sinh viên: Chỉ gồm 8 đến 9 chữ số (Ví dụ: 20231234).")
    print("    - Giảng viên: Phải theo định dạng 002.xxx.xxxxx (Ví dụ: 002.123.45678).")
    return None

def validate_non_empty(fields: dict) -> bool:
    """
    Kiểm tra một tập hợp các trường dữ liệu xem có bị rỗng không.
    Input: dict với key là tên trường, value là giá trị người dùng nhập.
    """
    for key, value in fields.items():
        if not str(value).strip():
            print(f"\n[!] Lỗi: Trường dữ liệu '{key}' không được bỏ trống.")
            return False
    return True

def validate_quantity(qty_str: str) -> bool:
    """
    Kiểm tra chuỗi số lượng có phải là số nguyên dương hay không.
    """
    qty_str = str(qty_str).strip()
    # isdigit() đảm bảo nó là số nguyên không âm (không chứa chữ hay dấu trừ)
    if qty_str.isdigit() and int(qty_str) > 0:
        return True
    return False

def validate_password(password: str) -> bool:
    """
    Kiểm tra độ mạnh của mật khẩu (tối thiểu 6 ký tự).
    """
    if len(password.strip()) < 6:
        print("\n[!] Lỗi: Mật khẩu quá ngắn. Cần tối thiểu 6 ký tự để đảm bảo an toàn.")
        return False
    return True
