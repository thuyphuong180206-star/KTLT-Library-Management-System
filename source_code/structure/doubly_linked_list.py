"""
Cấu trúc dữ liệu Danh sách liên kết kép (Doubly Linked List) — Lưu lịch sử giao dịch
Nhiệm vụ: Lưu trữ toàn bộ phiếu mượn/trả theo thứ tự thời gian.
          Giao dịch mới nhất luôn thêm vào cuối (tail), O(1).
Các phương thức:
    - add_transaction(loan_obj)          : Thêm phiếu mới vào cuối, O(1)
    - get_all_transactions()             : Lấy toàn bộ phiếu theo thứ tự thời gian, trả về CustomList, O(n)
    - get_transactions_by_user(user_id)  : Lọc phiếu của một bạn đọc, trả về CustomList, O(n)
Import bởi: storage.data_processor, logic.loan_manager, logic.report
"""
from structure.custom_list import CustomList


class _Node:
    """
    Nút nội bộ của danh sách liên kết kép.
 
    Attributes:
        data:           Đối tượng Loan được lưu tại nút này.
        prev (_Node):   Con trỏ tới nút liền trước (None nếu là head).
        next (_Node):   Con trỏ tới nút liền sau  (None nếu là tail).
    """
 
    __slots__ = ("data", "prev", "next")
 
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None
 
 
class TransactionList:
    """
    Danh sách liên kết kép lưu lịch sử giao dịch mượn/trả theo thứ tự thời gian.
 
    Mỗi phần tử trong danh sách là một đối tượng Loan.
    Giao dịch mới nhất luôn nằm ở cuối (tail) — phản ánh đúng thứ tự thêm vào.
 
    Attributes:
        _head (_Node):  Con trỏ tới nút đầu danh sách.
        _tail (_Node):  Con trỏ tới nút cuối danh sách.
        _size (int):    Số lượng giao dịch hiện có.
    """
 
    def __init__(self):
        self._head = None
        self._tail = None
        self._size = 0
    # Thuộc tính chỉ đọc
 
    @property
    def size(self) -> int:
        """Số lượng giao dịch đang lưu trong danh sách."""
        return self._size
 
    def is_empty(self) -> bool:
        """Trả về True nếu danh sách chưa có giao dịch nào."""
        return self._size == 0
 
    # Các hàm chính theo yêu cầu
 
    def add_transaction(self, loan_obj) -> None:
        """
        Thêm một giao dịch mới vào cuối danh sách.
 
        Độ phức tạp: O(1) — nhờ con trỏ _tail.
 
        Args:
            loan_obj (Loan): Đối tượng giao dịch cần thêm.
        """
        new_node = _Node(loan_obj)
 
        if self._tail is None:
            # Danh sách rỗng — nút mới vừa là head vừa là tail
            self._head = new_node
            self._tail = new_node
        else:
            # Nối nút mới vào sau tail hiện tại
            new_node.prev = self._tail
            self._tail.next = new_node
            self._tail = new_node
 
        self._size += 1
 
    def get_all_transactions(self) -> CustomList:
        """
        Duyệt toàn bộ danh sách từ đầu đến cuối, trả về lịch sử giao dịch theo thứ tự thời gian.

        Độ phức tạp: O(n).

        Returns:
            CustomList[Loan]: Danh sách tất cả giao dịch, sắp xếp từ cũ nhất đến mới nhất.
        """
        result = CustomList()
        current = self._head
        while current is not None:
            result.append(current.data)
            current = current.next
        return result

    def get_transactions_by_user(self, user_id: str) -> CustomList:
        """
        Lọc và trả về tất cả giao dịch thuộc về một độc giả cụ thể.

        Độ phức tạp: O(n).

        Args:
            user_id (str): Mã độc giả cần tra cứu lịch sử.

        Returns:
            CustomList[Loan]: Danh sách giao dịch của độc giả đó, theo thứ tự thời gian.
                               Trả về CustomList rỗng nếu không tìm thấy.
        """
        result = CustomList()
        current = self._head
        while current is not None:
            if current.data.user_id == user_id:
                result.append(current.data)
            current = current.next
        return result
 
    # Dunder methods
 
    def __len__(self) -> int:
        """Hỗ trợ len(transaction_list)."""
        return self._size
 
    def __iter__(self):
        """Hỗ trợ vòng lặp for loan in transaction_list."""
        current = self._head
        while current is not None:
            yield current.data
            current = current.next
 
    def __repr__(self) -> str:
        return f"TransactionList(size={self._size})"
 