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
    # Lưu ý: Nếu main.py nằm ở thư mục gốc, dùng 1 lần dirname. 
    # Nếu main.py nằm trong folder con (vd: source_code/), giữ nguyên 2 lần dirname.
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")
    
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        
    books_path = os.path.join(data_dir, "books.csv")
    users_path = os.path.join(data_dir, "users.csv")
    loans_path = os.path.join(data_dir, "loans.csv")
    waiting_path = os.path.join(data_dir, "waiting_requests.csv")
    
    return books_path, users_path, loans_path, waiting_path

def main():
    # Nhận đủ 4 đường dẫn file
    books_path, users_path, loans_path, waiting_path = get_data_paths()
    
    print("\n[Hệ thống] Đang khởi động và kết nối cơ sở dữ liệu...")
    try:
        # Bước 1: Nạp đủ 4 cấu trúc dữ liệu (Thêm waiting_queue)
        hash_map, dll, user_array, waiting_queue = data_processor.load_system_data(
            books_path, users_path, loans_path, waiting_path
        )
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
                # Truyền đủ 4 object và 4 đường dẫn để lưu file
                data_processor.save_system_data(
                    hash_map, dll, user_array, waiting_queue, 
                    books_path, users_path, loans_path, waiting_path
                )
                print("[Hệ thống] Đã đồng bộ an toàn. Tạm biệt!")
            except Exception as e:
                print(f"[!] Lỗi khi ghi file CSV: {e}")
            break
            
        # Nếu đăng nhập sai thì lặp lại
        if current_user is None:
            input("\n👉 Nhấn Enter để thử lại...")
            continue
            
        # Bước 3: Phân luồng điều hướng (Nhớ truyền thêm waiting_queue)
        if current_user.is_admin():
            menu.run_admin_menu(hash_map, dll, user_array, waiting_queue)
        else:
            menu.run_user_menu(hash_map, dll, user_array, waiting_queue, current_user)
            
        # Chốt lưu thêm một lần nữa khi User/Admin đăng xuất cho chắc cốp
        data_processor.save_system_data(
            hash_map, dll, user_array, waiting_queue, 
            books_path, users_path, loans_path, waiting_path
        )

if __name__ == "__main__":
    # Đảm bảo có thể chạy module bằng lệnh python source_code/main.py
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    main()
