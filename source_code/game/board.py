# ============================================================
# game/board.py - Class quản lý bàn cờ (mảng 2 chiều)
# ============================================================

from config import BOARD_SIZE, EMPTY


class Board:
    """
    Lớp Board đại diện cho bàn cờ Caro.
    Dữ liệu lưu trong mảng 2 chiều self.grid[row][col].
    Giá trị: 0 = ô trống, 1 = X, 2 = O
    """

    def __init__(self):
        """Khởi tạo bàn cờ trống kích thước BOARD_SIZE x BOARD_SIZE."""
        self.size = BOARD_SIZE
        # Tạo mảng 2D, tất cả các ô đều là EMPTY (0)
        self.grid = [[EMPTY] * self.size for _ in range(self.size)]

    def is_valid_move(self, row: int, col: int) -> bool:
        """
        Kiểm tra nước đi có hợp lệ không.
        Hợp lệ khi: tọa độ nằm trong bàn cờ VÀ ô đó đang trống.
        """
        in_bounds = 0 <= row < self.size and 0 <= col < self.size
        if not in_bounds:
            return False
        return self.grid[row][col] == EMPTY

    def make_move(self, row: int, col: int, player: int) -> bool:
        """
        Đặt quân của người chơi (player) vào ô (row, col).
        Trả về True nếu thành công, False nếu ô không hợp lệ.
        """
        if not self.is_valid_move(row, col):
            return False
        self.grid[row][col] = player
        return True

    def is_full(self) -> bool:
        """
        Kiểm tra bàn cờ đã đầy chưa (dùng để xét hòa).
        Trả về True nếu không còn ô trống nào.
        """
        for row in range(self.size):
            for col in range(self.size):
                if self.grid[row][col] == EMPTY:
                    return False
        return True

    def reset(self):
        """Đặt lại bàn cờ về trạng thái trống ban đầu."""
        self.grid = [[EMPTY] * self.size for _ in range(self.size)]
