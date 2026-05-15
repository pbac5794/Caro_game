# ============================================================
# ui/pygame_ui.py - Class giao diện đồ họa dùng Pygame
# ============================================================

import pygame
from config import (
    BOARD_SIZE, CELL_SIZE, MARGIN, STATUS_HEIGHT,
    WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE,
    PLAYER_X, PLAYER_O, EMPTY,
    COLOR_BG, COLOR_GRID, COLOR_X, COLOR_O,
    COLOR_STATUS_BG, COLOR_STATUS_TXT,
    COLOR_WIN_LINE, COLOR_HOVER, COLOR_BLACK, COLOR_WHITE
)
from game.board import Board


class PygameUI:
    """
    Lớp PygameUI chịu trách nhiệm toàn bộ phần hiển thị.
    Tách biệt hoàn toàn với logic game.
    """

    def __init__(self):
        """
        Khởi tạo cửa sổ pygame và font chữ.
        """
        pygame.init()
        # Tạo cửa sổ với kích thước đã tính trong config
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)

        # Font chữ cho trạng thái game
        self.font_status = pygame.font.SysFont("segoeui", 22, bold=True)
        self.font_symbol = pygame.font.SysFont("segoeui", 32, bold=True)

        # Lưu vị trí chuột hiện tại để vẽ hover effect
        self.hover_cell = None

    # ----------------------------------------------------------
    # PHẦN VẼ GIAO DIỆN
    # ----------------------------------------------------------

    def draw_status_bar(self, current_player: int, game_over: bool, winner, is_draw: bool):
        """
        Vẽ thanh trạng thái ở phía trên cùng màn hình.
        Hiển thị lượt chơi hiện tại hoặc kết quả game.
        """
        # Vẽ nền thanh trạng thái
        pygame.draw.rect(self.screen, COLOR_STATUS_BG,
                         (0, 0, WINDOW_WIDTH, STATUS_HEIGHT))

        # Xác định nội dung text
        if game_over:
            if is_draw:
                text = "🤝  HÒA!  Nhấn R để chơi lại"
            else:
                name = "X" if winner == PLAYER_X else "O"
                color = COLOR_X if winner == PLAYER_X else COLOR_O
                text = f"🏆  Người chơi {name} thắng!  Nhấn R để chơi lại"
        else:
            name = "X" if current_player == PLAYER_X else "O"
            color = COLOR_X if current_player == PLAYER_X else COLOR_O
            text = f"Lượt của người chơi:  {name}"

        # Render text lên màn hình (căn giữa)
        if game_over:
            if is_draw:
                surf = self.font_status.render(text, True, COLOR_WHITE)
            else:
                surf = self.font_status.render(text, True, color)
        else:
            # Render phần đầu với màu trắng, phần tên người chơi với màu riêng
            surf_pre  = self.font_status.render("Lượt của người chơi:  ", True, COLOR_STATUS_TXT)
            surf_name = self.font_status.render(name, True, color)
            # Tính vị trí căn giữa
            total_w = surf_pre.get_width() + surf_name.get_width()
            x_start = (WINDOW_WIDTH - total_w) // 2
            y_pos   = (STATUS_HEIGHT - surf_pre.get_height()) // 2
            self.screen.blit(surf_pre,  (x_start, y_pos))
            self.screen.blit(surf_name, (x_start + surf_pre.get_width(), y_pos))
            return

        x_pos = (WINDOW_WIDTH - surf.get_width()) // 2
        y_pos = (STATUS_HEIGHT - surf.get_height()) // 2
        self.screen.blit(surf, (x_pos, y_pos))

    def draw_board(self, board: Board):
        """
        Vẽ nền và lưới của bàn cờ.
        Lưới bắt đầu từ tọa độ (MARGIN, STATUS_HEIGHT + MARGIN).
        """
        # Vẽ nền toàn màn hình (màu bàn cờ)
        self.screen.fill(COLOR_BG)

        # Vẽ vùng bàn cờ sáng hơn
        board_rect = pygame.Rect(
            MARGIN, STATUS_HEIGHT + MARGIN,
            CELL_SIZE * BOARD_SIZE, CELL_SIZE * BOARD_SIZE
        )
        pygame.draw.rect(self.screen, COLOR_BG, board_rect)

        # Vẽ hover effect (tô màu ô đang trỏ chuột)
        if self.hover_cell:
            h_row, h_col = self.hover_cell
            hover_rect = pygame.Rect(
                MARGIN + h_col * CELL_SIZE,
                STATUS_HEIGHT + MARGIN + h_row * CELL_SIZE,
                CELL_SIZE, CELL_SIZE
            )
            pygame.draw.rect(self.screen, COLOR_HOVER, hover_rect)

        # Vẽ các đường kẻ lưới (ngang và dọc)
        for i in range(BOARD_SIZE + 1):
            # Đường ngang
            pygame.draw.line(
                self.screen, COLOR_GRID,
                (MARGIN, STATUS_HEIGHT + MARGIN + i * CELL_SIZE),
                (MARGIN + BOARD_SIZE * CELL_SIZE, STATUS_HEIGHT + MARGIN + i * CELL_SIZE),
                2 if i in (0, BOARD_SIZE) else 1  # Viền ngoài đậm hơn
            )
            # Đường dọc
            pygame.draw.line(
                self.screen, COLOR_GRID,
                (MARGIN + i * CELL_SIZE, STATUS_HEIGHT + MARGIN),
                (MARGIN + i * CELL_SIZE, STATUS_HEIGHT + MARGIN + BOARD_SIZE * CELL_SIZE),
                2 if i in (0, BOARD_SIZE) else 1
            )

    def draw_pieces(self, board: Board):
        """
        Quét mảng bàn cờ và vẽ ký hiệu X hoặc O lên từng ô.
        X được vẽ bằng 2 đường chéo (màu đỏ).
        O được vẽ bằng hình tròn rỗng (màu xanh).
        """
        grid = board.grid
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                cell_value = grid[row][col]
                if cell_value == EMPTY:
                    continue  # Bỏ qua ô trống

                # Tọa độ tâm của ô
                cx = MARGIN + col * CELL_SIZE + CELL_SIZE // 2
                cy = STATUS_HEIGHT + MARGIN + row * CELL_SIZE + CELL_SIZE // 2
                padding = CELL_SIZE // 4  # Khoảng cách từ tâm ra mép X/O

                if cell_value == PLAYER_X:
                    # Vẽ X: hai đường chéo giao nhau
                    pygame.draw.line(
                        self.screen, COLOR_X,
                        (cx - padding, cy - padding),
                        (cx + padding, cy + padding), 4
                    )
                    pygame.draw.line(
                        self.screen, COLOR_X,
                        (cx + padding, cy - padding),
                        (cx - padding, cy + padding), 4
                    )
                elif cell_value == PLAYER_O:
                    # Vẽ O: hình tròn rỗng
                    pygame.draw.circle(self.screen, COLOR_O,
                                       (cx, cy), padding, 4)

    def draw_winning_line(self, winning_cells: list):
        """
        Vẽ vạch vàng nối các ô thắng để làm nổi bật chuỗi chiến thắng.
        """
        if not winning_cells or len(winning_cells) < 2:
            return

        # Tính tọa độ pixel của ô đầu và ô cuối
        r0, c0 = winning_cells[0]
        r1, c1 = winning_cells[-1]

        start_pos = (
            MARGIN + c0 * CELL_SIZE + CELL_SIZE // 2,
            STATUS_HEIGHT + MARGIN + r0 * CELL_SIZE + CELL_SIZE // 2
        )
        end_pos = (
            MARGIN + c1 * CELL_SIZE + CELL_SIZE // 2,
            STATUS_HEIGHT + MARGIN + r1 * CELL_SIZE + CELL_SIZE // 2
        )
        pygame.draw.line(self.screen, COLOR_WIN_LINE, start_pos, end_pos, 5)

    def update_hover(self, mouse_pos):
        """
        Cập nhật ô đang được trỏ chuột (dùng cho hover effect).
        Gọi mỗi lần chuột di chuyển.
        """
        row, col = self.get_row_col_from_mouse(mouse_pos)
        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
            self.hover_cell = (row, col)
        else:
            self.hover_cell = None

    # ----------------------------------------------------------
    # PHẦN CHUYỂN ĐỔI TỌA ĐỘ
    # ----------------------------------------------------------

    def get_row_col_from_mouse(self, pos: tuple) -> tuple:
        """
        Chuyển tọa độ pixel (x, y) của chuột thành chỉ số (row, col) trên bàn cờ.

        Công thức:
            col = (x - MARGIN) // CELL_SIZE
            row = (y - STATUS_HEIGHT - MARGIN) // CELL_SIZE

        Trả về (row, col). Nếu click ngoài bàn cờ, giá trị có thể âm
        hoặc >= BOARD_SIZE, cần kiểm tra ở nơi gọi.
        """
        x, y = pos
        col = (x - MARGIN) // CELL_SIZE
        row = (y - STATUS_HEIGHT - MARGIN) // CELL_SIZE
        return int(row), int(col)

    def render(self):
        """Cập nhật toàn bộ màn hình (gọi cuối mỗi vòng lặp)."""
        pygame.display.update()

    def quit(self):
        """Dọn dẹp và thoát pygame."""
        pygame.quit()
