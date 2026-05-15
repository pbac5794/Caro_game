# ============================================================
# main.py - Entry point của game Caro (2 người chơi)
# ============================================================

import sys
import pygame

if sys.stdout is not None and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from config import FPS, PLAYER_X, PLAYER_O, BOARD_SIZE
from game.board import Board
from game.logic import GameLogic
from ui.pygame_ui import PygameUI
from game.evaluator import Evaluator


def main():
    """
    Hàm chính điều phối toàn bộ game.

    Luồng hoạt động:
    1. Khởi tạo các đối tượng: Board (bàn cờ), GameLogic (luật), PygameUI (giao diện)
    2. Vào vòng lặp game loop:
       a. Xử lý sự kiện (thoát, click chuột, nhấn phím)
       b. Cập nhật logic (đặt quân, kiểm tra thắng/hòa)
       c. Vẽ lại toàn bộ màn hình
       d. Giới hạn FPS
    """

    # ── 1. KHỞI TẠO ──────────────────────────────────────────
    board    = Board()       # Quản lý dữ liệu bàn cờ
    logic    = GameLogic()   # Xử lý luật chơi
    ui       = PygameUI()    # Giao diện pygame
    evaluator = Evaluator()  # Bộ đánh giá điểm số
    clock    = pygame.time.Clock()

    # Trạng thái game
    current_player = PLAYER_X   # X đi trước
    game_over      = False
    winner         = None        # Người thắng (PLAYER_X / PLAYER_O / None)
    winning_cells  = []          # Các ô tạo nên chuỗi thắng
    is_draw        = False

    # ── 2. GAME LOOP ─────────────────────────────────────────
    running = True
    while running:

        # ── 2a. XỬ LÝ SỰ KIỆN ───────────────────────────────
        for event in pygame.event.get():

            # Nhấn nút X đóng cửa sổ → thoát chương trình
            if event.type == pygame.QUIT:
                running = False

            # Nhấn phím R → chơi lại từ đầu
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    board.reset()
                    current_player = PLAYER_X
                    game_over      = False
                    winner         = None
                    winning_cells  = []
                    is_draw        = False
                    print("--- Ván mới bắt đầu! ---")

            # Di chuyển chuột → cập nhật hover effect
            if event.type == pygame.MOUSEMOTION:
                if not game_over:
                    ui.update_hover(event.pos)

            # Click chuột trái → đặt quân
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if game_over:
                    continue  # Không nhận nước đi khi game đã kết thúc

                # Chuyển tọa độ pixel → chỉ số ô trên bàn cờ
                row, col = ui.get_row_col_from_mouse(event.pos)

                # Kiểm tra ô có hợp lệ không
                if not (0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE):
                    continue  # Click ra ngoài bàn cờ

                # ── 2b. CẬP NHẬT LOGIC ───────────────────────
                moved = board.make_move(row, col, current_player)
                if not moved:
                    continue  # Ô đã có quân, bỏ qua

                player_name = "X" if current_player == PLAYER_X else "O"
                print(f"Người chơi {player_name} đặt tại [{row}, {col}]")
                
                # Tính toán và in điểm số Heuristic cục bộ
                score = evaluator.evaluate_local(board.grid, row, col)
                print(f"   -> Điểm Heuristic: {score:+,d}")

                # Kiểm tra thắng
                winner, winning_cells = logic.check_winner(board)
                if winner is not None:
                    game_over = True
                    win_name  = "X" if winner == PLAYER_X else "O"
                    print(f"🏆 Người chơi {win_name} THẮNG!")
                    ui.hover_cell = None  # Tắt hover khi game kết thúc

                # Kiểm tra hòa (chỉ khi chưa có người thắng)
                elif logic.is_draw(board):
                    game_over = True
                    is_draw   = True
                    print("🤝 HÒA! Bàn cờ đã đầy.")
                    ui.hover_cell = None

                else:
                    # Chuyển lượt: X → O, O → X
                    current_player = PLAYER_O if current_player == PLAYER_X else PLAYER_X

        # ── 2c. VẼ MÀN HÌNH ─────────────────────────────────
        # Thứ tự vẽ quan trọng: nền → bàn cờ → quân → vạch thắng → thanh trạng thái

        ui.draw_board(board)                           # Vẽ lưới bàn cờ (kèm hover)
        ui.draw_pieces(board)                          # Vẽ X / O lên các ô

        if game_over and winning_cells:
            ui.draw_winning_line(winning_cells)        # Vẽ vạch vàng nối chuỗi thắng

        ui.draw_status_bar(current_player, game_over, winner, is_draw)  # Thanh trạng thái

        ui.render()                                    # Cập nhật màn hình

        # ── 2d. GIỚI HẠN FPS ────────────────────────────────
        clock.tick(FPS)

    # ── 3. KẾT THÚC ─────────────────────────────────────────
    ui.quit()
    sys.exit()


# Điểm vào của chương trình
if __name__ == "__main__":
    main()
