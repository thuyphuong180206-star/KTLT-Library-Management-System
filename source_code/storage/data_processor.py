"""
MÔ-ĐUN LƯU TRỮ VÀ KHÔI PHỤC SAI SÓT TỆP VẬT LÝ CSV (STORAGE LAYER)
Nhiệm vụ: Đọc/Ghi cơ sở dữ liệu tệp phẳng, kiểm soát lỗi ngoại lệ I/O vật lý (Lập trình phòng ngừa lỗi).
Ràng buộc: Gọi phương thức from_dict() và to_dict() từ tầng Object. Tuyệt đối không chứa logic menu hay thuật toán nghiệp vụ.

Các hàm bắt buộc phải viết trực tiếp (Không dùng Stub):
    - load_system_data(books_path: str, users_path: str, loans_path: str) -> tuple[BookHashMap, TransactionList, list[User]]:
        + Tham số đầu vào: Chuỗi đường dẫn tuyệt đối đến 3 file CSV lưu trữ hệ thống.
        + Logic phòng ngừa lỗi: Bọc khối lệnh trong try...except FileNotFoundError. Nếu mất tệp tin vật lý, hệ thống
          tự khởi tạo file mới chỉ chứa dòng tiêu đề (Header row) chuẩn và trả về bộ cấu trúc RAM trống sạch.
          Duyệt từng dòng trong file thông qua thư viện csv.reader, bọc khối xử lý trong try...except (ValueError, IndexError).
          Nếu phát hiện dòng lỗi do can thiệp bên ngoài (sai kiểu số, thiếu cột), lập tức kích hoạt ghi log mô tả lỗi (gồm tên file,
          nội dung dòng hỏng) vào tệp 'data/system_error.log', đồng thời chạy lệnh 'continue' để bỏ qua dòng lỗi đó, cứu vãn toàn bộ các dữ liệu chuẩn còn lại.
        + Kết quả trả về: Bộ ba tham chiếu đối tượng cấu trúc dữ liệu đã nạp đầy RAM: (hash_map_obj, dll_sys, user_list).

    - save_system_data(hash_map_obj: BookHashMap, dll_sys: TransactionList, user_list: list[User], books_path: str, users_path: str, loans_path: str) -> None:
        + Tham số đầu vào: Các tham chiếu cấu trúc RAM hiện hành và đường dẫn vật lý file đích.
        + Xử lý: Quét qua bộ nhớ RAM, chuyển đổi trạng thái bằng to_dict() của từng thực thể, thực hiện ghi đè toàn cục (Overwrite sync) xuống ổ đĩa cứng.
        + Kết quả trả về: Trạng thái None.
"""