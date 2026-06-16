"""
MÔ-ĐUN ĐIỀU PHỐI DÒNG LỆNH VÀ XUẤT BẢNG ASCII TABLE (INTERFACE LAYER - MAIN ROUTER)
Nhiệm vụ: Nơi duy nhất tổ chức cấu trúc vòng lặp lặp vô hạn `while True` để giữ luồng ứng dụng và vẽ khung bảng ASCII dữ liệu vuông vắn.
Quy tắc kiến trúc: Điều phối luồng lệnh bằng cấu trúc rẽ nhánh điều kiện ứng với phím bấm của Admin và Reader. Gọi hàm đa tầng từ gói logic/ và storage/.
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
    """
    Giải thuật hiển thị bảng ASCII với độ rộng cột động (Max length) và phân trang.
    """
    if not books:
        print("\n[!] Không có dữ liệu sách để hiển thị.")
        return

    # 1. Tính toán độ rộng lớn nhất (Max length) cho các cột văn bản
    # Lấy len của chuỗi dài nhất trong mảng, có giới hạn kích thước tối đa để không vỡ màn hình
    w_id = max(8, max((len(b.book_id) for b in books), default=8))
    w_title = min(35, max(10, max((len(b.title) for b in books), default=10)))
    w_author = min(20, max(9, max((len(b.author) for b in books), default=9)))
    w_genre = min(15, max(9, max((len(b.genre) for b in books), default=9)))
    w_qty = 5     # Cột số lượng luôn cố định
    w_borrow = 10 # Cột lượt mượn cố định

    # 2. Tạo chuỗi đường viền phân cách
    separator = f"+{'-'*(w_id+2)}+{'-'*(w_title+2)}+{'-'*(w_author+2)}+{'-'*(w_genre+2)}+{'-'*(w_qty+2)}+{'-'*(w_borrow+2)}+"

    # In Header
    print(separator)
    print(f"| {'Mã Sách'.ljust(w_id)} | {'Tên Sách'.ljust(w_title)} | {'Tác Giả'.ljust(w_author)} | {'Thể Loại'.ljust(w_genre)} | {'Kho'.rjust(w_qty)} | {'Lượt Mượn'.rjust(w_borrow)} |")
    print(separator)

    # 3. Duyệt mảng và phân trang
    PAGE_SIZE = 15
    total_books = len(books)
    
    for i, b in enumerate(books):
        # Cắt chuỗi nếu vượt quá giới hạn hiển thị (cộng thêm dấu '...')
        title = (b.title[:w_title-3] + "...") if len(b.title) > w_title else b.title
        author = (b.author[:w_author-3] + "...") if len(b.author) > w_author else b.author
        genre = (b.genre[:w_genre-3] + "...") if len(b.genre) > w_genre else b.genre

        # Ép kiểu dữ liệu hiển thị (chữ dùng ljust, số dùng rjust)
        row_id = b.book_id.ljust(w_id)
        row_title = title.ljust(w_title)
        row_author = author.ljust(w_author)
        row_genre = genre.ljust(w_genre)
        row_qty = str(b.quantity).rjust(w_qty)
        row_borrow = str(b.borrow_count).rjust(w_borrow)

        print(f"| {row_id} | {row_title} | {row_author} | {row_genre} | {row_qty} | {row_borrow} |")
        
        # Xử lý Phân trang (Pagination)
        if (i + 1) % PAGE_SIZE == 0 and (i + 1) < total_books:
            print(separator)
            input(f"\n👉 Đang xem {i+1}/{total_books}. Nhấn Enter để lật sang trang tiếp theo...")
            print_header("DANH MỤC SÁCH THƯ VIỆN")
            print(separator)
            
    print(separator)
    print(f"Tổng số bản ghi: {total_books}")


# ==========================================
# 3. CÁC MENU RẼ NHÁNH
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
            print("\n[Đang gọi Module Quản lý Kho sách...]")
            # test hiển thị mảng sách: 
            # books = hash_map_obj.get_all_books()
            # display_book_table_interface(books)
            pause()
        elif choice == '2':
            print("\n[Đang gọi Module Mượn/Trả...]")
            pause()
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
# 4. ENTRY POINT: ĐIỀU PHỐI LUỒNG LỆNH CHÍNH
# ==========================================
def menu_main(hash_map_obj, dll_sys, user_list: list[User], books_path: str, users_path: str, loans_path: str) -> None:
    """
    Vòng lặp vô hạn giữ ứng dụng chạy liên tục. Điều phối luồng và đồng bộ dữ liệu lúc tắt.
    """
    while True:
        print_header("HỆ THỐNG QUẢN LÝ THƯ VIỆN ĐẠI HỌC")
        print("  1. Đăng nhập hệ thống")
        print("  2. Đăng ký thẻ bạn đọc mới")
        print("  0. Lưu dữ liệu và Thoát chương trình an toàn")
        print("-" * 80)
        
        choice = input("👉 Lựa chọn của bạn (0-2): ").strip()
        
        if choice == '1':
            # Gọi hàm đăng nhập từ account_manager
            current_user = account_manager.show_login_form(user_list)
            
            # Điều hướng phân quyền
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
                # Kích hoạt lưu dữ liệu theo chuẩn kiến trúc
                # data_processor.save_system_data(hash_map_obj, dll_sys, user_list, books_path, users_path, loans_path)
                print("[Hệ thống] Đã đồng bộ an toàn. Đóng chương trình. Tạm biệt!")
            except Exception as e:
                print(f"[!] Lỗi khi đồng bộ dữ liệu: {e}")
            break
        else:
            print("\n[!] Lựa chọn không hợp lệ.")
            pause()

# Block chạy độc lập để tự test (Nạp sẵn 1 vài user ảo)
if __name__ == "__main__":
    dummy_users = [
        User(user_id="admin", fullname="Quản trị tối cao", password="123", role="admin"),
        User(user_id="U00001", fullname="Sinh viên A", password="123", role="user")
    ]
    menu_main(None, None, dummy_users, "books.csv", "users.csv", "loans.csv")
