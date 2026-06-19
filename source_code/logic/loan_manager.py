"""
Mô-đun điều phối nghiệp vụ mượn/trả sách (Loan Manager)
Nhiệm vụ: Xử lý toàn bộ logic nghiệp vụ mượn sách, trả sách và tính tiền phạt.
Ràng buộc: Không chứa lệnh input/print. Mỗi hàm trả về tuple/giá trị thông báo
kết quả theo đúng mô tả riêng ở từng hàm bên dưới.
Hằng số phạt:
    OVERDUE_FEE = {"student": 2000, "lecturer": 1000}  # VNĐ/ngày
Các hàm:
    - process_borrow(hash_map, dll, user_array, user_id, book_id, borrow_date=None)
        Xử lý mượn sách. Kiểm tra theo thứ tự:
            1. User tồn tại không?
            2. Sách tồn tại không?
            3. User có đang nợ phiếu "overdue" không? → từ chối
            4. User có đang mượn quá borrow_limit không? → từ chối
            5. User có đang mượn chính cuốn này không? → từ chối
            6. Sách có đang lưu hành không (status == "active")? → từ chối nếu "inactive"
            7. Sách còn trong kho không (quantity > 0)?
        Nếu hợp lệ: tạo Loan (due_date tự tính), thêm vào DLL, giảm quantity đi 1, tăng borrow_count lên 1.
        borrow_date (tùy chọn): ngày mượn cụ thể, mặc định None → dùng ngày hệ thống
          (date.today()). Cho phép mô phỏng mượn vào một ngày bất kỳ khi viết test,
          không phải đợi thời gian thực trôi qua để test quá hạn.
        Trả về: (bool, str)
        Dùng khi: đọc giả đến mượn sách trực tiếp (luồng bình thường ở interface.menu),
        và được process_return() gọi lại nội bộ để thử cho người trong waiting_queue mượn ngay.

    - process_return(hash_map, dll, user_array, waiting_queue, user_id, book_id, return_date=None)
        Xử lý trả sách. Quy trình:
            1. User tồn tại không? Sách tồn tại không? → không hợp lệ thì từ chối.
            2. Tìm phiếu mượn gần nhất (status="borrowing" hoặc "overdue") khớp user_id + book_id.
               Không tìm thấy → từ chối (đọc giả này chưa mượn cuốn này).
            3. Tính tiền phạt = số ngày quá hạn (nếu trả sau due_date) × đơn giá theo reader_type.
            4. Cập nhật phiếu: return_date = hôm nay, status = "returned", overdue_fee = tiền phạt.
            5. Tăng quantity sách lên 1 — phải tăng trước vì sách đã thực sự về kho,
               và bước 6 cần có hàng để cho mượn lại được.
            6. Ưu tiên hàng chờ: duyệt waiting_queue theo đúng thứ tự FIFO, bỏ qua các
               yêu cầu của book_id khác; gặp yêu cầu đầu tiên đúng book_id thì gọi
               process_borrow() thử ngay cho người đó, dùng borrow_date = return_date
               (sách trả và giao cho người chờ được tính là cùng một ngày).
                 - Mượn được (còn đủ điều kiện): rút yêu cầu khỏi hàng đợi bằng
                   waiting_queue.remove_match(), dừng vòng lặp — sách coi như đã có
                   chủ mới, không "lọt" ra ngoài cho người tự do đến mượn.
                 - Không đủ điều kiện (vd: đang nợ overdue): bỏ qua, người đó vẫn giữ
                   chỗ trong hàng đợi để được xét lại ở lượt trả sách kế tiếp, sang
                   xét người tiếp theo.
                 - Không ai trong hàng đợi khớp book_id (hoặc hàng đợi rỗng): sách ở
                   lại kho, ai đến mượn trước cũng được.
        return_date (tùy chọn): ngày trả cụ thể, mặc định None → dùng ngày hệ thống
          (date.today()). Cho phép mô phỏng trả sách vào một ngày bất kỳ khi viết
          test (vd. trả sau due_date để kiểm tra tính tiền phạt).
        Trả về: (bool, str, float) — (thành công, thông báo, tiền phạt)

    - calculate_overdue_fee(loan, user, check_date=None)
        Tính tiền phạt tạm tính cho một phiếu CHƯA trả (status còn "borrowing"/"overdue").
        check_date (tùy chọn): ngày dùng để so sánh với due_date, mặc định None →
          dùng ngày hệ thống. Cho phép giả định một ngày cụ thể khi viết test.
        Dùng khi: hiển thị phí quá hạn ước tính real-time cho đọc giả/admin xem
        (vd. report.get_overdue_loans) — process_return tự tính phạt riêng tại thời
        điểm trả, không gọi lại hàm này.
        Trả về: float (VNĐ)

    - is_book_on_loan(dll, book_id)
        Kiểm tra sách có đang được mượn không, bằng cách duyệt DLL tìm phiếu có
        book_id khớp và status="borrowing" hoặc "overdue".
        Dùng khi: admin muốn xóa một cuốn sách khỏi hệ thống — phải kiểm tra sách
        không còn ai mượn trước khi cho xóa (interface.menu).
        Trả về: bool

    - add_to_waiting_queue(waiting_queue, user_id, book_id, request_date=None)
        Thêm yêu cầu chờ mượn vào cuối WaitingQueue khi sách hết kho.
        Kiểm tra user chưa có trong hàng chờ của book_id này trước khi thêm.
        request_date (tùy chọn): ngày đăng ký chờ cụ thể, mặc định None → dùng
          ngày hệ thống (date.today()). Cho phép mô phỏng đăng ký chờ vào một
          ngày bất kỳ khi viết test.
        Dùng khi: đọc giả muốn mượn nhưng process_borrow() đã từ chối vì hết kho
        (quantity == 0) — đăng ký chờ để được tự động xét mượn ngay ở lượt
        process_return() kế tiếp của đúng cuốn sách này.
        Trả về: (bool, str) — (thành công, thông báo)
Import: objects.loans.Loan, objects.requests.BorrowRequest
Import bởi: interface.menu
"""
from datetime import date, timedelta
from objects.loans import Loan
from objects.requests import BorrowRequest

