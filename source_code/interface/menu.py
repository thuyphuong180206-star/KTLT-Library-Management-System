"""
Mô-đun giao diện menu chính (Main Menu)
Nhiệm vụ: Vòng lặp while True điều hướng toàn bộ chức năng hệ thống.
          Hiển thị bảng ASCII, phân trang 10 dòng/trang.
          Nhận lựa chọn từ người dùng, gọi đúng hàm logic tương ứng,
          hiển thị kết quả và gọi save_system_data() sau mỗi thao tác thay đổi dữ liệu.
Các hàm:
    - run_admin_menu(hash_map, dll, user_array)
        Menu Admin — toàn quyền:
        [1] Quản lý sách
            1.1 Thêm sách mới
            1.2 Sửa thông tin sách (không được sửa book_id)
            1.3 Xóa sách (gọi is_book_on_loan() để kiểm tra trước khi xóa) 
            1.4 Hiển thị danh sách kho (QuickSort A-Z, phân trang)
            1.5 Tìm kiếm sách (theo tên / mã / tác giả / thể loại)
        [2] Nghiệp vụ mượn/trả
            2.1 Xử lý mượn sách
            2.2 Xử lý trả sách + hiển thị tiền phạt
            2.3 Xem toàn bộ lịch sử giao dịch
        [3] Quản lý bạn đọc
            3.1 Tạo tài khoản bạn đọc mới
            3.2 Xem danh sách bạn đọc
            3.3 Xem lịch sử mượn trả của một bạn đọc
        [4] Báo cáo
            4.1 Danh sách sách đang được mượn
            4.2 Danh sách sách quá hạn
            4.3 Top 5 sách mượn nhiều nhất
        [0] Đăng xuất

    - run_user_menu(hash_map, dll, user_array, current_user)
        Menu User — chỉ đọc:
        [1] Tìm kiếm sách
        [2] Xem danh sách sách
        [3] Sách tôi đang mượn + ngày hết hạn
        [4] Phí phạt tạm tính (nếu có)
        [5] Lịch sử mượn trả cá nhân
        [0] Đăng xuất
Import: logic.search, logic.sort, logic.loan_manager, logic.report,
        interface.account_manager, interface.validator,
        storage.data_processor
Import bởi: main
"""
import os
from interface import account_manager, validator
# Import hờ các thư viện để chống lỗi, khi các bạn làm logic xong thì gỡ comment
# from storage import data_processor
# from logic import search, sort, loan_manager
from objects.books import Book
from objects.users import User

# ==========================================
# 1. CÁC HÀM TIỆN ÍCH GIAO DIỆN
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

# ==========================================
# 2. HÀM VẼ BẢNG ASCII ĐỘNG (DYNAMIC ASCII TABLE)
# ==========================================
def display_book_table_interface(books: list[Book]) -> None:
    if not books:
        print("\n[!] Không có dữ liệu sách để hiển thị.")
        return

    w_id = max(8, max((len(b.book_id) for b in books), default=8))
    w_title = min(35, max(10, max((len(b.title) for b in books), default=10)))
    w_author = min(20, max(9, max((len(b.author) for b in books), default=9)))
    w_genre = min(15, max(9, max((len(b.genre) for b in books), default=9)))
    w_qty = 5     
    w_borrow = 10 

    separator = f"+{'-'*(w_id+2)}+{'-'*(w_title+2)}+{'-'*(w_author+2)}+{'-'*(w_genre+2)}+{'-'*(w_qty+2)}+{'-'*(w_borrow+2)}+"

    print(separator)
    print(f"| {'Mã Sách'.ljust(w_id)} | {'Tên Sách'.ljust(w_title)} | {'Tác Giả'.ljust(w_author)} | {'Thể Loại'.ljust(w_genre)} | {'Kho'.rjust(w_qty)} | {'Lượt Mượn'.rjust(w_borrow)} |")
    print(separator)

    PAGE_SIZE = 15
    total_books = len(books)

    for i, b in enumerate(books):
        title = (b.title[:w_title-3] + "...") if len(b.title) > w_title else b.title
        author = (b.author[:w_author-3] + "...") if len(b.author) > w_author else b.author
        genre = (b.genre[:w_genre-3] + "...") if len(b.genre) > w_genre else b.genre

        row_id = b.book_id.ljust(w_id)
        row_title = title.ljust(w_title)
        row_author = author.ljust(w_author)
        row_genre = genre.ljust(w_genre)
        row_qty = str(b.quantity).rjust(w_qty)
        row_borrow = str(b.borrow_count).rjust(w_borrow)

        print(f"| {row_id} | {row_title} | {row_author} | {row_genre} | {row_qty} | {row_borrow} |")

        if (i + 1) % PAGE_SIZE == 0 and (i + 1) < total_books:
            print(separator)
            input(f"\n👉 Đang xem {i+1}/{total_books}. Nhấn Enter để lật sang trang tiếp theo...")
            print_header("DANH MỤC SÁCH THƯ VIỆN")
            print(separator)

    print(separator)
    print(f"Tổng số bản ghi: {total_books}")


