"""
Mô-đun điều phối nghiệp vụ mượn/trả sách (Loan Manager)
Nhiệm vụ: Xử lý toàn bộ logic nghiệp vụ mượn sách, trả sách và tính tiền phạt.
Ràng buộc: Không chứa lệnh input/print. Trả về tuple (bool, str) thông báo kết quả.
Hằng số phạt:
    OVERDUE_FEE = {"student": 2000, "lecturer": 1000}  # VNĐ/ngày
Các hàm:
    - process_borrow(hash_map, dll, user_array, user_id, book_id)
        Xử lý mượn sách. Kiểm tra theo thứ tự:
            1. User tồn tại không?
            2. Sách tồn tại không?
            3. User có đang nợ phiếu "overdue" không? → từ chối
            4. User có đang mượn quá borrow_limit không? → từ chối
            5. User có đang mượn chính cuốn này không? → từ chối
            6. Sách có đang lưu hành không (status == "active")? → từ chối nếu "inactive"
7. Sách còn trong kho không (quantity > 0)? 
       Nếu hợp lệ: tạo Loan (due_date tự tính), thêm vào DLL, giảm quantity đi 1, tăng borrow_count lên 1. 
        Trả về: (bool, str)
    - process_return(hash_map, dll, user_array, waiting_queue, user_id, book_id)
        Xử lý trả sách.
        Tìm phiếu gần nhất có status="borrowing" hoặc status="overdue" khớp user_id + book_id
        Tính tiền phạt = số ngày quá hạn × đơn giá theo reader_type.
        Cập nhật phiếu: return_date, status="returned", overdue_fee.
        Tăng quantity sách lên 1, rồi ưu tiên xét cho mượn ngay theo đúng thứ tự
        trong waiting_queue (người đợi lâu nhất, còn đủ điều kiện mượn, được nhận sách
        trước người tự do đến mượn). Người không còn đủ điều kiện vẫn giữ chỗ trong hàng đợi.
        Trả về: (bool, str, float) — (thành công, thông báo, tiền phạt)
    - calculate_overdue_fee(loan, user)
        Tính tiền phạt tạm tính cho phiếu chưa trả.
        Dùng cho tính năng xem phí real-time của user.
        Trả về: float (VNĐ)
    - is_book_on_loan(dll, book_id)
    - add_to_waiting_queue(waiting_queue, user_id, book_id)
        Thêm yêu cầu chờ mượn vào cuối WaitingQueue khi sách hết kho.
        Kiểm tra user chưa có trong hàng chờ của book_id này trước khi thêm.
        Trả về: (bool, str) — (thành công, thông báo)
    - check_waiting_queue(waiting_queue, book_id)
        Kiểm tra có ai đang chờ mượn cuốn sách này không.
        Gọi sau process_return() để thông báo cho admin.
        Trả về: str | None — user_id đầu hàng chờ, hoặc None nếu không có ai
Kiểm tra sách có đang được mượn không bằng cách duyệt DLL.
Tìm phiếu có book_id khớp và status="borrowing" hoặc "overdue".
Dùng cho chức năng xóa sách ở interface.menu.
Trả về: bool 
Import: logic.search, objects.loans.Loan
Import bởi: interface.menu
"""
from datetime import date, timedelta
from objects.loans import Loan
from objects.requests import BorrowRequest

OVERDUE_FEE = {"student": 2000, "lecturer": 1000}  # VNĐ/ngày


