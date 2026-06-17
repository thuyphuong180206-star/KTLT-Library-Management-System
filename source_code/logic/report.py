"""
Mô-đun báo cáo thống kê (Report Engine)
Nhiệm vụ: Tổng hợp và trả về dữ liệu báo cáo phục vụ hiển thị.
Ràng buộc: Không chứa lệnh input/print. Trả về dữ liệu thô để interface hiển thị.
Các hàm:
    - get_borrowing_loans(dll, hash_map)
        Lấy tất cả phiếu có status="borrowing" kèm thông tin tên sách.
        Phục vụ: "Danh sách sách đang được mượn".
        Trả về: list[dict]

    - get_overdue_loans(dll, hash_map, user_array)
        Lấy phiếu status="borrowing" mà due_date < ngày hôm nay.
        Tự động cập nhật status → "overdue" ngay khi phát hiện.
        Kèm số ngày quá hạn và tiền phạt tạm tính.
        Phục vụ: "Danh sách sách quá hạn".
        Trả về: list[dict]

    - get_top5_books(hash_map, pq)
        Đẩy toàn bộ sách có borrow_count > 0 vào PriorityQueue.
        Gọi peek_top_n(5) lấy top 5 sách mượn nhiều nhất.
        Phục vụ: "Top 5 sách được mượn nhiều nhất".
        Trả về: list[Book]
Import: structure.priority_queue.PriorityQueue, logic.loan_manager
Import bởi: interface.menu
"""
from datetime import date
from structure.custom_list import CustomList
from logic import loan_manager


def get_borrowing_loans(dll, hash_map):
    """Lấy tất cả phiếu đang mượn kèm tên sách. Trả về CustomList[dict]."""
    result = CustomList()
    for loan in dll.get_all_transactions():
        if loan.status == "borrowing":
            book = hash_map.search(loan.book_id)
            result.append({
                "loan_id": loan.loan_id,
                "user_id": loan.user_id,
                "book_id": loan.book_id,
                "title": book.title if book else "Khong ro",
                "borrow_date": loan.borrow_date,
                "due_date": loan.due_date,
            })
    return result


def get_overdue_loans(dll, hash_map, user_array):
    """Lấy phiếu quá hạn, tự cập nhật status, kèm số ngày trễ và phí tạm tính. Trả về CustomList[dict]."""
    result = CustomList()
    today = date.today()
    for loan in dll.get_all_transactions():
        if loan.status == "borrowing" and loan.due_date is not None and loan.due_date < today:
            loan.status = "overdue"

        if loan.status == "overdue":
            user = user_array.get_by_id(loan.user_id)
            book = hash_map.search(loan.book_id)
            days_overdue = (today - loan.due_date).days if loan.due_date else 0
            fee = loan_manager.calculate_overdue_fee(loan, user) if user else 0.0
            result.append({
                "loan_id": loan.loan_id,
                "user_id": loan.user_id,
                "book_id": loan.book_id,
                "title": book.title if book else "Khong ro",
                "days_overdue": days_overdue,
                "temp_fee": fee,
            })
    return result


def get_top5_books(hash_map, pq):
    """Lấy top 5 sách mượn nhiều nhất. Trả về CustomList[Book]."""
    for book in hash_map.get_all_books():
        if book.borrow_count > 0:
            pq.enqueue(book)
    return pq.peek_top_n(5)
