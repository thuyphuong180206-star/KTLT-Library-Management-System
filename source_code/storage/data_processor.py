"""
Mô-đun đọc/ghi cơ sở dữ liệu CSV (Storage Layer)
Nhiệm vụ: Nạp dữ liệu từ file CSV lên các cấu trúc dữ liệu trên RAM khi khởi động,
          và ghi toàn bộ trạng thái RAM xuống CSV sau mỗi thao tác thay đổi dữ liệu.
Ràng buộc:
    - Tầng duy nhất được phép đọc/ghi file trong toàn hệ thống.
    - Không chứa logic nghiệp vụ hay hiển thị giao diện.
    - Tự parse CSV thủ công bằng csv.reader, không dùng thư viện json/pandas.
    - Nếu books.csv, loans.csv hoặc waiting_requests.csv không tồn tại:
      tự tạo file mới chỉ có header.
    - Nếu users.csv không tồn tại: tự tạo file mới với header và ghi sẵn
      tài khoản admin mặc định để đảm bảo hệ thống luôn đăng nhập được.
    - Nếu dòng dữ liệu lỗi: ghi vào system_error.log, bỏ qua dòng đó và tiếp tục.
Các hàm:
    - load_system_data(books_path, users_path, loans_path, waiting_path)
        → tuple(BookHashMap, TransactionList, UserArray, WaitingQueue)
    - save_system_data(hash_map, dll, user_array, waiting_queue,
                       books_path, users_path, loans_path, waiting_path)
        → None
Import: objects.books.Book, objects.users.User, objects.loans.Loan,
        objects.requests.BorrowRequest,
        structure.hash_map.BookHashMap,
        structure.doubly_linked_list.TransactionList,
        structure.user_array.UserArray,
        structure.waiting_queue.WaitingQueue
Import bởi: main
"""

import csv
import os
from datetime import datetime

from objects.books import Book
from objects.users import User
from objects.loans import Loan
from objects.requests import BorrowRequest
from structure.hash_map import BookHashMap
from structure.doubly_linked_list import TransactionList
from structure.user_array import UserArray
from structure.waiting_queue import WaitingQueue


# ------------------------------------------------------------------ #
# Hằng số — Header chuẩn cho từng file CSV                           #
# ------------------------------------------------------------------ #

BOOKS_HEADER   = ["book_id", "title", "author", "genre", "publisher",
                  "quantity", "status", "borrow_count"]
USERS_HEADER   = ["user_id", "fullname", "password", "role", "reader_type"]
LOANS_HEADER   = ["loan_id", "user_id", "book_id", "borrow_date",
                  "due_date", "return_date", "status", "overdue_fee"]
WAITING_HEADER = ["request_id", "user_id", "book_id", "request_date"]

# Tài khoản admin mặc định — ghi sẵn khi users.csv chưa tồn tại
ADMIN_DEFAULT  = {
    "user_id":     "admin",
    "fullname":    "Admin Thu Vien",
    "password":    "admin123",
    "role":        "admin",
    "reader_type": "",
}


# ------------------------------------------------------------------ #
# Helper — Ghi log lỗi ra system_error.log                           #
# ------------------------------------------------------------------ #