# ==========================================
# 3. CÁC MENU CẤP 2 (SUB-MENUS)
# ==========================================
def manage_books_menu(hash_map_obj):
    while True:
        print_header("MODULE 1: QUẢN LÝ KHO SÁCH (BIÊN MỤC)")
        print("  1. Thêm sách mới vào kho")
        print("  2. Hiển thị toàn bộ kho sách")
        print("  3. Xóa sách khỏi hệ thống")
        print("  0. Quay lại Menu Quản trị viên")
        print("-" * 80)

        choice = input("👉 Chọn tác vụ (0-3): ").strip()

        if choice == '1':
            print("\n📚 THÊM SÁCH MỚI VÀO KHO")
            b_id = input("Mã sách (VD: B001): ").strip()
            title = input("Tên sách: ").strip()
            author = input("Tác giả: ").strip()
            genre = input("Thể loại: ").strip()
            publisher = input("Nhà xuất bản: ").strip()
            reg_num = input("Số ĐKCB (VD: DKCB-123456): ").strip()
            year_str = input("Năm xuất bản: ").strip()
            price_str = input("Giá tiền (VNĐ): ").strip()
            qty_str = input("Số lượng nhập kho: ").strip()

            payload = {
                "book_id": b_id, "title": title, "author": author,
                "genre": genre, "publisher": publisher, "registration_number": reg_num
            }

            if not validator.validate_book_payload(payload):
                pause()
                continue
            if not validator.validate_year(year_str) or not validator.validate_positive_float(price_str):
                pause()
                continue

            if not qty_str.isdigit() or int(qty_str) <= 0:
                print("[!] Lỗi: Số lượng phải là số nguyên lớn hơn 0.")
                pause()
                continue

            print(f"\n[Giao diện] Đã lọc lỗi xong! Đang gọi hàm đưa sách '{title}' vào Bảng băm...")
            # new_book = Book(b_id, title, author, genre, publisher, int(qty_str))
            # hash_map_obj.insert(b_id, new_book)
            # print("[✓] Thêm sách thành công!")
            pause()

        elif choice == '2':
            print("\n[Giao diện] Đang rút dữ liệu từ Bảng băm để vẽ ASCII Table...")
            # books = hash_map_obj.get_all_books()
            # display_book_table_interface(books)
            pause()

        elif choice == '3':
            print("\n🗑️ XÓA SÁCH KHỎI HỆ THỐNG")
            b_id = input("Nhập Mã sách cần xóa: ").strip()
            if not b_id:
                print("[!] Lỗi: Mã sách không được để trống.")
            else:
                print(f"\n[Giao diện] Đang gọi lệnh xóa sách '{b_id}' khỏi Bảng băm...")
                # success = hash_map_obj.delete(b_id)
                # if success:
                #     print("[✓] Đã xóa sách thành công!")
                # else:
                #     print("[!] Xóa thất bại: Không tìm thấy Mã sách.")
            pause()

        elif choice == '0':
            break
        else:
            print("\n[!] Lựa chọn không hợp lệ.")
            pause()