OVERDUE_FEE = {"student": 2000, "lecturer": 1000}  # VNĐ/ngày


def process_borrow(hash_map, dll, user_array, user_id, book_id, borrow_date=None):
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

    borrow_date = borrow_date or date.today()
    due_date = borrow_date + timedelta(days=user.borrow_duration)
    loan_id = f"L{dll.size + 1:03d}"
    new_loan = Loan(loan_id, user_id, book_id, borrow_date, due_date=due_date, status="borrowing")

    dll.add_transaction(new_loan)
    book.quantity -= 1
    book.borrow_count += 1

    return True, f"Muon sach thanh cong. Han tra: {due_date}."


def process_return(hash_map, dll, user_array, waiting_queue, user_id, book_id, return_date=None):
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

    return_date = return_date or date.today()
    fee = 0.0
    if return_date > target_loan.due_date:
        days_overdue = (return_date - target_loan.due_date).days
        fee = days_overdue * OVERDUE_FEE.get(user.reader_type, 0)

    target_loan.return_date = return_date
    target_loan.status = "returned"
    target_loan.overdue_fee = fee
    book.quantity += 1

    serve_waiting_queue(hash_map, dll, user_array, waiting_queue, book_id, serve_date=return_date)

    return True, "Tra sach thanh cong.", fee


def serve_waiting_queue(hash_map, dll, user_array, waiting_queue, book_id, serve_date=None):
    """Uu tien nguoi doi lau nhat cho dung book_id nay, theo FIFO, cho den khi het
    ton kho hoac het nguoi cho khop. Goi moi khi quantity cua mot sach tang len,
    du la do tra sach hay do admin nhap them sach (sua thong tin sach)."""
    book = hash_map.search(book_id)
    while book is not None and book.quantity > 0:
        served = False
        for request in waiting_queue.to_list():
            if request.book_id != book_id:
                continue
            success, _ = process_borrow(hash_map, dll, user_array, request.user_id, book_id, borrow_date=serve_date)
            if success:
                waiting_queue.remove_match(lambda r: r.request_id == request.request_id)
                served = True
                break
        if not served:
            break


def calculate_overdue_fee(loan, user, check_date=None):
    """Tính tiền phạt tạm tính cho phiếu chưa trả. Trả về float (VNĐ)."""
    if loan.status not in ("borrowing", "overdue") or loan.due_date is None:
        return 0.0
    check_date = check_date or date.today()
    if check_date <= loan.due_date:
        return 0.0
    days_overdue = (check_date - loan.due_date).days
    return days_overdue * OVERDUE_FEE.get(user.reader_type, 0)


def is_book_on_loan(dll, book_id):
    """Kiểm tra sách có đang được mượn không. Trả về bool."""
    for loan in dll.get_all_transactions():
        if loan.book_id == book_id and loan.status in ("borrowing", "overdue"):
            return True
    return False


def add_to_waiting_queue(waiting_queue, user_id, book_id, request_date=None):
    """Thêm yêu cầu chờ mượn vào cuối WaitingQueue. Trả về (bool, str)."""
    for request in waiting_queue.to_list():
        if request.user_id == user_id and request.book_id == book_id:
            return False, "Ban da co trong hang doi cho sach nay."

    request_id = f"WR{waiting_queue.size + 1:03d}"
    request_date = request_date or date.today()
    new_request = BorrowRequest(request_id, user_id, book_id, request_date)
    waiting_queue.enqueue(new_request)
    return True, "Da them vao hang doi cho muon sach."
