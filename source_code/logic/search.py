"""
BỘ XỬ LÝ GIẢI THUẬT TRA CỨU HỆ THỐNG (LOGIC LAYER - SEARCH ENGINE)
Nhiệm vụ: Triển khai các thuật toán tra cứu sách độc lập. Cách ly hoàn toàn với các câu lệnh print() hay input() của tầng Interface.
Quy tắc kiến trúc: Tiếp nhận tham chiếu bộ nhớ từ RAM, return đối tượng hoặc danh sách kết quả thô.

Các hàm bắt buộc phải viết trực tiếp:
    - search_book_by_id(hash_map_obj: BookHashMap, book_id: str) -> Book | None:
        + Giải thuật tối ưu: Tìm kiếm chính xác tuyệt đối. Gọi trực tiếp phương thức băm hash_map_obj.search(book_id),
          định vị tức thời ô nhớ dữ liệu với hiệu năng đạt mức hằng số O(1).
        + Kết quả trả về: Tham chiếu đối tượng Book nếu tồn tại, ngược lại trả về None.

    - search_books_by_keyword(hash_map_obj: BookHashMap, keyword: str) -> list[Book]:
        + Giải thuật: Tìm kiếm gần đúng tương đối. Vì từ khóa là động (từ khóa nằm trong tên sách hoặc tác giả), giải thuật gọi
          hash_map_obj.get_all_books() để lấy mảng phẳng, thực hiện giải thuật Tìm kiếm tuyến tính (Linear Search) với độ phức tạp O(N),
          sử dụng phương thức chuỗi `.lower()` đưa dữ liệu về chữ thường để so khớp chuỗi con bằng toán tử `in`.
        + Kết quả trả về: Mảng list chứa tất cả các đối tượng Book thỏa mãn bộ lọc tìm kiếm.
"""
