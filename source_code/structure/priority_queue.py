"""
Cấu trúc dữ liệu Hàng đợi ưu tiên (Max-Heap) — Thống kê sách phổ biến
Nhiệm vụ: Xếp hạng sách theo số lượt mượn (borrow_count),
          sách có lượt mượn cao nhất luôn nằm ở đầu heap.
Cài đặt: Max-Heap nhị phân với _sift_up và _sift_down, lưu trên CustomList
         (không dùng list có sẵn của Python).
Các phương thức:
    - enqueue(book_obj)    : Thêm sách vào đúng vị trí theo borrow_count, O(log n)
    - dequeue()            : Lấy sách có lượt mượn cao nhất ra, O(log n)
    - peek_top_n(n)        : Lấy top n sách mà không xóa khỏi heap, trả về CustomList, O(n log n)
    - is_empty()           : Kiểm tra heap rỗng, O(1)
Import bởi: logic.report
"""
from structure.custom_list import CustomList


class PriorityQueue:

    def __init__(self):
        self._heap = CustomList()

    # ---------- helpers ----------

    def _sift_up(self, i):
        while i > 0:
            parent = (i - 1) // 2
            if self._heap[i].borrow_count > self._heap[parent].borrow_count:
                self._heap[i], self._heap[parent] = self._heap[parent], self._heap[i]
                i = parent
            else:
                break

    def _sift_down(self, i, heap=None):
        if heap is None:
            heap = self._heap
        n = len(heap)
        while True:
            largest, l, r = i, 2*i+1, 2*i+2
            if l < n and heap[l].borrow_count > heap[largest].borrow_count:
                largest = l
            if r < n and heap[r].borrow_count > heap[largest].borrow_count:
                largest = r
            if largest != i:
                heap[i], heap[largest] = heap[largest], heap[i]
                i = largest
            else:
                break

    # ---------- các hàm yêu cầu ----------

    def enqueue(self, book_obj):
        """Thêm sách vào đúng vị trí theo borrow_count. O(log n)"""
        self._heap.append(book_obj)
        self._sift_up(self._heap.size - 1)

    def dequeue(self):
        """Lấy sách có lượt mượn cao nhất ra. O(log n)"""
        if self.is_empty():
            raise IndexError("Hàng đợi rỗng")
        top = self._heap[0]
        last_index = self._heap.size - 1
        last = self._heap[last_index]
        self._heap.remove_at(last_index)
        if not self._heap.is_empty():
            self._heap[0] = last
            self._sift_down(0)
        return top

    def is_empty(self):
        """Kiểm tra hàng đợi rỗng. O(1)"""
        return self._heap.is_empty()

    def peek_top_n(self, n):
        """Lấy top n sách mượn nhiều nhất mà không xóa khỏi heap. O(n log n)."""
        result = CustomList()
        if n <= 0 or self.is_empty():
            return result

        temp_heap = CustomList()
        for book in self._heap:
            temp_heap.append(book)

        count = min(n, temp_heap.size)

        for _ in range(count):
            top = temp_heap[0]
            result.append(top)
            last_index = temp_heap.size - 1
            last = temp_heap[last_index]
            temp_heap.remove_at(last_index)
            if not temp_heap.is_empty():
                temp_heap[0] = last
                self._sift_down(0, temp_heap)

        return result
