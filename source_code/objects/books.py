"""
Lớp thực thể Sách (Book Object)
Nhiệm vụ: Khai báo cấu trúc thông tin của một đầu sách trong hệ thống.
Thuộc tính:
    - book_id (str)      : Mã sách duy nhất
    - title (str)        : Tên sách
    - author (str)       : Tác giả
    - genre (str)        : Thể loại
    - quantity (int)     : Số lượng tồn kho
    - status (str)       : Trạng thái ("available", "borrowed", "unavailable")
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
        quantity (int):     Tổng số bản sách hiện có trong thư viện.
        status (str):       Trạng thái hiện tại của sách.
                            Giá trị hợp lệ: "available" | "borrowed" | "unavailable".
        borrow_count (int): Số lần sách đã được mượn (dùng để thống kê/sắp xếp).
    """

    # Tập hợp trạng thái hợp lệ — dùng để validate từ các module khác
    VALID_STATUSES = {"available", "borrowed", "unavailable"}

    def __init__(
        self,
        book_id: str,
        title: str,
        author: str,
        genre: str,
        quantity: int = 1,
        status: str = "available",
        borrow_count: int = 0,
    ):
        """
        Khởi tạo đối tượng Book.

        Args:
            book_id (str):      Mã sách duy nhất.
            title (str):        Tên sách.
            author (str):       Tên tác giả.
            genre (str):        Thể loại sách (mặc định: "").
            quantity (int):     Số lượng bản sách (mặc định: 1).
            status (str):       Trạng thái sách (mặc định: "available").
            borrow_count (int): Số lần đã được mượn (mặc định: 0).
        """
        self.book_id = book_id
        self.title = title
        self.author = author
        self.genre = genre          # ← THÊM MỚI
        self.quantity = quantity
        self.status = status
        self.borrow_count = borrow_count

    def to_dict(self) -> dict:
        """
        Chuyển đối tượng Book thành dict — phục vụ storage.data_processor khi ghi file.

        Returns:
            dict: Dữ liệu sách dưới dạng key-value.
        """
        return {
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author,
            "genre": self.genre,    # ← THÊM MỚI
            "quantity": self.quantity,
            "status": self.status,
            "borrow_count": self.borrow_count,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Book":
        """
        Tạo đối tượng Book từ dict — phục vụ storage.data_processor khi đọc file.

        Args:
            data (dict): Dict chứa dữ liệu sách (thường đọc từ CSV).

        Returns:
            Book: Đối tượng Book tương ứng.
        """
        return cls(
            book_id=data["book_id"],
            title=data["title"],
            author=data["author"],
            genre=data.get("genre", ""),        # ← THÊM MỚI
            quantity=int(data.get("quantity", 1)),
            status=data.get("status", "available"),
            borrow_count=int(data.get("borrow_count", 0)),
        )

    def __repr__(self) -> str:
        return (
            f"Book(book_id={self.book_id!r}, title={self.title!r}, "
            f"author={self.author!r}, genre={self.genre!r}, "
            f"quantity={self.quantity}, status={self.status!r}, "
            f"borrow_count={self.borrow_count})"
        )

    def __eq__(self, other: object) -> bool:
        """So sánh hai sách dựa trên book_id — dùng trong logic.search."""
        if not isinstance(other, Book):
            return NotImplemented
        return self.book_id == other.book_id
