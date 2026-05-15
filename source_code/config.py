# ============================================================
# config.py - File cấu hình chứa các hằng số của game
# ============================================================

# --- Hằng số logic bàn cờ ---
BOARD_SIZE = 9          # Kích thước bàn cờ 9x9
EMPTY     = 0           # Ô trống
PLAYER_X  = 1           # Người chơi X
PLAYER_O  = 2           # Người chơi O
WIN_COUNT = 4           # Số quân liên tiếp để thắng

# --- Hằng số giao diện Pygame ---
CELL_SIZE     = 60                              # Kích thước mỗi ô (pixel)
MARGIN        = 40                              # Khoảng cách lề xung quanh bàn cờ
STATUS_HEIGHT = 60                              # Chiều cao thanh trạng thái phía trên

WINDOW_WIDTH  = CELL_SIZE * BOARD_SIZE + MARGIN * 2          # Chiều rộng cửa sổ
WINDOW_HEIGHT = CELL_SIZE * BOARD_SIZE + MARGIN * 2 + STATUS_HEIGHT  # Chiều cao cửa sổ

FPS = 30  # Số khung hình mỗi giây

# --- Màu sắc (RGB) ---
COLOR_BG         = (245, 222, 179)   # Màu nền bàn cờ (vàng gỗ)
COLOR_GRID       = (100,  70,  30)   # Màu lưới bàn cờ (nâu đậm)
COLOR_X          = (210,  50,  50)   # Màu X (đỏ)
COLOR_O          = ( 30, 100, 200)   # Màu O (xanh dương)
COLOR_WHITE      = (255, 255, 255)   # Trắng
COLOR_BLACK      = (  0,   0,   0)   # Đen
COLOR_STATUS_BG  = ( 40,  40,  60)   # Màu nền thanh trạng thái (tím đậm)
COLOR_STATUS_TXT = (255, 255, 200)   # Màu chữ trạng thái (vàng nhạt)
COLOR_WIN_LINE   = (255, 215,   0)   # Màu vạch thắng (vàng)
COLOR_HOVER      = (180, 220, 140)   # Màu highlight ô đang trỏ chuột

# --- Tên cửa sổ ---
WINDOW_TITLE = "Game Caro 9x9 - 2 Người Chơi"