def process_borrow(hash_map, dll, user_array, user_id, book_id):
    """Xử lý mượn sách theo đúng 7 bước kiểm tra. Trả về (bool, str)."""
    user = user_array.get_by_id(user_id)
    if user is None:
        return False, f"Khong tim thay doc gia co ma {user_id}."

    book = hash_map.search(book_id)
    if book is None:
        return False, f"Khong tim thay sach co ma {book_id}."

    user_loans = dll.get_transactions_by_user(user_id)

    for loan in user_loans:
        if loan.status == "overdue":
            return False, "Ban dang co phieu qua han chua tra, khong the muon them sach."

    borrowing_count = 0
    for loan in user_loans:
        if loan.status in ("borrowing", "overdue"):
            borrowing_count += 1
    if borrowing_count >= user.borrow_limit:
        return False, f"Ban da muon toi da {user.borrow_limit} cuon, khong the muon them."

    for loan in user_loans:
        if loan.book_id == book_id and loan.status in ("borrowing", "overdue"):
            return False, "Ban dang muon chinh cuon sach nay, chua tra."

    if book.status != "active":
        return False, "Sach nay da ngung luu hanh, khong the muon."

    if book.quantity <= 0:
        return False, "Sach da het trong kho."

    borrow_date = date.today()
    due_date = borrow_date + timedelta(days=user.borrow_duration)
    loan_id = f"L{dll.size + 1:03d}"
    new_loan = Loan(loan_id, user_id, book_id, borrow_date, due_date=due_date, status="borrowing")

    dll.add_transaction(new_loan)
    book.quantity -= 1
    book.borrow_count += 1

    return True, f"Muon sach thanh cong. Han tra: {due_date}."


def process_return(hash_map, dll, user_array, waiting_queue, user_id, book_id):
    """Xử lý trả sách — tìm phiếu gần nhất, tính phạt, cập nhật, ưu tiên hàng chờ. Trả về (bool, str, float)."""
    user = user_array.get_by_id(user_id)
    if user is None:
        return False, f"Khong tim thay doc gia co ma {user_id}.", 0.0

    book = hash_map.search(book_id)
    if book is None:
        return False, f"Khong tim thay sach co ma {book_id}.", 0.0

    target_loan = None
    for loan in dll.get_transactions_by_user(user_id):
        if loan.book_id == book_id and loan.status in ("borrowing", "overdue"):
            target_loan = loan  # duyệt hết để lấy phiếu gần nhất (cuối cùng khớp)

    if target_loan is None:
        return False, "Khong tim thay phieu muon dang mo cho doc gia va sach nay.", 0.0

    return_date = date.today()
    fee = 0.0
    if return_date > target_loan.due_date:
        days_overdue = (return_date - target_loan.due_date).days
        fee = days_overdue * OVERDUE_FEE.get(user.reader_type, 0)

    target_loan.return_date = return_date
    target_loan.status = "returned"
    target_loan.overdue_fee = fee
    book.quantity += 1

    # Uu tien nguoi doi lau nhat cho dung book_id nay, neu con du dieu kien muon
    for request in waiting_queue.to_list():
        if request.book_id != book_id:
            continue
        success, _ = process_borrow(hash_map, dll, user_array, request.user_id, book_id)
        if success:
            waiting_queue.remove_match(lambda r: r.request_id == request.request_id)
            break

    return True, "Tra sach thanh cong.", fee


def calculate_overdue_fee(loan, user):
    """Tính tiền phạt tạm tính cho phiếu chưa trả. Trả về float (VNĐ)."""
    if loan.status not in ("borrowing", "overdue") or loan.due_date is None:
        return 0.0
    today = date.today()
    if today <= loan.due_date:
        return 0.0
    days_overdue = (today - loan.due_date).days
    return days_overdue * OVERDUE_FEE.get(user.reader_type, 0)


def is_book_on_loan(dll, book_id):
    """Kiểm tra sách có đang được mượn không. Trả về bool."""
    for loan in dll.get_all_transactions():
        if loan.book_id == book_id and loan.status in ("borrowing", "overdue"):
            return True
    return False


def add_to_waiting_queue(waiting_queue, user_id, book_id):
    """Thêm yêu cầu chờ mượn vào cuối WaitingQueue. Trả về (bool, str)."""
    for request in waiting_queue.to_list():
        if request.user_id == user_id and request.book_id == book_id:
            return False, "Ban da co trong hang doi cho sach nay."

    request_id = f"WR{waiting_queue.size + 1:03d}"
    new_request = BorrowRequest(request_id, user_id, book_id, date.today())
    waiting_queue.enqueue(new_request)
    return True, "Da them vao hang doi cho muon sach."


def check_waiting_queue(waiting_queue, book_id):
    """Kiểm tra có ai đang chờ mượn cuốn sách này không. Trả về user_id hoặc None."""
    for request in waiting_queue.to_list():
        if request.book_id == book_id:
            return request.user_id
    return None
