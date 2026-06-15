"""
HẠ TẦNG DANH SÁCH LIÊN KẾT KÉP (DATA STRUCTURE - LOAN DOUBLY LINKED LIST)
Nhiệm vụ: Quản lý toàn bộ lịch sử phiếu mượn trả theo trình tự thời gian.
Hiệu năng: Chèn phần tử mới vào đuôi danh sách đạt tốc độ O(1).

Lớp nội bộ bổ trợ (Private Helper Class):
    - _Node:
        + Thuộc tính: data: Loan (Thực thể phiếu), prev: '_Node | None' (Lưới liên kết ngược), next: '_Node | None' (Lưới liên kết xuôi)

Các thuộc tính của lớp chính TransactionList:
    - _head: '_Node | None'            (Điểm quản lý đầu danh sách liên kết kép)
    - _tail: '_Node | None'            (Điểm quản lý đuôi danh sách liên kết kép, tối ưu chi phí chèn)
    - _size: int                       (Tổng lượt giao dịch lưu trên bộ nhớ RAM)

Các phương thức bắt buộc cài đặt trực tiếp (Cấm dùng cấu trúc dữ liệu list của Python làm hạ tầng cốt lõi):
    - add_transaction(self, loan_obj: Loan) -> None: Đóng gói đối tượng vào _Node, nối trực tiếp vào sau nút _tail hiện hành, cập nhật _tail mới.
    - get_all_transactions(self) -> list[Loan]: Duyệt tuần tự con trỏ từ _head đến _tail, trả về mảng phẳng đối tượng.
    - get_transactions_by_user(self, user_id: str) -> list[Loan]: Quét chuỗi liên kết kép, lọc tất cả phiếu khớp với mã độc giả truyền vào.
"""
