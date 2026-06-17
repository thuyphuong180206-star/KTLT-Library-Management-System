"""
Mô-đun báo cáo thống kê (Report Engine)
Nhiệm vụ: Tổng hợp và trả về dữ liệu báo cáo phục vụ hiển thị.
Ràng buộc: Không chứa lệnh input/print. Trả về dữ liệu thô để interface hiển thị.
Các hàm:
    - get_borrowing_loans(dll, hash_map)
        Lấy tất cả phiếu có status="borrowing" kèm thông tin tên sách.
        Phục vụ: "Danh sách sách đang được mượn".
        Trả về: list[dict]

    - get_overdue_loans(dll, hash_map, user_array)
        Lấy phiếu status="borrowing" mà due_date < ngày hôm nay.
        Tự động cập nhật status → "overdue" ngay khi phát hiện.
        Kèm số ngày quá hạn và tiền phạt tạm tính.
        Phục vụ: "Danh sách sách quá hạn".
        Trả về: list[dict]

    - get_top5_books(hash_map, pq)
        Đẩy toàn bộ sách có borrow_count > 0 vào PriorityQueue.
        Gọi peek_top_n(5) lấy top 5 sách mượn nhiều nhất.
        Phục vụ: "Top 5 sách được mượn nhiều nhất".
        Trả về: list[Book]
Import: structure.priority_queue.PriorityQueue
Import bởi: interface.menu
"""
