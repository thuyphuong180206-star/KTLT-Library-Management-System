"""
Mô-đun tìm kiếm sách (Search Engine)
Nhiệm vụ: Cài đặt các hàm tìm kiếm sách theo nhiều tiêu chí.
Ràng buộc: Không chứa lệnh input/print. Trả về kết quả qua return.
Các hàm:
    - search_by_id(hash_map, book_id)
        Tìm chính xác theo mã sách, O(1) qua BookHashMap.
        Trả về: Book | None

    - search_by_title(hash_map, keyword)
        Tìm tương đối theo tên sách, duyệt tuyến tính O(n).
        Trả về: list[Book]

    - search_by_author(hash_map, keyword)
        Tìm tương đối theo tên tác giả, duyệt tuyến tính O(n).
        Trả về: list[Book]

    - search_by_genre(hash_map, keyword)
        Tìm tương đối theo thể loại, duyệt tuyến tính O(n).
        Trả về: list[Book]
Import bởi: logic.loan_manager, interface.menu
"""