def _log_error(log_path: str, filename: str, row, error: Exception) -> None:
    """Ghi thông tin dòng lỗi vào system_error.log."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(
            f"[{timestamp}] File: {filename} "
            f"| Row: {row} "
            f"| Error: {error}\n"
        )


# ------------------------------------------------------------------ #
# Helper — Đọc file CSV thành list dict                              #
# ------------------------------------------------------------------ #

def _read_csv(filepath: str, log_path: str) -> list:
    """
    Đọc file CSV, trả về list các dict (mỗi dict là một dòng dữ liệu).
    Dòng trống hoặc lỗi sẽ bị bỏ qua và ghi vào log.
    """
    rows = []
    with open(filepath, "r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        headers = [h.strip() for h in next(reader)]
        for row in reader:
            try:
                if not any(cell.strip() for cell in row):
                    continue  # bỏ qua dòng trống
                row_dict = {}
                for i in range(len(headers)):
                    row_dict[headers[i]] = row[i].strip() if i < len(row) else ""
                rows.append(row_dict)
            except (ValueError, IndexError) as e:
                _log_error(log_path, filepath, row, e)
                continue
    return rows


# ------------------------------------------------------------------ #
# Helper — Tạo file CSV mới với header                               #
# ------------------------------------------------------------------ #

def _create_csv(filepath: str, header: list,
                default_row: dict = None) -> None:
    """
    Tạo file CSV mới với dòng header chuẩn.
    Nếu có default_row: ghi thêm một dòng dữ liệu mặc định.
    """
    dir_name = os.path.dirname(filepath)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    with open(filepath, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        if default_row:
            writer.writerow([default_row.get(h, "") for h in header])


# ------------------------------------------------------------------ #
# Helper — Ghi list dict xuống file CSV                              #
# ------------------------------------------------------------------ #

def _write_csv(filepath: str, header: list, rows: list) -> None:
    """Ghi đè toàn bộ dữ liệu xuống file CSV theo header chuẩn."""
    with open(filepath, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for row_dict in rows:
            writer.writerow([row_dict.get(h, "") for h in header])


# ------------------------------------------------------------------ #
# Hàm chính 1: load_system_data                                      #
# ------------------------------------------------------------------ #

def load_system_data(books_path: str, users_path: str,
                     loans_path: str, waiting_path: str) -> tuple:
    """
    Nạp toàn bộ dữ liệu từ 4 file CSV lên RAM.

    Args:
        books_path   : Đường dẫn tới books.csv
        users_path   : Đường dẫn tới users.csv
        loans_path   : Đường dẫn tới loans.csv
        waiting_path : Đường dẫn tới waiting_requests.csv

    Returns:
        tuple(BookHashMap, TransactionList, UserArray, WaitingQueue)
    """
    log_path = os.path.join(os.path.dirname(books_path), "system_error.log")

    hash_map      = BookHashMap()
    dll           = TransactionList()
    user_array    = UserArray()
    waiting_queue = WaitingQueue()

    # --- Nạp books.csv → BookHashMap ---
    try:
        for row in _read_csv(books_path, log_path):
            try:
                book = Book.from_dict(row)
                hash_map.insert(book.book_id, book)
            except (ValueError, KeyError) as e:
                _log_error(log_path, books_path, row, e)
    except FileNotFoundError:
        _create_csv(books_path, BOOKS_HEADER)

    # --- Nạp users.csv → UserArray ---
    try:
        for row in _read_csv(users_path, log_path):
            try:
                user = User.from_dict(row)
                user_array.append(user)
            except (ValueError, KeyError) as e:
                _log_error(log_path, users_path, row, e)
    except FileNotFoundError:
        # Tạo file mới + ghi sẵn tài khoản admin mặc định
        _create_csv(users_path, USERS_HEADER, ADMIN_DEFAULT)
        user_array.append(User.from_dict(ADMIN_DEFAULT))

    # --- Nạp loans.csv → TransactionList ---
    try:
        for row in _read_csv(loans_path, log_path):
            try:
                loan = Loan.from_dict(row)
                dll.add_transaction(loan)
            except (ValueError, KeyError) as e:
                _log_error(log_path, loans_path, row, e)
    except FileNotFoundError:
        _create_csv(loans_path, LOANS_HEADER)

    # --- Nạp waiting_requests.csv → WaitingQueue ---
    try:
        for row in _read_csv(waiting_path, log_path):
            try:
                request = BorrowRequest.from_dict(row)
                waiting_queue.enqueue(request)
            except (ValueError, KeyError) as e:
                _log_error(log_path, waiting_path, row, e)
    except FileNotFoundError:
        _create_csv(waiting_path, WAITING_HEADER)

    return hash_map, dll, user_array, waiting_queue


# ------------------------------------------------------------------ #
# Hàm chính 2: save_system_data                                      #
# ------------------------------------------------------------------ #

def save_system_data(hash_map: BookHashMap,
                     dll: TransactionList,
                     user_array: UserArray,
                     waiting_queue: WaitingQueue,
                     books_path: str,
                     users_path: str,
                     loans_path: str,
                     waiting_path: str) -> None:
    """
    Ghi toàn bộ trạng thái RAM xuống 4 file CSV.
    Ghi đè hoàn toàn — đảm bảo CSV luôn đồng bộ với RAM.

    Args:
        hash_map      : BookHashMap chứa toàn bộ sách
        dll           : TransactionList chứa toàn bộ phiếu mượn/trả
        user_array    : UserArray chứa toàn bộ tài khoản
        waiting_queue : WaitingQueue chứa toàn bộ yêu cầu chờ
        books_path    : Đường dẫn tới books.csv
        users_path    : Đường dẫn tới users.csv
        loans_path    : Đường dẫn tới loans.csv
        waiting_path  : Đường dẫn tới waiting_requests.csv
    """
    # Ghi books.csv
    _write_csv(
        books_path, BOOKS_HEADER,
        [book.to_dict() for book in hash_map.get_all_books()]
    )

    # Ghi users.csv
    _write_csv(
        users_path, USERS_HEADER,
        [user.to_dict() for user in user_array.get_all()]
    )

    # Ghi loans.csv
    _write_csv(
        loans_path, LOANS_HEADER,
        [loan.to_dict() for loan in dll.get_all_transactions()]
    )

    # Ghi waiting_requests.csv
    _write_csv(
        waiting_path, WAITING_HEADER,
        [req.to_dict() for req in waiting_queue.to_list()]
    )
