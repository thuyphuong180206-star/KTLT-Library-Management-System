"""
Mô-đun sắp xếp danh mục sách (Quick Sort)
Nhiệm vụ: Cài đặt giải thuật Quick Sort để sắp xếp danh sách sách
          phục vụ hiển thị theo thứ tự A-Z.
Ràng buộc: Không chứa lệnh input/print. Không dùng hàm sort() có sẵn của Python.
Các hàm:
    - quicksort(book_list, key="title")
        Sắp xếp danh sách sách A-Z theo tiêu chí (mặc định: tên sách).
        Trả về: list[Book] đã sắp xếp

    - _partition(book_list, low, high, key)
        Hàm nội bộ phục vụ quicksort — chọn pivot và phân hoạch mảng.
        Trả về: int (chỉ số pivot sau khi phân hoạch)
Import bởi: interface.menu
"""

def _partition(arr, low, high, key_fn):
    """Phân hoạch Lomuto: dồn các phần tử có khóa <= khóa của chốt (arr[high]) về bên trái."""
    pivot_key = key_fn(arr[high])
    i = low - 1
    for j in range(low, high):
        if key_fn(arr[j]) <= pivot_key:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def _quick_sort_recursive(arr, low, high, key_fn):
    """Lõi Quick Sort dùng chung: chỉ biết chia để trị, không biết tiêu chí sắp xếp cụ thể."""
    if low < high:
        pivot_index = _partition(arr, low, high, key_fn)
        _quick_sort_recursive(arr, low, pivot_index - 1, key_fn)
        _quick_sort_recursive(arr, pivot_index + 1, high, key_fn)


def _key_by_publisher(book):
    return (book.get_publisher().lower(), book.get_title().lower())


def _key_by_author(book):
    return (book.get_author().lower(), book.get_title().lower())


def quick_sort_by_publisher(book_list):
    """Sắp xếp một danh sách sách mới theo Nhà xuất bản, trùng NXB thì sắp theo tên sách."""
    result = list(book_list)
    _quick_sort_recursive(result, 0, len(result) - 1, _key_by_publisher)
    return result


def quick_sort_by_author(book_list):
    """Sắp xếp một danh sách sách mới theo Tác giả, trùng tác giả thì sắp theo tên sách."""
    result = list(book_list)
    _quick_sort_recursive(result, 0, len(result) - 1, _key_by_author)
    return result
