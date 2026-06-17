"""
Cấu trúc dữ liệu Danh sách liên kết kép (Doubly Linked List) — Lưu lịch sử giao dịch
Nhiệm vụ: Lưu trữ toàn bộ phiếu mượn/trả theo thứ tự thời gian.
          Giao dịch mới nhất luôn thêm vào cuối (tail), O(1).
Các phương thức:
    - add_transaction(loan_obj)          : Thêm phiếu mới vào cuối, O(1)
    - get_all_transactions()             : Lấy toàn bộ phiếu theo thứ tự thời gian, O(n)
    - get_transactions_by_user(user_id)  : Lọc phiếu của một bạn đọc, O(n)
Import bởi: storage.data_processor, logic.loan_manager, logic.report
"""
