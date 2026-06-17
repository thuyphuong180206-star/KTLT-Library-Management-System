"""
Mô-đun điều phối nghiệp vụ mượn/trả sách (Loan Manager)
Nhiệm vụ: Xử lý toàn bộ logic nghiệp vụ mượn sách, trả sách và tính tiền phạt.
Ràng buộc: Không chứa lệnh input/print. Trả về tuple (bool, str) thông báo kết quả.
Hằng số phạt:
    OVERDUE_FEE = {"student": 2000, "lecturer": 1000}  # VNĐ/ngày
Các hàm:
    - process_borrow(hash_map, dll, user_array, user_id, book_id)
        Xử lý mượn sách. Kiểm tra theo thứ tự:
            1. User tồn tại không?
            2. Sách tồn tại không?
            3. User có đang nợ phiếu "overdue" không? → từ chối
            4. User có đang mượn quá borrow_limit không? → từ chối
            5. User có đang mượn chính cuốn này không? → từ chối
            6. Sách có đang lưu hành không (status == "active")? → từ chối nếu "inactive"
7. Sách còn trong kho không (quantity > 0)? 
       Nếu hợp lệ: tạo Loan (due_date tự tính), thêm vào DLL, giảm quantity đi 1, tăng borrow_count lên 1. 
        Trả về: (bool, str)

    - process_return(hash_map, dll, user_array, user_id, book_id)
        Xử lý trả sách.
        Tìm phiếu gần nhất có status="borrowing" hoặc status="overdue" khớp user_id + book_id
        Tính tiền phạt = số ngày quá hạn × đơn giá theo reader_type.
        Cập nhật phiếu: return_date, status="returned", overdue_fee.
        Tăng quantity sách lên 1. 
        Trả về: (bool, str, float) — (thành công, thông báo, tiền phạt)

    - calculate_overdue_fee(loan, user)
        Tính tiền phạt tạm tính cho phiếu chưa trả.
        Dùng cho tính năng xem phí real-time của user.
        Trả về: float (VNĐ)
    - is_book_on_loan(dll, book_id)
Kiểm tra sách có đang được mượn không bằng cách duyệt DLL.
Tìm phiếu có book_id khớp và status="borrowing" hoặc "overdue".
Dùng cho chức năng xóa sách ở interface.menu.
Trả về: bool 
Import: logic.search, objects.loans.Loan
Import bởi: interface.menu
"""
