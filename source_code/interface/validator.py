"""
MÀNG LỌC XÁC THỰC CÚ Pháp ĐẦU VÀO INTERFACE (INTERFACE LAYER - VALIDATOR)
Nhiệm vụ: Chốt chặn dữ liệu bẩn (chuỗi thô người dùng gõ từ bàn phím) ngay tại tầng giao diện trước khi chuyển giao xuống bộ nhớ RAM.
Quy tắc kiến trúc: Hàm trả về True nếu cú pháp sạch, trả về False nếu vi phạm và in trực tiếp thông báo cảnh báo lỗi ra màn hình Console.
"""

import re

def validate_year(year_str: str) -> bool:
    """
    Kiểm tra năm xuất bản hợp lệ (toàn số, từ 1000 đến 2026).
    """
    year_clean = year_str.strip()
    
    # Kiểm tra toàn chữ số
    if not year_clean.isdigit():
        print("[!] Lỗi nhập liệu: Năm xuất bản phải hoàn toàn là các ký tự số.")
        return False
    
    # Kiểm tra khoảng giá trị
    year = int(year_clean)
    if not (1000 <= year <= 2026):
        print(f"[!] Lỗi logic: Năm xuất bản ({year}) không hợp lý. Phải nằm trong khoảng 1000 - 2026.")
        return False
        
    return True

def validate_positive_float(price_str: str) -> bool:
    """
    Kiểm tra giá tiền hợp lệ (> 0.0, ép kiểu float thành công).
    """
    try:
        price = float(price_str.strip())
        if price > 0.0:
            return True
        else:
            print(f"[!] Lỗi logic: Giá tiền ({price}) không hợp lệ. Phải lớn hơn 0.")
            return False
    except ValueError:
        print("[!] Lỗi nhập liệu: Giá tiền phải là một số (ví dụ: 50000 hoặc 50000.5).")
        return False

def validate_book_payload(payload: dict[str, str]) -> bool:
    """
    Kiểm tra toàn bộ biểu mẫu thêm sách.
    - Không trường nào rỗng.
    - registration_number khớp khuôn mẫu ^DKCB-\d{6}$.
    """
    # 1. Duyệt qua để quét lỗi bỏ trống
    for key, value in payload.items():
        if not value.strip():
            print(f"[!] Lỗi biểu mẫu: Trường dữ liệu '{key}' không được để trống.")
            return False
            
    # 2. Quét riêng lỗi định dạng của Số ĐKCB bằng Regex
    reg_num = payload.get("registration_number", "").strip()
    pattern = r"^DKCB-\d{6}$"
    
    if not re.match(pattern, reg_num):
        print("[!] Lỗi định dạng: Số ĐKCB phải theo khuôn mẫu 'DKCB-XXXXXX' (Ví dụ: DKCB-001234).")
        return False
        
    return True
