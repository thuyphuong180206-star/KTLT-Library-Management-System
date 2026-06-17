"""
Lớp thực thể Sách (Book Object)
Nhiệm vụ: Khai báo cấu trúc thông tin của một đầu sách trong hệ thống.
Thuộc tính:
    - book_id (str)      : Mã sách duy nhất
    - title (str)        : Tên sách
    - author (str)       : Tác giả
    - genre (str)        : Thể loại
    - publisher (str)    : Nhà xuất bản
    - quantity (int)     : Số lượng tồn kho
    - status (str)       : Tình trạng vật lý ("active" = đang lưu hành | "inactive" = ngừng lưu hành)
    - borrow_count (int) : Số lượt mượn tích lũy
Phương thức: to_dict(), from_dict(), __repr__, __eq__
Import bởi: storage.data_processor, logic.search, logic.sort, logic.loan_manager, interface.menu
"""


class Book:
    """
    Thực thể đại diện cho một cuốn sách trong hệ thống quản lý thư viện.

    Attributes:
        book_id (str):      Mã định danh duy nhất của sách (ví dụ: "B001").
        title (str):        Tên sách.
        author (str):       Tên tác giả.
        genre (str):        Thể loại sách (ví dụ: "Công nghệ", "Toán học", "Văn học").
        publisher (str):    Nhà xuất bản.
        quantity (int):     Tổng số bản sách hiện có trong thư viện.
        status (str):       Tình trạng vật lý của đầu sách.
                            Giá trị hợp lệ: "active" (đang lưu hành) | "inactive" (ngừng lưu hành).
        borrow_count (int): Số lần sách đã được mượn (dùng để thống kê/sắp xếp).
    """

    VALID_STATUSES = {"active", "inactive"}

    def __init__(
        self,
        book_id: str,
        title: str,
        author: str,
        genre: str,
        publisher: str,
        quantity: int = 1,
        status: str = "active",
        borrow_count: int = 0,
    ):
        """
        Khởi tạo đối tượng Book.

        Args:
            book_id (str):      Mã sách duy nhất.
            title (str):        Tên sách.
            author (str):       Tên tác giả.
            genre (str):        Thể loại sách.
            publisher (str):    Nhà xuất bản.
            quantity (int):     Số lượng bản sách (mặc định: 1).
            status (str):       Tình trạng vật lý sách (mặc định: "active").
            borrow_count (int): Số lần đã được mượn (mặc định: 0).
        """
        self.book_id      = book_id
        self.title        = title
        self.author       = author
        self.genre        = genre
        self.publisher    = publisher
        self.quantity     = quantity
        self.status       = status
        self.borrow_count = borrow_count

    def to_dict(self) -> dict:
        """Chuyển đối tượng Book thành dict — phục vụ storage.data_processor khi ghi CSV."""
        return {
            "book_id":      self.book_id,
            "title":        self.title,
            "author":       self.author,
            "genre":        self.genre,
            "publisher":    self.publisher,
            "quantity":     self.quantity,
            "status":       self.status,
            "borrow_count": self.borrow_count,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Book":
        """Tạo đối tượng Book từ dict đọc từ CSV — ép kiểu an toàn."""
        return cls(
            book_id      = str(data["book_id"]),
            title        = str(data["title"]),
            author       = str(data["author"]),
            genre        = str(data["genre"]),
            publisher    = str(data["publisher"]),
            quantity     = int(data.get("quantity", 1)),
            status       = str(data.get("status", "active")),
            borrow_count = int(data.get("borrow_count", 0)),
        )

    def __repr__(self) -> str:
        return (
            f"Book(book_id={self.book_id!r}, title={self.title!r}, "
            f"author={self.author!r}, genre={self.genre!r}, "
            f"publisher={self.publisher!r}, quantity={self.quantity}, "
            f"status={self.status!r}, borrow_count={self.borrow_count})"
        )

    def __eq__(self, other: object) -> bool:
        """So sánh hai sách dựa trên book_id — dùng trong logic.search."""
        if not isinstance(other, Book):
            return NotImplemented
        return self.book_id == other.book_id
