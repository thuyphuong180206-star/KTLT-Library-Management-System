"""
BỘ XỬ LÝ GIẢI THUẬT SẮP XẾP NÂNG CAO (LOGIC LAYER - SORT ENGINE)
Nhiệm vụ: Triển khai giải thuật sắp xếp tự thân đệ quy chia để trị. Nghiêm cấm sử dụng các phương thức tích hợp sẵn như .sort() hoặc sorted().
Quy tắc kiến trúc: Cách ly hoàn toàn với luồng I/O giao diện và tệp tin vật lý.

Các hàm bắt buộc phải viết trực tiếp:
    - quick_sort_books(book_list: list[Book], key_attr: str) -> list[Book]:
        + Giải thuật tối ưu: Triển khai Quick Sort đệ quy chia để trị (Độ phức tạp thời gian trung bình O(N log N)).
        + Logic điều phối đa tiêu chí: Khi tham số khóa gán key_attr == "publisher", quá trình so sánh toán học giữa hai phần tử
          Book_A và Book_B bắt buộc phải có luật kiểm tra: nếu trùng tên Nhà xuất bản, lập tức rẽ nhánh logic phụ: so sánh phụ theo thứ tự bảng chữ cái của trường tên sách (`title`).
        + Kết quả trả về: Một danh sách mảng list[Book] mới hoàn toàn đã được sắp đặt đúng trật tự bảng chữ cái tăng dần.
"""


