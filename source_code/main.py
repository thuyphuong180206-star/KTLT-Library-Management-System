"""
Điểm khởi chạy hệ thống (Entry Point)
Nhiệm vụ: Khởi động chương trình, nạp dữ liệu từ CSV lên RAM, điều hướng đến menu Admin hoặc User.
Luồng chạy:
    1. Gọi load_system_data() → nạp BookHashMap, TransactionList, UserArray
    2. Hiển thị màn hình đăng nhập (gọi account_manager.login())
    3. Phân luồng: role="admin" → run_admin_menu() | role="user" → run_user_menu()
Import: storage.data_processor, interface.menu, interface.account_manager
"""
import os
import sys
import datetime

# ==========================================
# 1. CẤU HÌNH ĐƯỜNG DẪN ĐỘNG (SYS PATH INJECTION)
# ==========================================
# Xác định vị trí thư mục hiện tại đang chứa file main.py (thư mục source_code/)
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Đẩy thư mục source_code/ vào biến môi trường hệ thống để Python nhận diện các package nội bộ
if CURRENT_DIR not in sys.path:
    sys.path.append(CURRENT_DIR)

# Import các module nội bộ sau khi đã tiêm đường dẫn
try:
    from storage import data_processor
    from interface import menu
except ModuleNotFoundError as e:
    print(f"\n[!] LỖI KHỞI ĐỘNG CỐT LÕI: {e}")
    print("Vui lòng đảm bảo bạn đang chạy file main.py trong đúng cấu trúc thư mục dự án.")
    sys.exit(1)

# ==========================================
# 2. KHAI BÁO HẰNG SỐ ĐƯỜNG DẪN TỆP VẬT LÝ
# ==========================================
# Lùi lại một cấp từ source_code/ để ra thư mục gốc Library-Management-System/
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)

DATA_DIR = os.path.join(PROJECT_ROOT, "data")
BOOKS_CSV = os.path.join(DATA_DIR, "books.csv")
USERS_CSV = os.path.join(DATA_DIR, "users.csv")
LOANS_CSV = os.path.join(DATA_DIR, "loans.csv")

# ==========================================
# 3. HÀM KHỞI CHẠY CHÍNH (MAIN ROUTINE)
# ==========================================
def main():
    print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Đang khởi động hệ thống Thư viện...")
    
    # Kiểm tra và tự động khởi tạo thư mục data/ nếu lần đầu clone Git về chưa có
    if not os.path.exists(DATA_DIR):
        try:
            os.makedirs(DATA_DIR)
            print(f"[!] Thư mục lưu trữ '{DATA_DIR}' chưa tồn tại. Hệ thống đã tự động tạo mới.")
        except OSError as e:
            print(f"[!] Không thể tạo thư mục lưu trữ: {e}")
            sys.exit(1)

    try:
        # BƯỚC 1: Nạp toàn bộ dữ liệu từ tệp vật lý lên RAM phẳng
        hash_map_obj, dll_sys, user_list = data_processor.load_system_data(
            BOOKS_CSV, USERS_CSV, LOANS_CSV
        )
        
        # BƯỚC 2: Chuyển giao bộ nhớ RAM và quyền điều khiển luồng cho Tầng Giao diện
        menu.menu_main(
            hash_map_obj, 
            dll_sys, 
            user_list, 
            BOOKS_CSV, 
            USERS_CSV, 
            LOANS_CSV
        )

    except KeyboardInterrupt:
        # Chốt chặn phòng ngừa: Người dùng bấm Ctrl+C để ép dừng chương trình
        print("\n\n[!] CẢNH BÁO: Hệ thống bị ngắt đột ngột (KeyboardInterrupt).")
        print("Đang tiến hành đồng bộ dữ liệu RAM xuống tệp CSV để tránh mất mát...")
        try:
            data_processor.save_system_data(
                hash_map_obj, dll_sys, user_list, BOOKS_CSV, USERS_CSV, LOANS_CSV
            )
            print("Đã sao lưu dữ liệu an toàn. Đóng chương trình.")
        except Exception as save_err:
            print(f"[!] Lỗi nghiêm trọng khi sao lưu khẩn cấp: {save_err}")
            
    except Exception as e:
        print(f"\n[!] Hệ thống gặp lỗi Runtime không xác định: {e}")

# ==========================================
# ĐIỂM KÍCH HOẠT DUY NHẤT
# ==========================================
if __name__ == "__main__":
    main()
