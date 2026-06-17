"""
Lớp thực thể Người dùng (User Object)
Nhiệm vụ: Khai báo cấu trúc thông tin tài khoản người dùng trong hệ thống thư viện.
Thuộc tính:
    - user_id (str)         : Mã định danh duy nhất (MSSV hoặc mã giảng viên)
    - fullname (str)        : Họ và tên đầy đủ
    - password (str)        : Mật khẩu tài khoản
    - role (str)            : Vai trò hệ thống ("admin" | "user")
    - reader_type (str)     : Loại bạn đọc ("student" | "lecturer" | "" nếu là admin)
    - borrow_limit (int)    : Hạn mức mượn tối đa (SV=3, GV=5, admin=0)
    - borrow_duration (int) : Số ngày được mượn (SV=14, GV=30, admin=0)
Phương thức: to_dict(), from_dict(), is_admin()
Import bởi: storage.data_processor, interface.account_manager, interface.menu
"""


class User:
    """
    Thực thể đại diện cho một tài khoản người dùng trong hệ thống thư viện.
    """

    VALID_ROLES        = {"admin", "user"}
    VALID_READER_TYPES = {"student", "lecturer", ""}

    BORROW_LIMITS = {
        "student":  3,
        "lecturer": 5,
        "":         0,   # admin không mượn sách
    }

    BORROW_DURATIONS = {
        "student":  14,
        "lecturer": 30,
        "":         0,   # admin không mượn sách
    }

    def __init__(
        self,
        user_id: str,
        fullname: str,
        password: str,
        role: str = "user",
        reader_type: str = "student",
    ):
        """
        Khởi tạo đối tượng User.

        Args:
            user_id (str):      Mã người dùng (MSSV / mã GV / "admin").
            fullname (str):     Họ tên đầy đủ.
            password (str):     Mật khẩu tài khoản.
            role (str):         Vai trò hệ thống (mặc định: "user").
            reader_type (str):  Loại bạn đọc (mặc định: "student").
                                Admin để "" vì không áp dụng hạn mức mượn.
        """
        self.user_id         = user_id
        self.fullname        = fullname
        self.password        = password
        self.role            = role
        self.reader_type     = reader_type
        self.borrow_limit    = self.BORROW_LIMITS.get(reader_type, 3)
        self.borrow_duration = self.BORROW_DURATIONS.get(reader_type, 14)

    # ------------------------------------------------------------------ #
    # Kiểm tra vai trò                                                    #
    # ------------------------------------------------------------------ #

    def is_admin(self) -> bool:
        """Trả về True nếu tài khoản có quyền quản trị."""
        return self.role == "admin"

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
        )

    # ------------------------------------------------------------------ #
    # Dunder methods                                                       #
    # ------------------------------------------------------------------ #

    def __repr__(self) -> str:
        return (
            f"User(user_id={self.user_id!r}, fullname={self.fullname!r}, "
            f"role={self.role!r}, reader_type={self.reader_type!r}, "
            f"borrow_limit={self.borrow_limit}, borrow_duration={self.borrow_duration})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, User):
            return NotImplemented
        return self.user_id == other.user_id
