"""
HẠ TẦNG HÀNG ĐỢI ƯU TIÊN CẤU TRÚC MAX-HEAP (DATA STRUCTURE - PRIORITY QUEUE)
Nhiệm vụ: Phục vụ mô-đun thống kê sách thịnh hành và điều tiết thứ hạng mượn sách khan hiếm của thư viện.
Hiệu năng: Vun đống (Sift) đạt tốc độ tối ưu O(log N).

Các thuộc tính của lớp chính PriorityQueue:
    - _heap: list[Any]                 (Mảng động lưu trữ cây nhị phân dạng Max-Heap phẳng)

Các phương thức bắt buộc cài đặt trực tiếp:
    - _parent(self, index: int) -> int: Trả về chỉ số nút cha: (index - 1) // 2.
    - _left_child(self, index: int) -> int: Trả về chỉ số nút con trái: 2 * index + 1.
    - _right_child(self, index: int) -> int: Trả về chỉ số nút con phải: 2 * index + 2.
    - _sift_up(self, index: int) -> None: So sánh thuộc tính ưu tiên (`borrow_count` của Sách hoặc thứ hạng tài khoản của Độc giả) với nút cha, đảo tầng đi lên nếu vi phạm cấu trúc đống lớn nhất.
    - _sift_down(self, index: int) -> None: So sánh nút hiện tại với hai nút con, thực hiện đảo vị trí hạ tầng đi xuống nút con lớn hơn nếu vi phạm cấu trúc đống.
    - enqueue(self, item: Any) -> None: Chèn phần tử vào cuối mảng `_heap` và kích hoạt hàm vun cao `_sift_up`.
    - dequeue(self) -> Any: Hoán đổi phần tử đầu gốc heap với phần tử cuối mảng, dùng phương thức `.pop()` gỡ bỏ phần tử cuối, gọi `_sift_down` cân bằng lại cây nhị phân và hoàn trả phần tử lớn nhất.
    - is_empty(self) -> bool: Kiểm tra mảng heap còn phần tử nào không.
"""