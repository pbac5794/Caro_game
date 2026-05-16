# ============================================================
# main.py - Entry point của game Caro (Người chơi vs AI Minimax)
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
from ai.minimax import MinimaxAgent


def main():
    """
    Hàm chính điều phối toàn bộ game.

    Luồng hoạt động:
    1. Khởi tạo các đối tượng: Board, GameLogic, PygameUI, Evaluator, và AI (MinimaxAgent).
    2. Vào vòng lặp game loop:
       a. Lượt AI (nếu đến lượt máy): AI tính nước đi tốt nhất qua thuật toán Minimax và tự đặt cờ.
       b. Lượt Người chơi: Xử lý sự kiện click chuột.
       c. Cập nhật logic (kiểm tra thắng/hòa sau mỗi nước).
       d. Vẽ lại toàn bộ màn hình.
       e. Giới hạn FPS.
    """

    # ── 1. KHỞI TẠO ──────────────────────────────────────────
    board      = Board()       # Quản lý dữ liệu bàn cờ
    logic      = GameLogic()   # Xử lý luật chơi
    ui         = PygameUI()    # Giao diện pygame
    evaluator  = Evaluator()   # Bộ đánh giá điểm số
    
    # Khởi tạo AI với độ sâu bằng 3 (đã tối ưu hóa radius=3 để chạy mượt hơn), truyền vào Evaluator
    ai_agent   = MinimaxAgent(depth=3, evaluator=evaluator)
    
    clock      = pygame.time.Clock()

    # Trạng thái game ban đầu
    current_player = PLAYER_X    # Người chơi (X) luôn đi trước
    game_over      = False
    winner         = None        # Người thắng (PLAYER_X / PLAYER_O / None)
    winning_cells  = []          # Các ô tạo nên chuỗi thắng
    is_draw        = False

    # ── 2. GAME LOOP ─────────────────────────────────────────
    running = True
    while running:

        # ── 2a. XỬ LÝ LƯỢT AI (MÁY CHƠI) ──────────────────────────
        # Chỉ kích hoạt nếu game chưa kết thúc và đang là lượt của Máy (PLAYER_O)
        if not game_over and current_player == PLAYER_O:
            print("\n🤖 AI đang suy nghĩ...")
            
            # (Tùy chọn) Gọi ui.render() 1 lần trước để hiện dòng trạng thái "Lượt O" trước khi AI nghĩ
            ui.draw_board(board)
            ui.draw_pieces(board)
            ui.draw_status_bar(current_player, game_over, winner, is_draw)
            ui.render()
            
            # Lấy tọa độ tốt nhất từ Minimax
            best_move, _ = ai_agent.get_move(board, logic)
            
            if best_move is not None:
                row, col = best_move
                board.make_move(row, col, PLAYER_O)
                print(f"👉 Máy (O) đánh tại tọa độ [{row}, {col}]")
                
                # Kiểm tra trạng thái game ngay sau nước cờ của AI
                winner, winning_cells = logic.check_winner(board, row, col)
                if winner is not None:
                    game_over = True
                    print(f"🏆 MÁY (O) ĐÃ THẮNG!")
                    ui.hover_cell = None
                elif logic.is_draw(board):
                    game_over = True
                    is_draw   = True
                    print("🤝 HÒA! Bàn cờ đã đầy.")
                    ui.hover_cell = None
                else:
                    # Chuyển lượt lại cho Người
                    current_player = PLAYER_X

        # ── 2b. XỬ LÝ SỰ KIỆN TỪ BÀN PHÍM/CHUỘT ─────────────────
        for event in pygame.event.get():

            # Đóng cửa sổ
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
                    print("\n--- Ván mới bắt đầu! (X đi trước) ---")

            # Di chuyển chuột → cập nhật hover effect
            if event.type == pygame.MOUSEMOTION:
                if not game_over and current_player == PLAYER_X:
                    ui.update_hover(event.pos)

            # Click chuột trái → Người chơi đặt quân
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Bỏ qua nếu game đã hết hoặc đang là lượt của Máy
                if game_over or current_player != PLAYER_X:
                    continue  

                # Chuyển tọa độ pixel → chỉ số ô
                row, col = ui.get_row_col_from_mouse(event.pos)

                if not (0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE):
                    continue  

                # ── CẬP NHẬT LOGIC LƯỢT NGƯỜI CHƠI ───────────────
                moved = board.make_move(row, col, PLAYER_X)
                if not moved:
                    continue  # Trùng ô đã đánh, bỏ qua
                    
                print(f"\n👤 Người chơi (X) đánh tại [{row}, {col}]")
                
                # Kiểm tra trạng thái game
                winner, winning_cells = logic.check_winner(board, row, col)
                if winner is not None:
                    game_over = True
                    print(f"🏆 NGƯỜI CHƠI (X) THẮNG!")
                    ui.hover_cell = None  
                elif logic.is_draw(board):
                    game_over = True
                    is_draw   = True
                    print("🤝 HÒA! Bàn cờ đã đầy.")
                    ui.hover_cell = None
                else:
                    # Chuyển lượt qua Máy
                    current_player = PLAYER_O

        # ── 2c. VẼ MÀN HÌNH ─────────────────────────────────
        ui.draw_board(board)
        ui.draw_pieces(board)

        if game_over and winning_cells:
            ui.draw_winning_line(winning_cells)

        ui.draw_status_bar(current_player, game_over, winner, is_draw)

        ui.render()

        # ── 2d. GIỚI HẠN FPS ────────────────────────────────
        clock.tick(FPS)

    # ── 3. KẾT THÚC ─────────────────────────────────────────
    ui.quit()
    sys.exit()


if __name__ == "__main__":
    main()
