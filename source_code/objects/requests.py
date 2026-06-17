"""
Lớp thực thể Yêu cầu chờ mượn sách (BorrowRequest Object)
Nhiệm vụ: Khai báo cấu trúc thông tin của một yêu cầu chờ khi sách hết kho.
Thuộc tính:
    - request_id (str)   : Mã yêu cầu chờ duy nhất (ví dụ: "WR001")
    - user_id (str)      : Mã bạn đọc đang chờ
    - book_id (str)      : Mã sách đang chờ
    - request_date (date): Ngày đăng ký chờ
Phương thức: to_dict(), from_dict(), _parse_date(), __repr__, __eq__
Import bởi: storage.data_processor, logic.loan_manager,
            structure.waiting_queue
"""

from datetime import date, datetime
from typing import Optional


class BorrowRequest:
    """
    Thực thể đại diện cho một yêu cầu chờ mượn sách khi sách hết kho.
    """

    DATE_FORMAT = "%Y-%m-%d"

    def __init__(
        self,
        request_id: str,
        user_id: str,
        book_id: str,
        request_date: date,
    ):
        """
        Khởi tạo đối tượng BorrowRequest.

        Args:
            request_id (str)   : Mã yêu cầu chờ duy nhất.
            user_id (str)      : Mã bạn đọc đang chờ.
            book_id (str)      : Mã sách đang chờ.
            request_date (date): Ngày đăng ký chờ.
        """
        self.request_id   = request_id
        self.user_id      = user_id
        self.book_id      = book_id
        self.request_date = request_date

    # ------------------------------------------------------------------ #
    # Serialization — phục vụ storage.data_processor                     #
    # ------------------------------------------------------------------ #

    def to_dict(self) -> dict:
        """Chuyển đối tượng BorrowRequest thành dict — phục vụ ghi CSV."""
        return {
            "request_id":   self.request_id,
            "user_id":      self.user_id,
            "book_id":      self.book_id,
            "request_date": self.request_date.strftime(self.DATE_FORMAT)
                            if isinstance(self.request_date, date) else "",
        }

    @classmethod
    def from_dict(cls, data: dict) -> "BorrowRequest":
        """Tạo đối tượng BorrowRequest từ dict đọc từ CSV — ép kiểu an toàn."""
        return cls(
            request_id   = str(data["request_id"]),
            user_id      = str(data["user_id"]),
            book_id      = str(data["book_id"]),
            request_date = cls._parse_date(data.get("request_date")),
        )

    # ------------------------------------------------------------------ #
    # Helper nội bộ                                                       #
    # ------------------------------------------------------------------ #

    @classmethod
    def _parse_date(cls, value) -> Optional[date]:
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
            f"BorrowRequest(request_id={self.request_id!r}, "
            f"user_id={self.user_id!r}, book_id={self.book_id!r}, "
            f"request_date={self.request_date})"
        )

    def __eq__(self, other: object) -> bool:
        """So sánh hai yêu cầu chờ theo request_id."""
        if not isinstance(other, BorrowRequest):
            return NotImplemented
        return self.request_id == other.request_id
