"""
Cấu trúc dữ liệu Hàng đợi đơn (Singly Linked Queue) — Quản lý yêu cầu chờ mượn sách
Nhiệm vụ: Lưu danh sách yêu cầu đặt trước mượn sách theo nguyên tắc FIFO —
          ai đăng ký trước được xử lý trước khi sách có sẵn trở lại.
Cài đặt: Danh sách liên kết đơn (QueueNode chỉ có .next, không có .prev như DLL),
         tự quản lý bằng _front/_rear, không dùng list có sẵn của Python để lưu hàng đợi.
Các phương thức:
    - enqueue(request)  : Thêm yêu cầu vào cuối hàng đợi, O(1)
    - dequeue()          : Lấy và xóa yêu cầu ở đầu hàng đợi, O(1)
    - peek()             : Xem yêu cầu đầu hàng đợi mà không xóa, O(1)
    - is_empty()         : Kiểm tra hàng đợi rỗng, O(1)
    - size (property)   : Số lượng yêu cầu đang chờ, O(1)
    - to_list()          : Xuất toàn bộ hàng đợi ra CustomList theo thứ tự FIFO, O(n)
    - remove_match(predicate) : Tìm và rút phần tử đầu tiên thỏa predicate ra khỏi hàng đợi
                                 (dù không ở đầu hàng), giữ nguyên thứ tự phần còn lại, O(n)
Import bởi: storage.data_processor, logic.loan_manager
"""
from structure.custom_list import CustomList


class QueueNode:
    def __init__(self, data):
        self.data = data
        self.next = None


class WaitingQueue:
    """
    Queue xử lý yêu cầu chờ mượn sách theo nguyên tắc FIFO.
    Người đăng ký trước sẽ được xử lý trước.
    """

    def __init__(self):
        self._front = None
        self._rear = None
        self._size = 0

    def enqueue(self, request):
        """
        Thêm yêu cầu vào cuối hàng đợi.
        Độ phức tạp: O(1)
        """
        new_node = QueueNode(request)

        if self._rear is None:
            self._front = new_node
            self._rear = new_node
        else:
            self._rear.next = new_node
            self._rear = new_node

        self._size += 1

    def dequeue(self):
        """
        Lấy yêu cầu ở đầu hàng đợi.
        Độ phức tạp: O(1)
        """
        if self.is_empty():
            return None

        removed_node = self._front
        self._front = self._front.next

        if self._front is None:
            self._rear = None

        self._size -= 1
        return removed_node.data

    def peek(self):
        """
        Xem yêu cầu đầu hàng đợi nhưng không xóa.
        Độ phức tạp: O(1)
        """
        if self.is_empty():
            return None

        return self._front.data

    def is_empty(self):
        """
        Kiểm tra hàng đợi rỗng.
        Độ phức tạp: O(1)
        """
        return self._size == 0

    @property
    def size(self) -> int:
        """Số lượng yêu cầu đang chờ trong hàng đợi."""
        return self._size

    def to_list(self):
        """
        Chuyển toàn bộ queue sang CustomList để hiển thị.
        Độ phức tạp: O(n)
        """
        result = CustomList()
        current = self._front

        while current is not None:
            result.append(current.data)
            current = current.next

        return result

    def remove_match(self, predicate):
        """
        Tìm phần tử đầu tiên thỏa predicate(item) == True và rút khỏi hàng đợi,
        dù phần tử đó không nằm ở đầu hàng. Giữ nguyên thứ tự các phần tử còn lại.
        Độ phức tạp: O(n)
        """
        prev = None
        current = self._front

        while current is not None:
            if predicate(current.data):
                if prev is None:
                    self._front = current.next
                else:
                    prev.next = current.next
                if current is self._rear:
                    self._rear = prev
                self._size -= 1
                return current.data
            prev = current
            current = current.next

        return None
