"""
HẠ TẦNG BẢNG BĂM ĐỘC LẬP TỰ CÀI ĐẶT (DATA STRUCTURE - BOOK HASH MAP)
Nhiệm vụ: Lưu trữ toàn bộ thực thể Book trên bộ nhớ chính RAM. Giải quyết va chạm bằng Separate Chaining.
Hiệu năng: Đạt tốc độ tra cứu, chèn và xóa lý tưởng trong thời gian hằng số O(1).

Lớp nội bộ bổ trợ (Private Helper Class):
    - _Entry:
        + Thuộc tính: key: str (Mã book_id), value: Book (Đối tượng thực thể), next: '_Entry | None' (Con trỏ node tiếp theo)

Các thuộc tính của lớp chính BookHashMap:
    - _buckets: list['_Entry | None']  (Mảng cố định kích thước nguyên tố tĩnh, chốt cứng M = 1009 Buckets)
    - _size: int                       (Tổng số lượng phần tử đầu sách thực tế đang lưu trên bộ nhớ RAM)

Các phương thức bắt buộc cài đặt trực tiếp (Cấm dùng kiểu dữ liệu dict có sẵn của Python làm hạ tầng cốt lõi):
    - _hash(self, key: str) -> int: Hàm băm nhân chuỗi chia lấy dư: hash_value = sum(ord(c)) % 1009.
    - insert(self, key: str, value: Book) -> None: Thêm mới đối tượng hoặc cập nhật nếu key đã tồn tại trong chuỗi liên kết đơn.
    - search(self, key: str) -> Book | None: Băm key, nhảy thẳng tới Bucket điều hướng và duyệt tìm tuyến tính. Trả về tham chiếu đối tượng.
    - delete(self, key: str) -> bool: Tìm và gỡ node _Entry ra khỏi chuỗi liên kết đơn Separate Chaining. Trả về True nếu thành công.
    - get_all_books(self) -> list[Book]: Quét qua toàn bộ 1009 ô Bucket, gom tất cả các đối tượng Book thành một mảng phẳng phục vụ tầng hiển thị.
"""
