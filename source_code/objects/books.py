"""
MÔ-ĐUN THỰC THỂ ĐỐI TƯỢNG SÁCH (OBJECT LAYER - BOOK ENTITY)
Nhiệm vụ: Định nghĩa lớp Book để đóng gói cấu trúc thông tin của một đầu sách trên RAM.
Ràng buộc: Toàn bộ thuộc tính phải để ở phạm vi Private (__), chỉ tương tác qua hệ thống Getters/Setters.

Các thuộc tính bảo vệ (Private Attributes):
    - __book_id: str                   (Mã định danh duy nhất, định dạng chuẩn Regex: ^B\d{5}$)
    - __title: str                     (Tên/Tiêu đề đầu sách, chuỗi không rỗng)
    - __author: str                    (Họ tên tác giả)
    - __publisher: str                 (Tên Nhà xuất bản)
    - __publish_year: int              (Năm xuất bản vật lý, điều kiện: 1000 <= value <= 2026)
    - __price: float                   (Giá bìa niêm yết, điều kiện: value > 0.0)
    - __registration_number: str       (Số đăng ký cá biệt định vị kho, định dạng Regex: ^DKCB-\d{6}$)
    - __quantity: int                  (Số lượng bản sách hiện còn trên kệ kệ kho, điều kiện: value >= 0)
    - __status: str                    (Trạng thái kho vật lý, tập đóng giá trị: "available", "borrowed", "unavailable")
    - __borrow_count: int              (Tổng số lượt mượn tích lũy từ trước đến nay, điều kiện: value >= 0)

Hệ thống phương thức bắt buộc cài đặt trực tiếp (Không dùng Stub):
    - __init__(self, book_id: str, title: str, author: str, publisher: str, publish_year: int, price: float, registration_number: str, quantity: int, status: str, borrow_count: int) -> None
    - get_book_id(self) -> str
    - get_title(self) -> str
    - get_author(self) -> str
    - get_publisher(self) -> str
    - get_publish_year(self) -> int
    - get_price(self) -> float
    - get_registration_number(self) -> str
    - get_quantity(self) -> int
    - get_status(self) -> str
    - get_borrow_count(self) -> int
    - set_title(self, title: str) -> None
    - set_author(self, author: str) -> None
    - set_publisher(self, publisher: str) -> None
    - set_publish_year(self, year: int) -> None
    - set_price(self, price: float) -> None
    - set_registration_number(self, reg_num: str) -> None
    - set_quantity(self, qty: int) -> None
    - set_status(self, status: str) -> None
    - set_borrow_count(self, count: int) -> None
    - to_dict(self) -> dict[str, Any]:
        + Không nhận tham số. Trả về dict chứa 10 khóa chuỗi (tên tương ứng thuộc tính, bỏ tiền tố __).
    - from_dict(cls, data: dict[str, Any]) -> 'Book' (Classmethod):
        + Nhận dict dữ liệu chuỗi từ file CSV, thực hiện ép kiểu an toàn và return đối tượng Book mới.
"""
