"""
Cấu trúc dữ liệu Mảng động tự quản lý (Custom List)
Nhiệm vụ: Cài đặt List bằng mảng động tự quản lý, dùng làm container thay cho list built-in
          của Python ở bất kỳ nơi nào cần lưu một danh sách phần tử (book, user, loan...).
Cài đặt: Tự quản lý capacity (_data, _capacity, _size) trên một mảng Python thô —
         tự nhân đôi capacity khi đầy (amortized O(1) append), tự dồn phần tử khi xóa.
         Không gọi list.append()/list.remove() có sẵn để "giả vờ" tự cài.
Các phương thức:
    - append(item)           : Thêm phần tử vào cuối, O(1) trung bình (tự resize khi đầy)
    - get(index)              : Lấy phần tử theo vị trí, O(1)
    - remove_at(index)        : Xóa phần tử theo vị trí, dồn mảng, O(n)
    - remove(predicate)       : Xóa phần tử đầu tiên thỏa predicate, O(n)
    - find(predicate)         : Tìm phần tử đầu tiên thỏa predicate, O(n)
    - is_empty()              : Kiểm tra rỗng, O(1)
    - clear()                 : Xóa toàn bộ phần tử, giữ nguyên capacity
    - to_list() / get_all()   : Chuyển sang list thuần của Python, dùng ở biên ghi CSV/hiển thị, O(n)
    - size (property)        : Số lượng phần tử hiện có, O(1)
Dunder hỗ trợ: __len__, __iter__, __getitem__ (có slicing), __setitem__,
               __contains__, __eq__, __repr__
"""


class CustomList:
    """
    List tự cài bằng mảng động tự quản lý capacity — dùng thay cho list built-in trong toàn hệ thống.
    """

    def __init__(self, initial_capacity: int = 8):
        if initial_capacity < 1:
            initial_capacity = 1
        self._capacity = initial_capacity
        self._data = [None] * self._capacity
        self._size = 0

    # ------------------------------------------------------------------ #
    # Quản lý capacity nội bộ                                             #
    # ------------------------------------------------------------------ #

    def _resize(self, new_capacity: int) -> None:
        new_data = [None] * new_capacity
        for i in range(self._size):
            new_data[i] = self._data[i]
        self._data = new_data
        self._capacity = new_capacity

    # ------------------------------------------------------------------ #
    # API ghi                                                              #
    # ------------------------------------------------------------------ #

    def append(self, item) -> None:
        """Thêm phần tử vào cuối mảng. O(1) trung bình — tự nhân đôi capacity khi đầy."""
        if self._size == self._capacity:
            self._resize(self._capacity * 2)
        self._data[self._size] = item
        self._size += 1

    def remove_at(self, index: int) -> None:
        """Xóa phần tử tại vị trí index, dồn các phần tử phía sau lên một bậc. O(n)."""
        if index < 0 or index >= self._size:
            raise IndexError("Chỉ số vượt giới hạn CustomList")
        for i in range(index, self._size - 1):
            self._data[i] = self._data[i + 1]
        self._data[self._size - 1] = None
        self._size -= 1

    def remove(self, predicate) -> bool:
        """Xóa phần tử đầu tiên thỏa predicate(item) == True. Trả về True nếu đã xóa."""
        for i in range(self._size):
            if predicate(self._data[i]):
                self.remove_at(i)
                return True
        return False

    def clear(self) -> None:
        """Xóa toàn bộ phần tử, giữ nguyên capacity hiện tại."""
        self._data = [None] * self._capacity
        self._size = 0

    # ------------------------------------------------------------------ #
    # API đọc                                                              #
    # ------------------------------------------------------------------ #

    def get(self, index: int):
        """Lấy phần tử tại vị trí index. O(1)."""
        if index < 0 or index >= self._size:
            raise IndexError("Chỉ số vượt giới hạn CustomList")
        return self._data[index]

    def find(self, predicate):
        """Trả về phần tử đầu tiên thỏa predicate(item) == True, hoặc None nếu không có."""
        for i in range(self._size):
            if predicate(self._data[i]):
                return self._data[i]
        return None

    def is_empty(self) -> bool:
        """Kiểm tra mảng có rỗng không. O(1)."""
        return self._size == 0

    def to_list(self) -> list:
        """Chuyển toàn bộ phần tử sang list thuần của Python — dùng ở biên ghi CSV/hiển thị. O(n)."""
        return [self._data[i] for i in range(self._size)]

    def get_all(self) -> list:
        """Alias của to_list() — phục vụ nơi gọi theo quy ước .get_all()."""
        return self.to_list()

    @property
    def size(self) -> int:
        """Số lượng phần tử hiện có."""
        return self._size

    # ------------------------------------------------------------------ #
    # Dunder methods — dùng tự nhiên như list ở interface/logic layer     #
    # ------------------------------------------------------------------ #

    def __len__(self) -> int:
        return self._size

    def __iter__(self):
        for i in range(self._size):
            yield self._data[i]

    def __getitem__(self, index):
        if isinstance(index, slice):
            result = CustomList()
            for i in range(*index.indices(self._size)):
                result.append(self._data[i])
            return result
        if index < 0 or index >= self._size:
            raise IndexError("Chỉ số vượt giới hạn CustomList")
        return self._data[index]

    def __setitem__(self, index, value) -> None:
        if index < 0 or index >= self._size:
            raise IndexError("Chỉ số vượt giới hạn CustomList")
        self._data[index] = value

    def __contains__(self, item) -> bool:
        for i in range(self._size):
            if self._data[i] == item:
                return True
        return False

    def __eq__(self, other) -> bool:
        if isinstance(other, CustomList):
            other_items = list(other)
        elif isinstance(other, list):
            other_items = other
        else:
            return NotImplemented
        if len(other_items) != self._size:
            return False
        for i in range(self._size):
            if self._data[i] != other_items[i]:
                return False
        return True

    def __repr__(self) -> str:
        return f"CustomList({self.to_list()!r})"
