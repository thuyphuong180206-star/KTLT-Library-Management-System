"""
MÔ-ĐUN THỰC THỂ ĐỐI TƯỢNG TÀI KHOẢN (OBJECT LAYER - USER ENTITY)
Nhiệm vụ: Định nghĩa lớp User để mô hình hóa thông tin tài khoản độc giả và quản trị viên thư viện.

Các thuộc tính bảo vệ (Private Attributes):
    - __user_id: str                   (Mã định danh duy nhất của người dùng, chuẩn Regex: ^U\d{5}$)
    - __username: str                  (Tên đăng nhập hệ thống, chuỗi không rỗng, không chứa khoảng trắng)
    - __password: str                  (Mật khẩu bảo mật mã hóa chuỗi)
    - __fullname: str                  (Họ và tên đầy đủ của chủ thẻ)
    - __role: str                      (Vai trò hệ thống, tập đóng giá trị: "admin" hoặc "reader")
    - __priority_level: str            (Hạng tài khoản điều tiết hàng đợi, tập đóng: "VIP", "Standard", "Restricted")

Hệ thống phương thức bắt buộc cài đặt trực tiếp:
    - __init__(self, user_id: str, username: str, password: str, fullname: str, role: str, priority_level: str) -> None
    - Getters/Setters tương ứng cho toàn bộ 6 thuộc tính ẩn trên (Tuân thủ chuẩn đóng gói snake_case).
    - to_dict(self) -> dict[str, Any]: Đóng gói thuộc tính thành từ điển phục vụ lưu trữ file CSV.
    - from_dict(cls, data: dict[str, Any]) -> 'User' (Classmethod): Tạo thực thể User sạch từ dữ liệu thô.
"""
