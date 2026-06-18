"""
Cấu trúc dữ liệu Mảng người dùng (User Array) — Lưu danh sách bạn đọc
Nhiệm vụ: Lưu trữ danh sách tài khoản người dùng trên RAM, tra cứu/xóa theo user_id.
Cài đặt: Xây trên nền CustomList (mảng động tự quản lý capacity) — không dùng list có
         sẵn của Python, chỉ thêm các phương thức tra cứu chuyên biệt cho User.
Các phương thức:
    - append(user_obj)         : Thêm người dùng vào cuối mảng, O(1)
    - get_by_id(user_id)       : Tìm người dùng theo mã, O(n)
    - get_all()                : Lấy toàn bộ người dùng ra CustomList, O(n)
    - remove_by_id(user_id)    : Xóa người dùng theo mã, O(n)
    - size()                   : Trả về số lượng người dùng hiện có, O(1)
    - is_empty()               : Kiểm tra mảng người dùng có rỗng không, O(1)
Import bởi: storage.data_processor, logic.loan_manager,
            interface.account_manager, interface.menu
"""
from structure.custom_list import CustomList


class UserArray:
    """
    Mảng người dùng — bọc quanh CustomList, thêm tra cứu/xóa theo user_id.
    """

    def __init__(self):
        self._users = CustomList()

    def append(self, user_obj) -> None:
        """Thêm người dùng vào cuối mảng. O(1) trung bình."""
        self._users.append(user_obj)

    def get_by_id(self, user_id):
        """Tìm người dùng theo user_id. Trả về User hoặc None. O(n)."""
        return self._users.find(lambda u: u.user_id == user_id)

    def remove_by_id(self, user_id) -> bool:
        """Xóa người dùng theo user_id. Trả về True nếu đã xóa. O(n)."""
        return self._users.remove(lambda u: u.user_id == user_id)

    def get_all(self) -> CustomList:
        """Lấy toàn bộ người dùng ra CustomList. O(n)."""
        result = CustomList()
        for user in self._users:
            result.append(user)
        return result

    def size(self) -> int:
        """Số lượng người dùng hiện có. O(1)."""
        return self._users.size

    def is_empty(self) -> bool:
        """Kiểm tra mảng người dùng có rỗng không. O(1)."""
        return self._users.is_empty()

    def __len__(self) -> int:
        return self._users.size

    def __iter__(self):
        return iter(self._users)

    def __repr__(self) -> str:
        return f"UserArray(size={self._users.size})"
