"""
Kiểm thử nghiệp vụ mượn/trả sách (Unit Test — Loan)
Nhiệm vụ: Xác thực tính đúng đắn của các hàm nghiệp vụ cốt lõi.
Các test case:
    - test_borrow_success          : Mượn hợp lệ → thành công
    - test_borrow_out_of_stock     : Sách hết kho → từ chối
    - test_borrow_overdue_debt     : Đang nợ quá hạn → từ chối
    - test_borrow_exceed_limit     : Vượt hạn mức mượn → từ chối
    - test_return_no_overdue       : Trả đúng hạn → phí phạt = 0
    - test_return_with_overdue_fee : Trả trễ 3 ngày (SV) → phí = 6.000 VNĐ
Import: logic.loan_manager, objects.books.Book, objects.users.User,
        objects.loans.Loan, structure.hash_map.BookHashMap,
        structure.doubly_linked_list.TransactionList,
        structure.user_array.UserArray
"""
