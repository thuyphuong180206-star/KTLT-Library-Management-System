"""
Lớp thực thể Người dùng (User Object)
Nhiệm vụ: Khai báo cấu trúc thông tin tài khoản người dùng trong hệ thống thư viện.
Thuộc tính:
    - user_id (str)         : Mã định danh duy nhất (đồng thời là mã sinh viên/mã giảng viên)
    - fullname (str)        : Họ và tên đầy đủ
    - password (str)        : Mật khẩu tài khoản
    - role (str)            : Vai trò hệ thống ("admin" | "user")
    - reader_type (str)     : Loại bạn đọc ("student" | "lecturer")
    - borrow_limit (int)    : Hạn mức mượn tối đa (tự tính từ reader_type: SV=3, GV=5)
    - borrow_duration (int) : Số ngày được mượn (tự tính từ reader_type: SV=14, GV=30)
    - status (str)          : Trạng thái tài khoản ("active" | "inactive")
Phương thức: to_dict(), from_dict(), is_admin(), is_active(), deactivate(), activate()
Import bởi: storage.data_processor, interface.account_manager, interface.menu
"""


class User:
    """
    Thực thể đại diện cho một tài khoản người dùng trong hệ thống thư viện.
    """

    VALID_ROLES        = {"admin", "user"}
    VALID_STATUS       = {"active", "inactive"}
    VALID_READER_TYPES = {"student", "lecturer"}

    # Hạn mức mượn theo loại bạn đọc
    BORROW_LIMITS = {
        "student":  3,    # Sinh viên mượn tối đa 3 cuốn
        "lecturer": 5,    # Giảng viên mượn tối đa 5 cuốn
    }

    # Số ngày được mượn theo loại bạn đọc
    BORROW_DURATIONS = {
        "student":  14,   # Sinh viên được mượn 14 ngày
        "lecturer": 30,   # Giảng viên được mượn 30 ngày
    }

    def __init__(
        self,
        user_id: str,
        fullname: str,
        password: str,
        role: str = "user",
        reader_type: str = "student",
        status: str = "active",
    ):
        """
        Khởi tạo đối tượng User.

        Args:
            user_id (str):      Mã người dùng (mã sinh viên / mã giảng viên).
            fullname (str):     Họ tên đầy đủ.
            password (str):     Mật khẩu tài khoản.
            role (str):         Vai trò hệ thống (mặc định: "user").
            reader_type (str):  Loại bạn đọc (mặc định: "student").
            status (str):       Trạng thái tài khoản (mặc định: "active").
        """
        self.user_id         = user_id
        self.fullname        = fullname
        self.password        = password
        self.role            = role
        self.reader_type     = reader_type
        self.borrow_limit    = self.BORROW_LIMITS.get(reader_type, 3)    # tự tính từ reader_type
        self.borrow_duration = self.BORROW_DURATIONS.get(reader_type, 14) # tự tính từ reader_type
        self.status          = status

    # ------------------------------------------------------------------ #
    # Kiểm tra trạng thái — phục vụ interface.menu, logic.loan_manager   #
    # ------------------------------------------------------------------ #

    def is_admin(self) -> bool:
        """Trả về True nếu tài khoản có quyền quản trị."""
        return self.role == "admin"

    def is_active(self) -> bool:
        """Trả về True nếu tài khoản đang hoạt động."""
        return self.status == "active"

    def deactivate(self):
        """Vô hiệu hóa tài khoản."""
        self.status = "inactive"

    def activate(self):
        """Kích hoạt lại tài khoản."""
        self.status = "active"

    # ------------------------------------------------------------------ #
    # Serialization — phục vụ storage.data_processor                     #
    # ------------------------------------------------------------------ #

    def to_dict(self) -> dict:
        """Chuyển đối tượng User thành dict — phục vụ storage.data_processor khi ghi CSV."""
        return {
            "user_id":     self.user_id,
            "fullname":    self.fullname,
            "password":    self.password,
            "role":        self.role,
            "reader_type": self.reader_type,
            "status":      self.status,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        """Tạo đối tượng User từ dict đọc từ CSV — ép kiểu an toàn."""
        return cls(
            user_id     = str(data["user_id"]),
            fullname    = str(data["fullname"]),
            password    = str(data["password"]),
            role        = str(data.get("role", "user")),
            reader_type = str(data.get("reader_type", "student")),
            status      = str(data.get("status", "active")),
        )

    # ------------------------------------------------------------------ #
    # Dunder methods                                                       #
    # ------------------------------------------------------------------ #

    def __repr__(self) -> str:
        return (
            f"User(user_id={self.user_id!r}, fullname={self.fullname!r}, "
            f"role={self.role!r}, reader_type={self.reader_type!r}, "
            f"borrow_limit={self.borrow_limit}, "
            f"borrow_duration={self.borrow_duration}, status={self.status!r})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, User):
            return NotImplemented
        return self.user_id == other.user_id
