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

    def check_winner(self, board: Board, last_r: int, last_c: int):
        """
        Kiểm tra người thắng bằng cách chỉ quét 4 đường đi qua tọa độ vừa đánh (last_r, last_c).
        Tối ưu hiệu năng cực lớn.
        """
        grid = board.grid
        size = board.size

        directions = [
            (0, 1),   # Ngang
            (1, 0),   # Dọc
            (1, 1),   # Chéo chính
            (1, -1),  # Chéo phụ
        ]

        current = grid[last_r][last_c]
        if current == EMPTY:
            return None, []

        for dr, dc in directions:
            cells = [(last_r, last_c)]
            
            # Kiểm tra theo chiều dương
            for step in range(1, WIN_COUNT):
                r = last_r + dr * step
                c = last_c + dc * step
                if 0 <= r < size and 0 <= c < size and grid[r][c] == current:
                    cells.append((r, c))
                else:
                    break
            
            # Kiểm tra theo chiều âm
            for step in range(1, WIN_COUNT):
                r = last_r - dr * step
                c = last_c - dc * step
                if 0 <= r < size and 0 <= c < size and grid[r][c] == current:
                    cells.append((r, c))
                else:
                    break

            if len(cells) >= WIN_COUNT:
                cells.sort()  # Sắp xếp lại tọa độ cho đẹp nếu cần vẽ đường kẻ
                return current, cells

        return None, []

    def is_draw(self, board: Board) -> bool:
        """
        Kiểm tra hòa: bàn cờ đầy. 
        (Đã bỏ check_winner bên trong vì luồng chính luôn kiểm tra win trước khi check hòa)
        """
        return board.is_full()
