Library-Management-System/              # THƯ MỤC GỐC CỦA TOÀN BỘ DỰ ÁN
│
├── data/                               # Thư mục chứa các tệp cơ sở dữ liệu phẳng vật lý
│   ├── books.csv                       # Lưu danh mục sách (8 trường: book_id, title, author, genre, publisher, quantity, status, borrow_count)
│   ├── users.csv                       # Lưu danh sách tài khoản (Admin / Sinh viên / Giảng viên)
│   ├── loans.csv                       # Lưu lịch sử toàn bộ giao dịch mượn/trả sách
│   ├── waiting_requests.csv            # Lưu danh sách yêu cầu chờ mượn khi sách hết kho
│   └── system_error.log                # Tệp ghi log lỗi I/O (tự tạo bởi data_processor)
│
├── source_code/                        # THƯ MỤC CHỨA TOÀN BỘ MÃ NGUỒN CHÍNH (.py)
│   ├── __init__.py                     # File rỗng định danh Python Package cho source_code/
│   ├── main.py                         # Điểm khởi chạy hệ thống: load dữ liệu, đăng nhập, phân luồng menu
│   │
│   ├── storage/                        # TẦNG LƯU TRỮ DỮ LIỆU (STORAGE LAYER)
│   │   ├── __init__.py                 # Khai báo package nội bộ storage
│   │   └── data_processor.py           # Đọc/Ghi 4 file CSV, xử lý lỗi I/O, tự phục hồi khi mất file
│   │
│   ├── objects/                        # TẦNG THỰC THỂ ĐỐI TƯỢNG (OBJECT LAYER)
│   │   ├── __init__.py                 # Khai báo package nội bộ objects
│   │   ├── books.py                    # Lớp Book: thông tin đầu sách, to_dict/from_dict
│   │   ├── users.py                    # Lớp User: tài khoản, phân quyền, hạn mức mượn theo SV/GV
│   │   ├── loans.py                    # Lớp Loan: phiếu mượn/trả, trạng thái, tiền phạt
│   │   └── requests.py                 # Lớp BorrowRequest: yêu cầu chờ mượn khi sách hết kho
│   │
│   ├── structure/                      # TẦNG CẤU TRÚC DỮ LIỆU LÕI VẬN HÀNH TRÊN RAM (STRUCTURE LAYER)
│   │   ├── __init__.py                 # Khai báo package nội bộ structure
│   │   ├── hash_map.py                 # Lớp BookHashMap (Separate Chaining) — tra cứu sách O(1)
│   │   ├── doubly_linked_list.py       # Lớp TransactionList (DLL) — lưu lịch sử giao dịch O(1)
│   │   ├── priority_queue.py           # Lớp PriorityQueue (Max-Heap) — thống kê top 5 sách O(log N)
│   │   ├── user_array.py               # Lớp UserArray (Mảng tự quản lý) — lưu danh sách bạn đọc
│   │   └── waiting_queue.py            # Lớp WaitingQueue (FIFO) — hàng chờ mượn khi sách hết kho
│   │
│   ├── logic/                          # TẦNG ĐIỀU PHỐI NGHIỆP VỤ VÀ THUẬT TOÁN (LOGIC LAYER)
│   │   ├── __init__.py                 # Khai báo package nội bộ logic
│   │   ├── search.py                   # Tìm kiếm sách: chính xác O(1) theo mã, tương đối O(N) theo tên/tác giả/thể loại
│   │   ├── sort.py                     # Quick Sort sắp xếp danh sách sách A-Z theo tên để hiển thị
│   │   ├── loan_manager.py             # Nghiệp vụ mượn/trả, kiểm tra hạn mức, tính tiền phạt, quản lý hàng chờ
│   │   └── report.py                   # Báo cáo: sách đang mượn, sách quá hạn, top 5 sách mượn nhiều nhất
│   │
│   └── interface/                      # TẦNG GIAO DIỆN NGƯỜI DÙNG CONSOLE (INTERFACE LAYER)
│       ├── __init__.py                 # Khai báo package nội bộ interface
│       ├── menu.py                     # Vòng lặp while True: menu Admin và menu User, hiển thị bảng ASCII, phân trang
│       ├── account_manager.py          # Đăng nhập hệ thống và tạo tài khoản bạn đọc mới
│       └── validator.py                # Xác thực dữ liệu đầu vào: mã SV/GV, số lượng, mật khẩu, trường rỗng
│
└── tests/                              # TẦNG KIỂM THỬ TỰ ĐỘNG (UNIT TEST LAYER)
    ├── __init__.py                     # File rỗng định danh package tests/
    ├── test_sort.py                    # Kiểm thử Quick Sort: danh sách rỗng, một phần tử, nhiều phần tử, trùng tên
    └── test_loan.py                    # Kiểm thử nghiệp vụ: mượn hợp lệ, hết kho, quá hạn, tính tiền phạt
