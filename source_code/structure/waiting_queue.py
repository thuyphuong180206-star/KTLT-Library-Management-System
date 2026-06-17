"""
Cấu trúc dữ liệu Hàng đợi chờ mượn sách (Waiting Queue — FIFO)
Nhiệm vụ: Lưu danh sách bạn đọc đang chờ mượn một đầu sách đã hết kho.
          Người đăng ký trước được phục vụ trước (FIFO).
Cài đặt: Queue liên kết đơn tự cài — không dùng list có sẵn của Python.
Các phương thức:
    - enqueue(request_obj) : Thêm yêu cầu chờ vào cuối hàng, O(1)
    - dequeue()            : Lấy yêu cầu đầu hàng ra, O(1)
    - peek()               : Xem yêu cầu đầu hàng mà không xóa, O(1)
    - is_empty()           : Kiểm tra hàng rỗng, O(1)
    - size()               : Trả về số lượng yêu cầu đang chờ, O(1)
    - to_list()            : Xuất toàn bộ hàng đợi ra list để hiển thị, O(n)
Import bởi: storage.data_processor, logic.loan_manager
"""
