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
