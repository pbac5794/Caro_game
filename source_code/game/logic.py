# ============================================================
# game/logic.py - Class xử lý logic game (kiểm tra thắng/hòa)
# ============================================================

from config import BOARD_SIZE, EMPTY, WIN_COUNT
from game.board import Board


class GameLogic:
    """
    Lớp GameLogic chứa các luật chơi của Caro.
    Tách biệt hoàn toàn với phần giao diện.
    """

    def check_winner(self, board: Board):
        """
        Quét toàn bộ bàn cờ để tìm người thắng.

        Thuật toán:
        - Duyệt từng ô trên bàn cờ.
        - Từ ô đó, kiểm tra 4 hướng: ngang (→), dọc (↓),
          chéo chính (↘), chéo phụ (↙).
        - Nếu tìm thấy WIN_COUNT quân liên tiếp cùng loại
          thì trả về (player, danh sách ô thắng).
        - Nếu không có ai thắng, trả về (None, []).

        Trả về: tuple (winner, winning_cells)
            - winner: PLAYER_X, PLAYER_O, hoặc None
            - winning_cells: list[(row, col)] các ô tạo nên chuỗi thắng
        """
        grid = board.grid
        size = board.size

        # 4 hướng kiểm tra: (delta_row, delta_col)
        directions = [
            (0, 1),   # → ngang (phải)
            (1, 0),   # ↓ dọc (xuống)
            (1, 1),   # ↘ chéo chính
            (1, -1),  # ↙ chéo phụ
        ]

        for row in range(size):
            for col in range(size):
                current = grid[row][col]

                # Bỏ qua ô trống
                if current == EMPTY:
                    continue

                for dr, dc in directions:
                    # Thu thập WIN_COUNT ô liên tiếp theo hướng (dr, dc)
                    cells = []
                    for step in range(WIN_COUNT):
                        r = row + dr * step
                        c = col + dc * step
                        # Kiểm tra vẫn trong bàn cờ và cùng người chơi
                        if 0 <= r < size and 0 <= c < size and grid[r][c] == current:
                            cells.append((r, c))
                        else:
                            break  # Chuỗi bị đứt, thôi kiểm tra hướng này

                    # Nếu tìm đủ WIN_COUNT quân liên tiếp → có người thắng
                    if len(cells) == WIN_COUNT:
                        return current, cells  # (người thắng, các ô thắng)

        # Không có ai thắng
        return None, []

    def is_draw(self, board: Board) -> bool:
        """
        Kiểm tra hòa: bàn cờ đầy mà không có người thắng.
        """
        winner, _ = self.check_winner(board)
        return board.is_full() and winner is None
