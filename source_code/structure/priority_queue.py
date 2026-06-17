"""
Cấu trúc dữ liệu Hàng đợi ưu tiên (Max-Heap) — Thống kê sách phổ biến
Nhiệm vụ: Xếp hạng sách theo số lượt mượn (borrow_count),
          sách có lượt mượn cao nhất luôn nằm ở đầu heap.
Cài đặt: Max-Heap nhị phân với _sift_up và _sift_down.
Các phương thức:
    - enqueue(book_obj)    : Thêm sách vào đúng vị trí theo borrow_count, O(log n)
    - dequeue()            : Lấy sách có lượt mượn cao nhất ra, O(log n)
    - peek_top_n(n)        : Lấy top n sách mà không xóa khỏi heap, O(n log n)
    - is_empty()           : Kiểm tra heap rỗng, O(1)
Import bởi: logic.report
"""
