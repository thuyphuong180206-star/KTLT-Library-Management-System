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
def search_book_by_id(hash_map_obj, book_id):
    """Tìm chính xác một cuốn sách thông qua Mã sách (Tra cứu O(1))"""
    if not hash_map_obj:
        return None
    return hash_map_obj.search(book_id)

def search_books_by_keyword(hash_map_obj, keyword):
    """Tìm kiếm tương đối theo Tên sách hoặc Tác giả"""
    if not hash_map_obj:
        return []
    
    # Lấy toàn bộ sách từ Hash Map ra mảng
    all_books = hash_map_obj.get_all_books()
    keyword_lower = keyword.lower().strip()
    
    result = []
    for book in all_books:
        if (keyword_lower in book.get_title().lower()) or (keyword_lower in book.get_author().lower()):
            result.append(book)
            
    return result