"""
Mô-đun giao diện menu chính (Main Menu)
Nhiệm vụ: Vòng lặp while True điều hướng toàn bộ chức năng hệ thống.
          Hiển thị bảng ASCII, phân trang 10 dòng/trang.
          Nhận lựa chọn từ người dùng, gọi đúng hàm logic tương ứng,
          hiển thị kết quả và gọi save_system_data() sau mỗi thao tác thay đổi dữ liệu.
"""
import os
from objects.books import Book
from objects.users import User
from objects.loans import Loan

# Import các package từ các tầng khác
from interface import account_manager, validator
from storage import data_processor
from logic import search, sort, loan_manager, report

# ==========================================
# 1. CÁC HÀM TIỆN ÍCH GIAO DIỆN & LƯU DỮ LIỆU
# ==========================================
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title: str):
    clear_screen()
    print("+" + "-" * 78 + "+")
    print(f"|{title.center(78)}|")
    print("+" + "-" * 78 + "+")

def pause():
    input("\n👉 Nhấn Enter để tiếp tục...")

def _trigger_save(hash_map, dll, user_array, waiting_queue):
    """Lưu dữ liệu ngầm sau mỗi thao tác thay đổi trạng thái hệ thống."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")
    
    # Đảm bảo thư mục data tồn tại
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        
    books_path = os.path.join(data_dir, "books.csv")
    users_path = os.path.join(data_dir, "users.csv")
    loans_path = os.path.join(data_dir, "loans.csv")
    waiting_path = os.path.join(data_dir, "waiting_requests.csv")
    
    try:
        data_processor.save_system_data(hash_map, dll, user_array, waiting_queue, books_path, users_path, loans_path, waiting_path)
    except Exception as e:
        print(f"\n[!] Lỗi khi tự động lưu dữ liệu: {e}")

# ==========================================
# 2. CÁC HÀM IN BẢNG ASCII PHÂN TRANG
# ==========================================
def display_books_paginated(books):
    if not books or len(books) == 0:
        print("\n[!] Không có dữ liệu sách.")
        return

    PAGE_SIZE = 10
    total = len(books)
    w_id, w_title, w_author, w_genre, w_qty = 8, 30, 20, 15, 5

    separator = f"+{'-'*(w_id+2)}+{'-'*(w_title+2)}+{'-'*(w_author+2)}+{'-'*(w_genre+2)}+{'-'*(w_qty+2)}+"

    for i in range(0, total, PAGE_SIZE):
        chunk = books[i:i + PAGE_SIZE]
        print(separator)
        print(f"| {'Mã Sách'.ljust(w_id)} | {'Tên Sách'.ljust(w_title)} | {'Tác Giả'.ljust(w_author)} | {'Thể Loại'.ljust(w_genre)} | {'Kho'.rjust(w_qty)} |")
        print(separator)
        
        for b in chunk:
            title = (b.title[:w_title-3] + "...") if len(b.title) > w_title else b.title
            author = (b.author[:w_author-3] + "...") if len(b.author) > w_author else b.author
            genre = (b.genre[:w_genre-3] + "...") if len(b.genre) > w_genre else b.genre
            print(f"| {b.book_id.ljust(w_id)} | {title.ljust(w_title)} | {author.ljust(w_author)} | {genre.ljust(w_genre)} | {str(b.quantity).rjust(w_qty)} |")
        
        print(separator)
        if i + PAGE_SIZE < total:
            input(f"\n👉 Đang xem {i + len(chunk)}/{total}. Nhấn Enter để sang trang tiếp theo...")

def display_loans_paginated(loans):
    if not loans or len(loans) == 0:
        print("\n[!] Không có dữ liệu giao dịch.")
        return
        
    PAGE_SIZE = 10
    total = len(loans)
    
    # Đường kẻ viền chuẩn khít 100% với tổng độ rộng các cột
    separator = "+" + "-"*10 + "+" + "-"*15 + "+" + "-"*10 + "+" + "-"*12 + "+" + "-"*12 + "+" + "-"*11 + "+"
    
    for i in range(0, total, PAGE_SIZE):
        chunk = loans[i:i + PAGE_SIZE]
        
        # 1. In Header của trang
        print(separator)
        print(f"| {'Mã Phiếu':<8} | {'Mã Độc giả':<13} | {'Mã Sách':<8} | {'Ngày Mượn':<10} | {'Trạng Thái':<10} | {'Phạt(VNĐ)':>9} |")
        print(separator)
        
        # 2. In Data của trang
        for l in chunk:
            # Bắt lỗi an toàn cho thuộc tính fee hoặc overdue_fee
            fee_val = getattr(l, 'fee', getattr(l, 'overdue_fee', 0))
            fee = str(int(fee_val))
            
            # Tất cả phải dùng format string y như header
            print(f"| {l.loan_id:<8} | {l.user_id:<13} | {l.book_id:<8} | {str(l.borrow_date):<10} | {l.status:<10} | {fee:>9} |")
            
        print(separator)
        
        # 3. Chuyển trang
        if i + PAGE_SIZE < total:
            input(f"\n👉 Đang xem {i + len(chunk)}/{total}. Nhấn Enter để sang trang tiếp theo...")

# ==========================================
# 3. SUB-MENUS CỦA ADMIN
# ==========================================
def admin_manage_books(hash_map, dll, user_array, waiting_queue):
    while True:
        print_header("QUẢN LÝ KHO SÁCH (ADMIN)")
        print("  1. Thêm sách mới")
        print("  2. Sửa thông tin sách (Trừ Mã sách)")
        print("  3. Xóa sách")
        print("  4. Hiển thị danh sách kho (A-Z)")
        print("  5. Tìm kiếm sách")
        print("  0. Quay lại")
        print("-" * 80)
        choice = input("👉 Chọn tác vụ: ").strip()

        if choice == '1':
            print("\n📚 THÊM SÁCH MỚI")
            
            # 1. Nhập và kiểm tra Mã sách
            b_id = input("Mã sách: ").strip().upper()
            if not validator.validate_book_id(b_id):
                pause(); continue
                
            if hash_map.search(b_id):
                print("[!] Lỗi: Mã sách đã tồn tại.")
                pause(); continue
                
            # 2. Nhập và kiểm tra Tên sách
            title = input("Tên sách: ").strip()
            if not validator.validate_text_length(title, "Tên sách", 50):
                pause(); continue
                
            # 3. Nhập và kiểm tra Tác giả
            author = input("Tác giả: ").strip()
            if not validator.validate_person_name(author):
                pause(); continue
                
            # 4. Nhập và kiểm tra Thể loại
            genre = input("Thể loại: ").strip()
            if not validator.validate_text_length(genre, "Thể loại", 30):
                pause(); continue
                
            publisher = input("Nhà xuất bản: ").strip()
            qty_str = input("Số lượng: ").strip()

            # 5. Kiểm tra rỗng và số lượng
            if not validator.validate_non_empty({"id": b_id, "title": title, "author": author}):
                pause(); continue
                
            if not validator.validate_quantity(qty_str):
                pause(); continue

            # 6. Lưu sách
            new_book = Book(b_id, title, author, genre, publisher, int(qty_str), "active", 0)
            hash_map.insert(b_id, new_book)
            _trigger_save(hash_map, dll, user_array, waiting_queue)
            print("[✓] Thêm sách thành công!")
            pause()

        elif choice == '2':
            print("\n✏️ SỬA THÔNG TIN SÁCH")
            b_id = input("Nhập Mã sách cần sửa: ").strip().upper()
            book = hash_map.search(b_id)
            if not book:
                print("[!] Không tìm thấy sách.")
                pause(); continue
                
            print(f"Đang sửa: {book.title} (Bỏ trống nếu không muốn đổi)")
            title = input(f"Tên sách [{book.title}]: ").strip() or book.title
            author = input(f"Tác giả [{book.author}]: ").strip() or book.author
            qty_str = input(f"Số lượng [{book.quantity}]: ").strip()
            
            qty = book.quantity
            if qty_str:
                if validator.validate_quantity(qty_str):
                    qty = int(qty_str)
                else:
                    print("[!] Lỗi số lượng. Giữ nguyên giá trị cũ.")

            old_qty = book.quantity
            book.title, book.author, book.quantity = title, author, qty
            hash_map.insert(b_id, book)
            if qty > old_qty:
                loan_manager.serve_waiting_queue(hash_map, dll, user_array, waiting_queue, b_id)
            _trigger_save(hash_map, dll, user_array, waiting_queue)
            print("[✓] Cập nhật thành công!")
            pause()

        elif choice == '3':
            print("\n🗑️ XÓA SÁCH")
            b_id = input("Nhập Mã sách cần xóa: ").strip().upper()
            
            if loan_manager.is_book_on_loan(dll, b_id):
                print("[!] Từ chối xóa: Sách này đang có người mượn hoặc nợ quá hạn.")
            else:
                success = hash_map.delete(b_id)
                if success:
                    _trigger_save(hash_map, dll, user_array, waiting_queue)
                    print("[✓] Đã xóa sách khỏi hệ thống.")
                else:
                    print("[!] Không tìm thấy sách để xóa.")
            pause()

        elif choice == '4':
            print("\n📖 DANH SÁCH KHO SÁCH (A-Z)")
            books_cl = hash_map.get_all_books()
            try:
                sorted_books = sort.quicksort(books_cl, key="title")
                display_books_paginated(sorted_books)
            except AttributeError:
                # Fallback an toàn
                books_list = books_cl.to_list()
                books_list.sort(key=lambda x: x.title)
                display_books_paginated(books_list)
            pause()

        elif choice == '5':
            print("\n🔍 TÌM KIẾM SÁCH")
            keyword = input("Nhập từ khóa (Tên sách): ").strip()
            res_title = search.search_by_title(hash_map, keyword)
            display_books_paginated(res_title)
            pause()

        elif choice == '0':
            break

def admin_manage_loans(hash_map, dll, user_array, waiting_queue):
    while True:
        print_header("NGHIỆP VỤ MƯỢN TRẢ (ADMIN)")
        print("  1. Xử lý Mượn sách")
        print("  2. Xử lý Trả sách")
        print("  3. Xem toàn bộ lịch sử giao dịch")
        print("  0. Quay lại")
        print("-" * 80)
        choice = input("👉 Chọn tác vụ: ").strip()


        if choice == '1':
            print("\n📝 TẠO PHIẾU MƯỢN")
            u_id = input("Mã độc giả: ").strip()
            b_id = input("Mã sách: ").strip().upper()
            
            book = hash_map.search(b_id)
            if not book:
                print("[!] Không tìm thấy sách!")
                pause(); continue

            # Chốt chặn: Sách hết thì hỏi vào hàng đợi
            if book.quantity <= 0:
                confirm = input("⚠️ Sách đã hết! Bạn có muốn vào hàng đợi không? (y/n): ").strip().lower()
                if confirm == 'y':
                    success, msg = loan_manager.add_to_waiting_queue(waiting_queue, u_id, b_id)
                    print(f"Hệ thống: {msg}")
                else:
                    print("Hệ thống: Đã hủy.")
                pause(); continue 

            # GỌI HÀM MƯỢN VỚI ĐỦ 6 THAM SỐ
            success, msg = loan_manager.process_borrow(hash_map, dll, user_array, u_id, b_id, waiting_queue)
            
            print(f"\nHệ thống: {msg}")
            if success: _trigger_save(hash_map, dll, user_array, waiting_queue)
            pause()
        elif choice == '2':
            print("\n✅ GHI NHẬN TRẢ SÁCH")
            u_id = input("Mã độc giả: ").strip()
            b_id = input("Mã sách: ").strip().upper()
            
            # Truyền waiting_queue vào để hàm Trả sách tự động xét người chờ
            success, msg, fee = loan_manager.process_return(hash_map, dll, user_array, waiting_queue, u_id, b_id)
            
            print(f"\nHệ thống: {msg}")
            if fee > 0: print(f"⚠️ THU PHẠT: {fee} VNĐ (Trễ hạn)")
            if success: _trigger_save(hash_map, dll, user_array, waiting_queue)
            pause()

        elif choice == '3':
            print("\n📜 LỊCH SỬ GIAO DỊCH TOÀN HỆ THỐNG")
            loans = dll.get_all_transactions()
            display_loans_paginated(loans)
            pause()

        elif choice == '0':
            break

def admin_manage_readers(hash_map, dll, user_array, waiting_queue):
    while True:
        print_header("QUẢN LÝ BẠN ĐỌC (ADMIN)")
        print("  1. Tạo tài khoản bạn đọc mới (Cấp thẻ)")
        print("  2. Xem danh sách bạn đọc")
        print("  3. Xem lịch sử mượn trả của 1 bạn đọc")
        print("  0. Quay lại")
        print("-" * 80)
        choice = input("👉 Chọn tác vụ: ").strip()

        if choice == '1':
            success, msg = account_manager.create_reader(user_array)
            if success: _trigger_save(hash_map, dll, user_array, waiting_queue)
            pause()

        elif choice == '2':
            print("\n👥 DANH SÁCH BẠN ĐỌC")
            users = user_array.get_all()
            for u in users:
                print(f" - {u.user_id.ljust(10)} | {u.fullname.ljust(20)} | Loại: {u.reader_type}")
            pause()

        elif choice == '3':
            u_id = input("\nNhập Mã độc giả cần tra cứu: ").strip()
            loans = dll.get_transactions_by_user(u_id)
            display_loans_paginated(loans)
            pause()

        elif choice == '0':
            break

def admin_reports(hash_map, dll, user_array):
    while True:
        print_header("BÁO CÁO THỐNG KÊ (ADMIN)")
        print("  1. Danh sách sách đang được mượn")
        print("  2. Danh sách sách QUÁ HẠN")
        print("  3. Top 5 sách mượn nhiều nhất")
        print("  0. Quay lại")
        print("-" * 80)
        choice = input("👉 Chọn tác vụ: ").strip()

        if choice == '1':
            print("\n📖 SÁCH ĐANG ĐƯỢC MƯỢN")
            data = report.get_borrowing_loans(dll, hash_map)
            for d in data:
                print(f"Phiếu: {d['loan_id']} | Sách: {d['title']} | Người mượn: {d['user_id']}")
            pause()
            
        elif choice == '2':
            print("\n⏰ SÁCH QUÁ HẠN TRẢ")
            data = report.get_overdue_loans(dll, hash_map, user_array)
            for d in data:
                print(f"Phiếu: {d['loan_id']} | Trễ: {d['days_overdue']} ngày | Phạt: {d['temp_fee']}đ")
            pause()
            
        elif choice == '3':
            print("\n🔥 TOP 5 SÁCH HOT NHẤT")
            from structure.priority_queue import PriorityQueue
            pq = PriorityQueue()
            books = report.get_top5_books(hash_map, pq) 
            for idx, b in enumerate(books):
                print(f" Top {idx+1}: {b.title} ({b.borrow_count} lượt mượn)")
            pause()

        elif choice == '0':
            break

# ==========================================
# 4. MAIN MENUS (ĐƯỢC GỌI TỪ MAIN.PY)
# ==========================================
def run_admin_menu(hash_map, dll, user_array, waiting_queue):
    """Điểm truy cập chính của Admin."""
    while True:
        print_header("BẢNG ĐIỀU KHIỂN QUẢN TRỊ VIÊN")
        print("  1. Quản lý Sách (Kho)")
        print("  2. Nghiệp vụ Mượn/Trả")
        print("  3. Quản lý Bạn đọc")
        print("  4. Báo cáo thống kê")
        print("  0. Đăng xuất")
        print("-" * 80)
        choice = input("👉 Chọn Module: ").strip()

        if choice == '1':
            admin_manage_books(hash_map, dll, user_array, waiting_queue)
        elif choice == '2':
            admin_manage_loans(hash_map, dll, user_array, waiting_queue)
        elif choice == '3':
            admin_manage_readers(hash_map, dll, user_array, waiting_queue)
        elif choice == '4':
            admin_reports(hash_map, dll, user_array)
        elif choice == '0':
            print("\nĐang đăng xuất...")
            break
        else:
            print("\n[!] Lựa chọn không hợp lệ.")
            pause()

def run_user_menu(hash_map, dll, user_array, waiting_queue, current_user):
    """Điểm truy cập chính của Độc giả."""
    while True:
        print_header(f"CỔNG THÔNG TIN ĐỘC GIẢ | Xin chào: {current_user.fullname}")
        print("  1. Tìm kiếm sách")
        print("  2. Xem toàn bộ danh sách kho")
        print("  3. Sách tôi đang mượn (Gồm hạn trả)")
        print("  4. Phí phạt tạm tính (Nếu có)")
        print("  5. Lịch sử mượn trả cá nhân")
        print("  0. Đăng xuất")
        print("-" * 80)
        choice = input("👉 Chọn tác vụ: ").strip()

        if choice == '1':
            print("\n🔍 TÌM KIẾM SÁCH")
            keyword = input("Nhập từ khóa (Tên sách): ").strip()
            res = search.search_by_title(hash_map, keyword)
            display_books_paginated(res)
            pause()

        elif choice == '2':
            print("\n📖 KHO SÁCH (A-Z)")
            books_cl = hash_map.get_all_books()
            try:
                sorted_books = sort.quicksort(books_cl, key="title")
                display_books_paginated(sorted_books)
            except AttributeError:
                books_list = books_cl.to_list()
                books_list.sort(key=lambda x: x.title)
                display_books_paginated(books_list)
            pause()

        elif choice == '3':
            print("\n🎒 SÁCH BẠN ĐANG MƯỢN")
            loans = dll.get_transactions_by_user(current_user.user_id)
            active_loans = [l for l in loans if l.status in ("borrowing", "overdue")]
            if not active_loans:
                print("Bạn hiện không mượn cuốn sách nào.")
            else:
                for l in active_loans:
                    b = hash_map.search(l.book_id)
                    title = b.title if b else "Không rõ"
                    print(f" - Mượn: {title} | Trạng thái: {l.status} | Hạn trả: {l.due_date}")
            pause()

        elif choice == '4':
            print("\n💸 PHÍ PHẠT TẠM TÍNH TRỄ HẠN")
            loans = dll.get_transactions_by_user(current_user.user_id)
            total_fee = sum(l.overdue_fee for l in loans if l.status == "overdue")
            print(f"Tổng tiền phạt hiện tại của bạn là: {int(total_fee)} VNĐ")
            if total_fee == 0:
                print("Tuyệt vời! Bạn không có khoản phạt nào.")
            pause()

        elif choice == '5':
            print("\n📜 LỊCH SỬ MƯỢN TRẢ CÁ NHÂN")
            loans = dll.get_transactions_by_user(current_user.user_id)
            display_loans_paginated(loans)
            pause()

        elif choice == '0':
            print("\nĐang đăng xuất...")
            break
        else:
            print("\n[!] Lựa chọn không hợp lệ.")
            pause()
