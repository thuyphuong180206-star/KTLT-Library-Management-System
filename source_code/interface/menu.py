"""
MÔ-ĐUN ĐIỀU PHỐI DÒNG LỆNH VÀ XUẤT BẢNG ASCII TABLE (INTERFACE LAYER - MAIN ROUTER)
Nhiệm vụ: Nơi duy nhất tổ chức cấu trúc vòng lặp lặp vô hạn `while True` để giữ luồng ứng dụng và vẽ khung bảng ASCII dữ liệu vuông vắn.
Quy tắc kiến trúc: Điều phối luồng lệnh bằng cấu trúc rẽ nhánh điều kiện ứng với phím bấm của Admin và Reader. Gọi hàm đa tầng từ gói logic/ và storage/.

Các hàm bắt buộc phải viết trực tiếp:
    - display_book_table_interface(books: list[Book]) -> None:
        + Giải thuật hiển thị: Nhận mảng phẳng đối tượng sách từ tầng Logic. Tính toán độ rộng lớn nhất của chuỗi dữ liệu trong từng cột (Max length).
          Sử dụng phương thức định dạng chuỗi văn bản `.ljust()` cho trường chữ (Tên sách, Tác giả, NXB, Số ĐKCB) và `.rjust()` cho trường số (Giá tiền, Số lượng, Năm)
          để đóng khung lưới vuông vắn qua các ký tự (| , - , +) chuyên nghiệp. Tích hợp giải pháp phân trang (Pagination) để chống trôi màn hình.
          
    - menu_main(hash_map_obj: BookHashMap, dll_sys: TransactionList, user_list: list[User], books_path: str, users_path: str, loans_path: str) -> None:
        + Xử lý: Vòng lặp vô hạn giữ ứng dụng chạy liên tục. Gọi hàm đăng nhập. Nếu role là "admin", định tuyến hiển thị Menu Quản trị viên gồm đầy đủ các tính năng con;
          Nếu role là "reader", điều hướng sang Menu Độc giả cá nhân. Khi người dùng bấm phím lệnh điều hướng số 0 (Thoát an toàn), vòng lặp kết thúc, kích hoạt gọi lệnh
          data_processor.save_system_data(...) đồng bộ toàn cục bộ nhớ xuống file CSV trước khi tắt luồng phần mềm.
"""
