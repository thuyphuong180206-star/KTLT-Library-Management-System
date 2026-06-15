"""
ĐIỂM KHỞI CHẠY VÀ ĐIỀU PHỐI HỆ THỐNG TRUNG TÂM (SYSTEM ENTRY POINT - BOOTSTRAPPER)
Nhiệm vụ: Khởi tạo đường dẫn động, nạp dữ liệu từ tệp CSV lên bộ nhớ RAM phẳng và chuyển giao luồng cho Menu.
Quy tắc: Là tệp duy nhất được gọi lệnh chạy trực tiếp từ Terminal. Không chứa vòng lặp menu hay logic tính toán.

Các thư viện và mô-đun bắt buộc phải import:
    - os, sys, datetime (Thư viện chuẩn hệ thống)
    - storage.data_processor (Để gọi hàm load_system_data)
    - interface.menu (Để chuyển giao luồng chạy sang hàm menu_main)

Đường dẫn tệp tin vật lý được chốt cấu hình (Khai báo biến hằng số toàn cục):
    - DATA_DIR = Thư mục 'data/' nằm tại thư mục gốc dự án
    - BOOKS_CSV = os.path.join(DATA_DIR, "books.csv")
    - USERS_CSV = os.path.join(DATA_DIR, "users.csv")
    - LOANS_CSV = os.path.join(DATA_DIR, "loans.csv")
"""
