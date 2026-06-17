Library-Management-System/              # THƯ MỤC GỐC CỦA TOÀN BỘ DỰ ÁN
│
├── data/                               # Thư mục chứa các tệp cơ sở dữ liệu phẳng vật lý
│   ├── books.csv                       # Lưu kho sách mở rộng (Đã cấu trúc lại thành 10 trường)
│   ├── users.csv                       # Lưu danh sách tài khoản hệ thống (Admin / Reader)
│   ├── loans.csv                       # Lưu lịch sử tất cả giao dịch mượn/trả sách
│   └── system_error.log                # Tệp ghi log ngoại lệ I/O (Chốt chặn lập trình phòng ngừa)
│
├── source_code/                        # THƯ MỤC CHỨA TOÀN BỘ MÃ NGUỒN CHÍNH (.py)
│   ├── __init__.py                     # File rỗng định danh Python Package cho source_code/
│   ├── main.py                         # Điểm khởi chạy hệ thống (System Entry Point & Bootstrapper)
│   │
│   ├── storage/                        # TẦNG LƯU TRỮ DỮ LIỆU (STORAGE LAYER)
│   │   ├── __init__.py                 # Khai báo package nội bộ storage
│   │   └── data_processor.py           # Logic Đọc/Ghi file CSV, kiểm soát ngoại lệ và tự phục hồi
│   │
│   ├── objects/                        # TẦNG THỰC THỂ ĐỐI TƯỢNG (OBJECT LAYER)
│   │   ├── __init__.py                 # Khai báo package nội bộ objects
│   │   ├── books.py                    # Định nghĩa lớp Book (Đóng gói private __, Getters/Setters, to_dict/from_dict)
│   │   ├── users.py                    # Định nghĩa lớp User (Mô hình hóa tài khoản, phân quyền, mức ưu tiên)
│   │   └── loans.py                    # Định nghĩa lớp Loan (Mô hình hóa phiếu mượn/trả, lưu vết tiền phạt)
│   │
│   ├── structure/                      # TẦNG CẤU TRÚC DỮ LIỆU LÕI VẬN HÀNH TRÊN RAM (STRUCTURE LAYER)
│   │   ├── __init__.py                 # Khai báo package nội bộ structure
│   │   ├── hash_map.py                 # Cài đặt lớp BookHashMap (Separate Chaining) tra cứu sách O(1)
│   │   ├── doubly_linked_list.py       # Cài đặt lớp TransactionList (DLL) lưu lịch sử giao dịch O(1)
│   │   └── priority_queue.py           # Cài đặt lớp PriorityQueue (Max-Heap nhị phân) thống kê sách phổ biến O(log N)
│   │
│   ├── logic/                          # TẦNG ĐIỀU PHỐI NGHIỆP VỤ VÀ THUẬT TOÁN (LOGIC LAYER)
│   │   ├── __init__.py                 # Khai báo package nội bộ logic
│   │   ├── search.py                   # Cài đặt tìm kiếm chính xác O(1) và tìm kiếm tương đối O(N)
│   │   ├── sort.py                     # Cài đặt giải thuật Quick Sort đệ quy đa tiêu chí động tự thân
│   │   └── loan_manager.py             # Logic mượn/trả, công thức phạt lũy tiến, điều tiết hàng chờ Max-Heap
│   │
│   └── interface/                      # TẦNG GIAO DIỆN NGƯỜI DÙNG CONSOLE (INTERFACE LAYER)
│       ├── __init__.py                 # Khai báo package nội bộ interface
│       ├── menu.py                     # Vòng lặp while True điều hướng chính, vẽ khung ASCII Table (.ljust/.rjust)
│       ├── account_manager.py          # Biểu mẫu dòng lệnh phục vụ Đăng nhập / Đăng ký tài khoản
│       └── validator.py                # Màng lọc dữ liệu thô (chuỗi nhập từ bàn phím), Regex kiểm tra cú pháp ĐKCB
│
└── tests/                              # TẦNG KIỂM THỬ TỰ ĐỘNG ĐỘC LẬP (UNIT TEST LAYER)
    ├── __init__.py                     # File rỗng định danh package tests/
    ├── test_sort.py                    # Kịch bản unittest xác thực giải thuật Quick Sort đa tiêu chí trùng NXB
    └── test_validator.py               # Kịch bản unittest xác thực bộ lọc validator chặn dữ liệu bẩn đầu vào