def manage_loans_menu(hash_map_obj, dll_sys, user_list):
    while True:
        print_header("MODULE 2: NGHIỆP VỤ MƯỢN TRẢ & GIAO DỊCH")
        print("  1. Tra cứu nhanh trạng thái sách (Còn/Hết)")
        print("  2. Ghi nhận CHO MƯỢN sách (Tạo phiếu)")
        print("  3. Ghi nhận TRẢ SÁCH & Thu tiền phạt")
        print("  4. Theo dõi Sách đang mượn & Cảnh báo Quá hạn")
        print("  0. Quay lại Menu Quản trị viên")
        print("-" * 80)

        choice = input("👉 Chọn tác vụ (0-4): ").strip()

        if choice == '1':
            print("\n🔍 TRA CỨU TRẠNG THÁI SÁCH")
            keyword = input("Nhập tên sách hoặc tác giả cần tìm: ").strip()
            if keyword:
                print(f"\n[Giao diện] Đang gửi từ khóa '{keyword}' xuống tầng Logic để tìm trong Bảng băm...")
                # results = search.search_books_by_keyword(hash_map_obj, keyword)
                # display_book_table_interface(results)
            pause()

        elif choice == '2':
            print("\n📝 TẠO PHIẾU MƯỢN SÁCH")
            user_id = input("Nhập Mã độc giả (VD: U00001): ").strip()
            book_id = input("Nhập Mã sách (VD: B001): ").strip()

            if not user_id or not book_id:
                print("\n[!] Lỗi: Mã độc giả và Mã sách không được để trống.")
            else:
                print(f"\n[Giao diện] Đang chuyển yêu cầu mượn sách ({book_id}) của độc giả ({user_id}) xuống tầng Logic...")
                # success, msg = loan_manager.process_borrow(hash_map_obj, dll_sys, user_list, user_id, book_id)
                # print(f"\nThông báo từ hệ thống: {msg}")
            pause()

        elif choice == '3':
            print("\n✅ GHI NHẬN TRẢ SÁCH")
            loan_id = input("Nhập Mã phiếu mượn (VD: L001): ").strip()

            if not loan_id:
                print("\n[!] Lỗi: Mã phiếu mượn không được để trống.")
            else:
                print(f"\n[Giao diện] Đang chuyển yêu cầu trả sách phiếu ({loan_id}) xuống tầng Logic...")
                # success, fee, msg = loan_manager.process_return(hash_map_obj, dll_sys, loan_id)
                # print(f"\nThông báo: {msg}")
                # if fee > 0:
                #     print(f"⚠️ CẢNH BÁO: Độc giả bị phạt {fee} VNĐ do nộp trễ hạn!")
            pause()

        elif choice == '4':
            print("\n⏰ DANH SÁCH QUÁ HẠN & ĐANG MƯỢN")
            print("[Giao diện] Đang quét toàn bộ Danh sách liên kết kép (DLL) để lọc phiếu...")
            # active_loans = loan_manager.get_active_and_overdue_loans(dll_sys)
            pause()

        elif choice == '0':
            break
        else:
            print("\n[!] Lựa chọn không hợp lệ.")
            pause()

