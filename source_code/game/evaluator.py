class Evaluator:
    # Hằng số quy định trạng thái ô cờ
    EMPTY = 0
    PLAYER = 1   # MIN (Người chơi đánh X)
    MACHINE = 2  # MAX (Máy đánh O)

    def __init__(self):
        pass

    def _count_ray(self, board, r, c, dr, dc, player):
        """
        Đếm số lượng quân liên tiếp cùng màu theo một hướng tia (dr, dc)
        bắt đầu từ vị trí (r, c).
        
        Args:
            board (list[list[int]]): Bảng trò chơi 2D.
            r (int): Tọa độ hàng của quân vừa đánh.
            c (int): Tọa độ cột của quân vừa đánh.
            dr (int): Hướng duyệt theo hàng (delta row).
            dc (int): Hướng duyệt theo cột (delta col).
            player (int): Người chơi hiện tại (PLAYER hoặc MACHINE).
            
        Returns:
            tuple: (số_quân_cùng_màu_liên_tiếp, bị_chặn_hay_không)
        """
        count = 0
        blocked = False
        rows = len(board)
        cols = len(board[0])
        
        curr_r = r + dr
        curr_c = c + dc
        
        while True:
            # Nếu vượt ra ngoài mép bàn cờ -> Bị chặn
            if curr_r < 0 or curr_r >= rows or curr_c < 0 or curr_c >= cols:
                blocked = True
                break
            
            if board[curr_r][curr_c] == player:
                # Gặp quân đồng chất -> đếm thêm và đi tiếp
                count += 1
                curr_r += dr
                curr_c += dc
            elif board[curr_r][curr_c] == self.EMPTY:
                # Gặp ô trống -> Hướng này đang Mở (không bị chặn)
                blocked = False
                break
            else:
                # Gặp quân đối thủ -> Bị chặn
                blocked = True
                break
                
        return count, blocked

    def evaluate_local(self, board, last_r, last_c):
        """
        Đánh giá điểm số cục bộ tại tọa độ vừa đánh (last_r, last_c).
        Bắn tia theo 4 trục: Ngang, Dọc, Chéo chính, Chéo phụ.
        
        Args:
            board (list[list[int]]): Bảng trò chơi 2D.
            last_r (int): Tọa độ hàng của quân vừa đánh.
            last_c (int): Tọa độ cột của quân vừa đánh.
            
        Returns:
            int: Tổng điểm cục bộ dựa trên 4 trục.
        """
        player = board[last_r][last_c]
        if player == self.EMPTY:
            return 0
            
        # 4 hướng cơ bản (trục): (Ngang, Dọc, Chéo chính, Chéo phụ)
        directions = [
            (0, 1),   # Ngang
            (1, 0),   # Dọc
            (1, 1),   # Chéo chính
            (1, -1)   # Chéo phụ
        ]
        
        total_score = 0
        
        for dr, dc in directions:
            # Bắn tia về 2 hướng ngược nhau trên cùng một trục
            count1, blocked1 = self._count_ray(board, last_r, last_c, dr, dc, player)
            count2, blocked2 = self._count_ray(board, last_r, last_c, -dr, -dc, player)
            
            # Tổng số quân liên tiếp = Quân ở giữa (1) + số quân hướng 1 + số quân hướng 2
            total_count = 1 + count1 + count2
            
            # Tổng số đầu bị chặn = Tổng các đầu bị chặn của hướng 1 và hướng 2 (0, 1 hoặc 2)
            total_blocks = (1 if blocked1 else 0) + (1 if blocked2 else 0)
            
            # Khởi tạo điểm cho trục hiện tại
            axis_score = 0
            
            # Áp dụng BẢNG ĐIỂM CHUẨN (Heuristic Scoring)
            if total_count >= 4:
                # Nhóm 4 quân: Thắng luôn, không quan tâm bị chặn hay không
                axis_score = 100000 if player == self.MACHINE else -100000
                
            elif total_blocks == 2:
                # Nhóm Chết: Bị chặn 2 đầu thì 0 điểm (dù 2 hay 3 quân)
                axis_score = 0
                
            elif total_count == 3:
                # Nhóm 3 quân
                if total_blocks == 0:
                    # Mở 2 đầu (Chặn 0)
                    axis_score = 50000 if player == self.MACHINE else -50000
                elif total_blocks == 1:
                    # Bị chặn 1 đầu (Chặn 1)
                    axis_score = 1000 if player == self.MACHINE else -5000
                    
            elif total_count == 2:
                # Nhóm 2 quân
                if total_blocks == 0:
                    # Mở 2 đầu (Chặn 0)
                    axis_score = 100 if player == self.MACHINE else -100
                # Chặn 1 đầu thì được 0 điểm do luật không quy định khác
            
            # Cộng dồn điểm của trục này vào tổng điểm chung
            total_score += axis_score
            print(total_score)
        return total_score
