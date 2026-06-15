"""
MÔ-ĐUN THỰC THỂ PHIẾU MƯỢN TRẢ (OBJECT LAYER - LOAN ENTITY)
Nhiệm vụ: Định nghĩa lớp Loan lưu vết thông tin chi tiết của một giao dịch mượn sách thư viện.

Các thuộc tính bảo vệ (Private Attributes):
    - __loan_id: str                   (Mã giao dịch độc nhất, chuẩn Regex: ^L\d{5}$)
    - __user_id: str                   (Mã bạn đọc mượn sách, liên kết ngoài với User.__user_id)
    - __book_id: str                   (Mã đầu sách được mượn, liên kết ngoài với Book.__book_id)
    - __borrow_date: str               (Ngày hệ thống kích hoạt mượn sách, định dạng chuỗi: YYYY-MM-DD)
    - __return_date: str               (Ngày trả thực tế, chuỗi YYYY-MM-DD, mặc định rỗng "" nếu đang mượn)
    - __status: str                    (Trạng thái phiếu giao dịch, tập đóng: "borrowing" hoặc "returned")
    - __overdue_fee: float             (Tiền phạt quá hạn tạm tính hoặc thực tế khi tất toán, điều kiện: >= 0.0)

Hệ thống phương thức bắt buộc cài đặt trực tiếp:
    - __init__(self, loan_id: str, user_id: str, book_id: str, borrow_date: str, return_date: str, status: str, overdue_fee: float) -> None
    - Getters/Setters đầy đủ cho 7 thuộc tính ẩn trên (Cấm can thiệp trực tiếp biến ngoài lớp).
    - to_dict(self) -> dict[str, Any]: Đóng gói thuộc tính phiếu mượn sang dict để tầng Storage đồng bộ.
    - from_dict(cls, data: dict[str, Any]) -> 'Loan' (Classmethod): Phục hồi đối tượng phiếu từ bản ghi CSV thô.
"""