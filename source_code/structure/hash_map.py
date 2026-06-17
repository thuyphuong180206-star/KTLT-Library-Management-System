"""
Cấu trúc dữ liệu Bảng băm (Hash Map) — Lưu trữ danh mục sách
Nhiệm vụ: Lưu trữ và tra cứu sách theo mã sách (book_id) với độ phức tạp O(1).
Cài đặt: Separate Chaining — mỗi bucket là một chuỗi liên kết _Entry, lưu trên CustomList
         (không dùng list có sẵn của Python). Hàm băm tự viết (polynomial hash), không
         dùng hash() có sẵn. Tự động rehash khi load factor vượt ngưỡng 0.75.
Các phương thức:
    - insert(book_id, book_obj)  : Thêm/cập nhật sách, O(1) trung bình
    - search(book_id)            : Tìm sách theo mã, O(1) trung bình
    - delete(book_id)            : Xóa sách khỏi bảng băm, O(1) trung bình
    - get_all_books()            : Lấy toàn bộ sách ra CustomList, O(n)
Import bởi: storage.data_processor, logic.search, logic.sort,
            logic.loan_manager, logic.report, interface.menu
"""
from structure.custom_list import CustomList

_INITIAL_CAPACITY = 16
_LOAD_FACTOR_THRESHOLD = 0.75


class _Entry:
    """Nút trong chuỗi liên kết của một bucket — lưu (book_id, book_obj, next)."""
    __slots__ = ("book_id", "book_obj", "next")

    def __init__(self, book_id, book_obj):
        self.book_id = book_id
        self.book_obj = book_obj
        self.next = None


class BookHashMap:
    """Bảng băm separate chaining lưu sách theo book_id."""

    def __init__(self, capacity: int = _INITIAL_CAPACITY):
        self._capacity = capacity
        self._buckets = CustomList()
        for _ in range(capacity):
            self._buckets.append(None)
        self._count = 0

    def _hash(self, book_id: str) -> int:
        """Polynomial hash tự viết trên chuỗi book_id, không dùng hash() có sẵn."""
        h = 0
        for ch in str(book_id):
            h = (h * 31 + ord(ch)) % self._capacity
        return h

    def insert(self, book_id, book_obj) -> None:
        """Thêm sách mới hoặc cập nhật nếu book_id đã tồn tại. O(1) trung bình."""
        index = self._hash(book_id)
        entry = self._buckets[index]
        while entry is not None:
            if entry.book_id == book_id:
                entry.book_obj = book_obj
                return
            entry = entry.next

        new_entry = _Entry(book_id, book_obj)
        new_entry.next = self._buckets[index]
        self._buckets[index] = new_entry
        self._count += 1

        if self._count / self._capacity > _LOAD_FACTOR_THRESHOLD:
            self._rehash()

    def search(self, book_id):
        """Tìm sách theo book_id. Trả về book_obj hoặc None. O(1) trung bình."""
        index = self._hash(book_id)
        entry = self._buckets[index]
        while entry is not None:
            if entry.book_id == book_id:
                return entry.book_obj
            entry = entry.next
        return None

    def delete(self, book_id) -> bool:
        """Xóa sách theo book_id. Trả về True nếu đã xóa. O(1) trung bình."""
        index = self._hash(book_id)
        entry = self._buckets[index]
        prev = None
        while entry is not None:
            if entry.book_id == book_id:
                if prev is None:
                    self._buckets[index] = entry.next
                else:
                    prev.next = entry.next
                self._count -= 1
                return True
            prev = entry
            entry = entry.next
        return False

    def get_all_books(self) -> CustomList:
        """Lấy toàn bộ sách ra CustomList. O(n)."""
        result = CustomList()
        for i in range(self._capacity):
            entry = self._buckets[i]
            while entry is not None:
                result.append(entry.book_obj)
                entry = entry.next
        return result

    def _rehash(self) -> None:
        """Tăng gấp đôi số bucket và chèn lại toàn bộ entry khi vượt load factor. O(n)."""
        old_capacity = self._capacity
        old_buckets = self._buckets

        self._capacity = old_capacity * 2
        self._buckets = CustomList()
        for _ in range(self._capacity):
            self._buckets.append(None)
        self._count = 0

        for i in range(old_capacity):
            entry = old_buckets[i]
            while entry is not None:
                self.insert(entry.book_id, entry.book_obj)
                entry = entry.next

    def __len__(self) -> int:
        return self._count

    def __repr__(self) -> str:
        return f"BookHashMap(count={self._count}, capacity={self._capacity})"
