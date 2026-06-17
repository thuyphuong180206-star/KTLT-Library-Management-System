"""
Mô-đun tìm kiếm sách (Search Engine)
Nhiệm vụ: Cài đặt các hàm tìm kiếm sách theo nhiều tiêu chí.
Ràng buộc: Không chứa lệnh input/print. Trả về kết quả qua return.
Các hàm:
    - search_by_id(hash_map, book_id)        : Tìm chính xác theo mã sách, O(1). Trả về: Book | None
    - search_by_title(hash_map, keyword)      : Tìm tương đối theo tên sách, O(n). Trả về: CustomList[Book]
    - search_by_author(hash_map, keyword)     : Tìm tương đối theo tác giả, O(n). Trả về: CustomList[Book]
    - search_by_genre(hash_map, keyword)      : Tìm tương đối theo thể loại, O(n). Trả về: CustomList[Book]
Import bởi: logic.loan_manager, interface.menu
"""
from structure.custom_list import CustomList


def search_by_id(hash_map, book_id):
    """Tìm chính xác một cuốn sách theo book_id. O(1) qua BookHashMap."""
    return hash_map.search(book_id)


def search_by_title(hash_map, keyword):
    """Tìm tương đối theo tên sách. O(n)."""
    result = CustomList()
    keyword_lower = keyword.lower().strip()
    for book in hash_map.get_all_books():
        if keyword_lower in book.title.lower():
            result.append(book)
    return result


def search_by_author(hash_map, keyword):
    """Tìm tương đối theo tác giả. O(n)."""
    result = CustomList()
    keyword_lower = keyword.lower().strip()
    for book in hash_map.get_all_books():
        if keyword_lower in book.author.lower():
            result.append(book)
    return result


def search_by_genre(hash_map, keyword):
    """Tìm tương đối theo thể loại. O(n)."""
    result = CustomList()
    keyword_lower = keyword.lower().strip()
    for book in hash_map.get_all_books():
        if keyword_lower in book.genre.lower():
            result.append(book)
    return result
