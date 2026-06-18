"""
Mô-đun nạp dữ liệu kiểm thử dùng chung (Test Data Loader)
Nhiệm vụ: Đọc 4 file CSV trong tests/data_test/ (books, users, loans, waiting_requests)
          và dựng thành đúng các cấu trúc dữ liệu thật của hệ thống — dùng chung cho
          mọi file test trong thư mục tests/.
Ràng buộc: Không phụ thuộc storage.data_processor (storage chỉ đọc data/ thật).
Các hàm:
    - load_books()           : Trả về BookHashMap, nạp từ tests/data_test/books.csv
    - load_users()            : Trả về UserArray, nạp từ tests/data_test/users.csv
    - load_loans()             : Trả về TransactionList, nạp từ tests/data_test/loans.csv
    - load_waiting_requests() : Trả về WaitingQueue, nạp từ tests/data_test/waiting_requests.csv
Import: objects.books.Book, objects.users.User, objects.loans.Loan, objects.requests.BorrowRequest,
        structure.hash_map.BookHashMap, structure.user_array.UserArray,
        structure.doubly_linked_list.TransactionList, structure.waiting_queue.WaitingQueue
"""
import csv
import os

from objects.books import Book
from objects.users import User
from objects.loans import Loan
from objects.requests import BorrowRequest
from structure.hash_map import BookHashMap
from structure.user_array import UserArray
from structure.doubly_linked_list import TransactionList
from structure.waiting_queue import WaitingQueue

_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data_test")


def _read_csv(filename):
    path = os.path.join(_DATA_DIR, filename)
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_books():
    """Nạp tests/data_test/books.csv. Trả về BookHashMap."""
    hash_map = BookHashMap()
    for row in _read_csv("books.csv"):
        book = Book.from_dict(row)
        hash_map.insert(book.book_id, book)
    return hash_map


def load_users():
    """Nạp tests/data_test/users.csv. Trả về UserArray."""
    user_array = UserArray()
    for row in _read_csv("users.csv"):
        user_array.append(User.from_dict(row))
    return user_array


def load_loans():
    """Nạp tests/data_test/loans.csv. Trả về TransactionList."""
    dll = TransactionList()
    for row in _read_csv("loans.csv"):
        dll.add_transaction(Loan.from_dict(row))
    return dll


def load_waiting_requests():
    """Nạp tests/data_test/waiting_requests.csv. Trả về WaitingQueue."""
    waiting_queue = WaitingQueue()
    for row in _read_csv("waiting_requests.csv"):
        waiting_queue.enqueue(BorrowRequest.from_dict(row))
    return waiting_queue
