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
    Dùng regex phân biệt MSSV và mã giảng viên.
    - MSSV  : 8-9 chữ số -> trả về "student"
    - Mã GV : 002.XXX.XXXXX -> trả về "lecturer"
    - Sai   : in lỗi -> trả về None
    """
    user_id_clean = user_id.strip()
    
    student_pattern = r"^\d{8,9}$"
    lecturer_pattern = r"^002\.\d{3}\.\d{5}$"
    
    if re.match(student_pattern, user_id_clean):
        return "student"
    elif re.match(lecturer_pattern, user_id_clean):
        return "lecturer"
    else:
        print("[!] Lỗi nhập liệu: Mã định danh không hợp lệ.")
        print("    - Sinh viên nhập MSSV gồm 8-9 chữ số (Ví dụ: 20211234).")
        print("    - Giảng viên nhập mã dạng 002.XXX.XXXXX (Ví dụ: 002.123.45678).")
        return None

def validate_non_empty(fields: dict[str, str]) -> bool:
    """
    Kiểm tra tất cả giá trị trong dict không được rỗng sau khi strip().
    Gom toàn bộ lỗi và in ra một lần để tối ưu trải nghiệm (UX).
    """
    is_valid = True
    error_list = []
    
    for key, value in fields.items():
        # Ép kiểu về string để đề phòng value truyền vào là số (int/float)
        if not str(value).strip():
            error_list.append(key)
            is_valid = False
            
    if not is_valid:
        print("[!] Lỗi biểu mẫu: Các trường sau không được để trống:")
        for err in error_list:
            print(f"    - {err}")
            
    return is_valid

def validate_quantity(qty_str: str) -> bool:
    """
    Kiểm tra chuỗi có thể ép kiểu int và giá trị > 0.
    Phục vụ cho việc nhập số lượng khi thêm sách mới.
    """
    try:
        quantity = int(qty_str.strip())
        if quantity > 0:
            return True
        else:
            print(f"[!] Lỗi logic: Số lượng nhập vào ({quantity}) không hợp lệ. Phải lớn hơn 0.")
            return False
    except ValueError:
        print("[!] Lỗi định dạng: Số lượng phải là số nguyên dương (Ví dụ: 5, 10).")
        return False

def validate_password(password: str) -> bool:
    """
    Kiểm tra mật khẩu không rỗng và tối thiểu 6 ký tự.
    """
    pwd_clean = password.strip()
    
    if not pwd_clean:
        print("[!] Lỗi bảo mật: Mật khẩu không được để trống.")
        return False
        
    if len(pwd_clean) < 6:
        print(f"[!] Lỗi bảo mật: Mật khẩu quá ngắn ({len(pwd_clean)} ký tự). Yêu cầu tối thiểu 6 ký tự.")
        return False
        
    return True
