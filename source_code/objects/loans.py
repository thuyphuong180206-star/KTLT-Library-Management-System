"""
Lớp thực thể Phiếu mượn sách (Loan Object)
Nhiệm vụ: Khai báo cấu trúc thông tin của một phiếu giao dịch mượn/trả sách.
Thuộc tính:
    - loan_id (str)            : Mã phiếu mượn duy nhất (ví dụ: "L001")
    - user_id (str)            : Mã bạn đọc thực hiện mượn
    - book_id (str)            : Mã sách được mượn
    - borrow_date (date)       : Ngày mượn sách
    - due_date (date)          : Ngày hết hạn trả (tính từ borrow_date theo hạn mức bạn đọc)
    - return_date (date|None)  : Ngày trả thực tế (None nếu chưa trả)
    - status (str)             : Trạng thái ("borrowing" | "returned" | "overdue")
    - overdue_fee (float)      : Tiền phạt quá hạn (đơn vị: VNĐ, mặc định 0.0)
Phương thức: to_dict(), from_dict(), _parse_date(), __repr__, __eq__
Import bởi: storage.data_processor, logic.loan_manager
"""

from datetime import date, datetime
from typing import Optional


class Loan:
    """
    Thực thể đại diện cho một phiếu giao dịch mượn/trả sách.
    """

    VALID_STATUSES = {"borrowing", "returned", "overdue"}
    DATE_FORMAT    = "%Y-%m-%d"

    def __init__(
        self,
        loan_id: str,
        user_id: str,
        book_id: str,
        borrow_date: date,
        due_date: Optional[date] = None,
        return_date: Optional[date] = None,
        status: str = "borrowing",
        overdue_fee: float = 0.0,
    ):
        """
        Khởi tạo đối tượng Loan.

        Args:
            loan_id (str)           : Mã phiếu mượn duy nhất.
            user_id (str)           : Mã bạn đọc.
            book_id (str)           : Mã sách được mượn.
            borrow_date (date)      : Ngày mượn sách.
            due_date (date|None)    : Ngày hết hạn trả (mặc định: None, do loan_manager tính).
            return_date (date|None) : Ngày trả thực tế (mặc định: None nếu chưa trả).
            status (str)            : Trạng thái phiếu (mặc định: "borrowing").
            overdue_fee (float)     : Tiền phạt quá hạn (mặc định: 0.0).
        """
        self.loan_id     = loan_id
        self.user_id     = user_id
        self.book_id     = book_id
        self.borrow_date = borrow_date
        self.due_date    = due_date
        self.return_date = return_date
        self.status      = status
        self.overdue_fee = overdue_fee

    # ------------------------------------------------------------------ #
    # Serialization — phục vụ storage.data_processor                     #
    # ------------------------------------------------------------------ #

    def to_dict(self) -> dict:
        """Chuyển đối tượng Loan thành dict — phục vụ storage.data_processor khi ghi CSV."""
        def format_date(value):
            if value is None or value == "":
                return ""
            if isinstance(value, str):
                return value
            return value.strftime(self.DATE_FORMAT)

        return {
            "loan_id":     self.loan_id,
            "user_id":     self.user_id,
            "book_id":     self.book_id,
            "borrow_date": format_date(self.borrow_date),
            "due_date":    format_date(self.due_date),      # ← THÊM MỚI
            "return_date": format_date(self.return_date),
            "status":      self.status,
            "overdue_fee": self.overdue_fee,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Loan":
        """Tạo đối tượng Loan từ dict đọc từ CSV — ép kiểu an toàn."""
        return cls(
            loan_id     = str(data["loan_id"]),
            user_id     = str(data["user_id"]),
            book_id     = str(data["book_id"]),
            borrow_date = cls._parse_date(data.get("borrow_date")),
            due_date    = cls._parse_date(data.get("due_date")),
            return_date = cls._parse_date(data.get("return_date")),
            status      = str(data.get("status", "borrowing")),
            overdue_fee = float(data.get("overdue_fee", 0.0)),
        )

    # ------------------------------------------------------------------ #
    # Helper nội bộ                                                       #
    # ------------------------------------------------------------------ #

    @classmethod
    def _parse_date(cls, value):
        """Chuyển chuỗi ISO hoặc đối tượng date/datetime thành date."""
        if value is None or value == "":
            return None
        if isinstance(value, date):
            return value
        if isinstance(value, datetime):
            return value.date()
        return datetime.strptime(value, cls.DATE_FORMAT).date()

    # ------------------------------------------------------------------ #
    # Dunder methods                                                       #
    # ------------------------------------------------------------------ #

    def __repr__(self) -> str:
        return (
            f"Loan(loan_id={self.loan_id!r}, user_id={self.user_id!r}, "
            f"book_id={self.book_id!r}, borrow_date={self.borrow_date}, "
            f"due_date={self.due_date}, return_date={self.return_date}, "
            f"status={self.status!r}, overdue_fee={self.overdue_fee})"
        )

    def __eq__(self, other: object) -> bool:
        """So sánh hai phiếu mượn theo loan_id."""
        if not isinstance(other, Loan):
            return NotImplemented
        return self.loan_id == other.loan_id
