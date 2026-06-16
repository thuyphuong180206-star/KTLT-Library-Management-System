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

