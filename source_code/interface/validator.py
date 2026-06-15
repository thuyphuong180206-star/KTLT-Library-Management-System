"""
MÀNG LỌC XÁC THỰC CÚ PHÁP ĐẦU VÀO INTERFACE (INTERFACE LAYER - VALIDATOR)
Nhiệm vụ: Chốt chặn dữ liệu bẩn (chuỗi thô người dùng gõ từ bàn phím) ngay tại tầng giao diện trước khi chuyển giao xuống bộ nhớ RAM.
Quy tắc kiến trúc: Hàm trả về True nếu cú pháp sạch, trả về False nếu vi phạm và in trực tiếp thông báo cảnh báo lỗi ra màn hình Console.

Các hàm bắt buộc phải viết trực tiếp:
    - validate_year(year_str: str) -> bool:
        + Xử lý: Kiểm tra chuỗi có hoàn toàn là ký tự số bằng .isdigit(), tiến hành thử nghiệm ép kiểu int, kiểm tra khoảng giá trị toán học: 1000 <= year <= 2026.
    - validate_positive_float(price_str: str) -> bool:
        + Xử lý: Thử nghiệm bọc trong try...except ValueError câu lệnh ép kiểu float(price_str), kiểm tra điều kiện giá trị thu được phải > 0.0.
    - validate_book_payload(payload: dict[str, str]) -> bool:
        + Xử lý: Duyệt qua từ điển biểu mẫu, dùng phương thức `.strip()` loại bỏ khoảng trắng. Chặn lỗi nếu có trường cốt lõi để rỗng `""`.
          Sử dụng thư viện `re` (Regular Expression) đối chiếu trường 'registration_number' phải khớp chính xác khuôn mẫu mã hóa vị trí kho: ^DKCB-\d{6}$.
"""


