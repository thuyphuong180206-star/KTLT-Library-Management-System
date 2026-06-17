"""
Cấu trúc dữ liệu Bảng băm (Hash Map) — Lưu trữ danh mục sách
Nhiệm vụ: Lưu trữ và tra cứu sách theo mã sách (book_id) với độ phức tạp O(1).
Cài đặt: Separate Chaining — mỗi bucket là một chuỗi liên kết _Entry.
         Tự động rehash khi load factor vượt ngưỡng 0.75.
Các phương thức:
    - insert(book_id, book_obj)  : Thêm/cập nhật sách, O(1) trung bình
    - search(book_id)            : Tìm sách theo mã, O(1) trung bình
    - delete(book_id)            : Xóa sách khỏi bảng băm, O(1) trung bình
    - get_all_books()            : Lấy toàn bộ sách ra list, O(n)
Import bởi: storage.data_processor, logic.search, logic.sort,
            logic.loan_manager, logic.report, interface.menu
"""
