storage/data_processor.py
"""
Mô-đun đọc/ghi cơ sở dữ liệu CSV (Storage Layer)
Nhiệm vụ: Nạp dữ liệu từ file CSV lên các cấu trúc dữ liệu trên RAM khi khởi động,
        và ghi toàn bộ trạng thái RAM xuống CSV sau mỗi thao tác thay đổi dữ liệu.
Ràng buộc:
    - Tầng duy nhất được phép đọc/ghi file trong toàn hệ thống.
    - Không chứa logic nghiệp vụ hay hiển thị giao diện.
    - Tự parse CSV thủ công bằng csv.reader, không dùng thư viện json/pandas.
    - Nếu books.csv hoặc loans.csv không tồn tại: tự tạo file mới chỉ có header.
    - Nếu users.csv không tồn tại: tự tạo file mới với header và ghi sẵn tài khoản admin mặc định (user_id="admin", password="admin123", role="admin", reader_type="") để đảm bảo hệ thống luôn đăng nhập được. 
    - Nếu dòng dữ liệu lỗi: ghi vào system_error.log, bỏ qua dòng đó và tiếp tục.
Các hàm:
    - load_system_data(books_path, users_path, loans_path)
        → tuple(BookHashMap, TransactionList, UserArray)
    - save_system_data(hash_map, dll, user_array, books_path, users_path, loans_path)
        → None
Import: objects.books.Book, objects.users.User, objects.loans.Loan,
        structure.hash_map.BookHashMap, structure.doubly_linked_list.TransactionList,
        structure.user_array.UserArray
Import bởi: main
"""
