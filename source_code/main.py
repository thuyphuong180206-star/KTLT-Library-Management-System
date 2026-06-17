"""
Điểm khởi chạy hệ thống (Entry Point)
Nhiệm vụ: Khởi động chương trình, nạp dữ liệu từ CSV lên RAM, điều hướng đến menu Admin hoặc User.
"""

import os
import sys

# Import các package theo đúng cấu trúc thư mục
from storage import data_processor
from interface import account_manager, menu

def get_data_paths():
    """Hàm phụ trợ: Định vị hoặc tạo thư mục chứa file CSV an toàn trên mọi hệ điều hành."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")
    
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        
    books_path = os.path.join(data_dir, "books.csv")
    users_path = os.path.join(data_dir, "users.csv")
    loans_path = os.path.join(data_dir, "loans.csv")
    
    return books_path, users_path, loans_path

def main():
    books_path, users_path, loans_path = get_data_paths()
    
    print("\n[Hệ thống] Đang khởi động và kết nối cơ sở dữ liệu...")
    try:
        # Bước 1: Gọi load_system_data() → nạp BookHashMap, TransactionList, UserArray
        hash_map, dll, user_array = data_processor.load_system_data(books_path, users_path, loans_path)
    except Exception as e:
        print(f"[!] Lỗi nghiêm trọng khi nạp hệ thống: {e}")
        sys.exit(1)

    # Vòng lặp duy trì phần mềm
    while True:
        # Làm sạch màn hình trước khi hiện form đăng nhập
        os.system('cls' if os.name == 'nt' else 'clear')
        print("+" + "-" * 78 + "+")
        print(f"|{'HỆ THỐNG QUẢN LÝ THƯ VIỆN ĐẠI HỌC'.center(78)}|")
        print("+" + "-" * 78 + "+")
        print(" (Gõ 'exit' hoặc '0' ở ô Tài khoản để tắt phần mềm)\n")
        
        # Bước 2: Hiển thị màn hình đăng nhập
        current_user = account_manager.login(user_array)
        
        # Xử lý thoát chương trình
        if current_user == "EXIT_SIGNAL":
            print("\n[Hệ thống] Đang lưu dữ liệu toàn cục...")
            try:
                data_processor.save_system_data(hash_map, dll, user_array, books_path, users_path, loans_path)
                print("[Hệ thống] Đã đồng bộ an toàn. Tạm biệt!")
            except Exception as e:
                print(f"[!] Lỗi khi ghi file CSV: {e}")
            break
            
        # Nếu đăng nhập sai thì lặp lại (hàm login đã tự in câu chửi rồi)
        if current_user is None:
            input("\n👉 Nhấn Enter để thử lại...")
            continue
            
        # Bước 3: Phân luồng điều hướng
        if current_user.role == "admin":
            # Chạy menu quản trị viên
            menu.run_admin_menu(hash_map, dll, user_array)
        else:
            # Chạy menu độc giả
            menu.run_user_menu(hash_map, dll, user_array, current_user)
            
        # Docstring của menu.py yêu cầu: gọi save_system_data() SAU MỖI thao tác thay đổi.
        # Ở đây ta có thể chốt lưu thêm một lần nữa khi User/Admin đăng xuất khỏi vòng lặp của họ cho chắc cốp.
        data_processor.save_system_data(hash_map, dll, user_array, books_path, users_path, loans_path)

if __name__ == "__main__":
    # Đảm bảo có thể chạy module bằng lệnh python source_code/main.py
    # tự động nhận diện module cha để tránh lỗi ModuleNotFoundError
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    main()