# ==========================================
# 4. CÁC MENU RẼ NHÁNH CHÍNH
# ==========================================
def admin_menu(hash_map_obj, dll_sys, user_list, current_user: User):
    while True:
        print_header(f"👑 MENU QUẢN TRỊ VIÊN | Xin chào: {current_user.fullname}")
        print("  1. Quản lý Kho Sách (Thêm, Sửa, Xóa, Xem)")
        print("  2. Nghiệp vụ Mượn/Trả sách tại quầy")
        print("  3. Đổi mật khẩu cá nhân")
        print("  0. Đăng xuất")
        print("-" * 80)

        choice = input("👉 Chọn tác vụ (0-3): ").strip()

        if choice == '1':
            manage_books_menu(hash_map_obj) # Gọi menu con
        elif choice == '2':
            manage_loans_menu(hash_map_obj, dll_sys, user_list) # Gọi menu con
        elif choice == '3':
            account_manager.show_change_password_form(current_user)
            pause()
        elif choice == '0':
            print("\nĐang đăng xuất khỏi tài khoản Quản trị...")
            break
        else:
            print("\n[!] Lựa chọn không hợp lệ.")
            pause()

def reader_menu(hash_map_obj, dll_sys, current_user: User):
    while True:
        print_header(f"👤 CỔNG ĐỘC GIẢ | Xin chào: {current_user.fullname}")
        print(f"  Loại bạn đọc: {'Sinh viên' if current_user.reader_type == 'student' else 'Giảng viên'} | Hạn mức: {current_user.borrow_limit} cuốn")
        print("-" * 80)
        print("  1. Tra cứu sách trong thư viện")
        print("  2. Xem sách đang mượn cá nhân")
        print("  3. Đổi mật khẩu bảo mật")
        print("  0. Đăng xuất")
        print("-" * 80)

        choice = input("👉 Chọn tác vụ (0-3): ").strip()

        if choice == '1':
            print("\n[Đang tải danh mục sách...]")
            pause()
        elif choice == '2':
            print("\n[Đang tra cứu lịch sử trong Danh sách liên kết kép...]")
            pause()
        elif choice == '3':
            account_manager.show_change_password_form(current_user)
            pause()
        elif choice == '0':
            print("\nĐang đăng xuất khỏi Cổng thông tin...")
            break
        else:
            print("\n[!] Lựa chọn không hợp lệ.")
            pause()

# ==========================================
# 5. ENTRY POINT: ĐIỀU PHỐI LUỒNG LỆNH CHÍNH
# ==========================================
def menu_main(hash_map_obj, dll_sys, user_list: list[User], books_path: str, users_path: str, loans_path: str) -> None:
    while True:
        print_header("HỆ THỐNG QUẢN LÝ THƯ VIỆN ĐẠI HỌC")
        print("  1. Đăng nhập hệ thống")
        print("  2. Đăng ký thẻ bạn đọc mới")
        print("  0. Lưu dữ liệu và Thoát chương trình an toàn")
        print("-" * 80)

        choice = input("👉 Lựa chọn của bạn (0-2): ").strip()

        if choice == '1':
            current_user = account_manager.show_login_form(user_list)
            if current_user:
                if current_user.role == "admin":
                    admin_menu(hash_map_obj, dll_sys, user_list, current_user)
                else:
                    reader_menu(hash_map_obj, dll_sys, current_user)
            else:
                pause()

        elif choice == '2':
            account_manager.show_register_form(user_list)
            pause()

        elif choice == '0':
            print("\n[Hệ thống] Đang kích hoạt lưu dữ liệu toàn cục xuống tệp CSV...")
            try:
                # data_processor.save_system_data(hash_map_obj, dll_sys, user_list, books_path, users_path, loans_path)
                print("[Hệ thống] Đã đồng bộ an toàn. Đóng chương trình. Tạm biệt!")
            except Exception as e:
                print(f"[!] Lỗi khi đồng bộ dữ liệu: {e}")
            break
        else:
            print("\n[!] Lựa chọn không hợp lệ.")
            pause()

if __name__ == "__main__":
    dummy_users = [
        User(user_id="admin", fullname="Quản trị tối cao", password="123", role="admin"),
        User(user_id="U00001", fullname="Sinh viên A", password="123", role="user")
    ]
    menu_main(None, None, dummy_users, "books.csv", "users.csv", "loans.csv")
