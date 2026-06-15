"""
BỘ QUẢN LÝ QUY TẮC NGHIỆP VỤ THƯ VIỆN LÕI (LOGIC LAYER - BUSINESS MANAGER)
Nhiệm vụ: Quản lý logic thay đổi số lượng kho RAM, tính phí phạt lũy tiến hình phạt nặng ngày trễ hạn, điều tiết thứ hạng độc giả.
Quy tắc kiến trúc: Không chứa lệnh nhập xuất chuỗi thô (print/input), tương tác trực tiếp hạ tầng bộ nhớ RAM phẳng.

Các hàm bắt buộc phải viết trực tiếp:
    - process_borrow(hash_map_obj: BookHashMap, dll_sys: TransactionList, user_id: str, book_id: str) -> dict[str, Any]:
        + Xử lý: Tra cứu sách trên RAM qua hash_map_obj.search(book_id). Kiểm tra điều kiện quantity > 0. Nếu thỏa mãn, thực hiện gán:
          trừ 1 số lượng tồn kho (set_quantity), tăng 1 lượt mượn tích lũy (set_borrow_count). Khởi tạo thực thể Loan mới (status="borrowing", borrow_date=ngày hiện tại),
          gọi phương thức nạp dữ liệu dll_sys.add_transaction(new_loan) đẩy vào đuôi cấu trúc danh sách liên kết kép lịch sử.
        + Kết quả trả về: Từ điển từ hiệu phản hồi trạng thái logic {"success": bool, "message": str}.

    - process_return(hash_map_obj: BookHashMap, dll_sys: TransactionList, user_list: list[User], user_id: str, book_id: str, return_date_str: str) -> dict[str, Any]:
        + Xử lý: Duyệt danh sách liên kết kép lịch sử tìm phiếu Loan có trạng thái "borrowing" khớp mã user và sách. Cộng lại 1 đơn vị quantity kho RAM.
          Gọi thư viện datetime để tính khoảng cách ngày thực tế: delta_days = return_date - borrow_date.
          Áp công thức tính phạt lũy tiến:
             * Nếu delta_days <= 14: fee = 0
             * Nếu 14 < delta_days <= 21: fee = (delta_days - 14) * 5,000
             * Nếu delta_days > 21: fee = 35,000 + (delta_days - 21) * 15,000. Đồng thời duyệt mảng user_list, tìm đối tượng độc giả và gán set_priority_level("Restricted").
        + Kết quả trả về: Từ điển chứa số liệu tất toán: {"success": bool, "overdue_days": int, "fee": float, "account_status": str}.
"""