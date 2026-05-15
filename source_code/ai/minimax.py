import time
import math

class MinimaxAgent:
    """
    Class AI sử dụng thuật toán Minimax tích lũy điểm dọc theo các nhánh tìm kiếm.
    Cấu trúc không cắt tỉa Alpha-Beta.
    """

    def __init__(self, depth, evaluator):
        """
        Khởi tạo AI với độ sâu giới hạn và bộ đánh giá trạng thái.
        
        Args:
            depth (int): Độ sâu tối đa để duyệt cây.
            evaluator (Evaluator): Đối tượng chứa hàm đánh giá cục bộ evaluate_local.
        """
        self.max_depth = depth
        self.evaluator = evaluator
        
        # Hằng số định danh người chơi
        self.PLAYER = 1   # X - Người chơi (MIN)
        self.MACHINE = 2  # O - Máy (MAX)
        
        self.node_count = 0

    def get_move(self, board, game_logic):
        """
        Khởi động quá trình tìm kiếm nước đi tốt nhất cho Máy (MAX).
        """
        start_time = time.time()
        self.node_count = 0
        
        best_score = -float('inf')
        best_move = None
        
        # Lấy các ô trống trong bán kính 3 để tập trung đánh xoay quanh các quân cờ
        empty_cells = board.get_empty_cells(radius=3)
        
        for r, c in empty_cells:
            # 1. Tính điểm phòng thủ: Nếu Người (MIN) đánh vào đây thì được bao nhiêu?
            board.make_move(r, c, self.PLAYER)
            defense_score = self.evaluator.evaluate_local(board.grid, r, c)
            board.undo_move(r, c)
            
            # 2. Tính điểm tấn công: Máy (MAX) thực sự đánh vào đây
            board.make_move(r, c, self.MACHINE)
            attack_score = self.evaluator.evaluate_local(board.grid, r, c)
            
            # Điểm của nước đi = Điểm tấn công của Máy - Điểm phòng thủ (tức là chặn Người chơi)
            # Vì Evaluator trả điểm âm cho Người chơi, nên attack - defense -> Tăng điểm dương cho Máy
            move_score = attack_score - defense_score
            
            # Gọi đệ quy hàm minimax
            score = self._minimax_rec(board, self.max_depth - 1, False, move_score, r, c, game_logic)
            
            # Rút lại nước đi để làm sạch trạng thái bàn cờ
            board.undo_move(r, c)
            
            # Cập nhật nước đi tốt nhất
            if score > best_score:
                best_score = score
                best_move = (r, c)
                
        execution_time = time.time() - start_time
        
        # Báo cáo ra terminal
        print(f"[Minimax] Độ sâu: {self.max_depth} | Trạng thái đã xét: {self.node_count} "
              f"| Thời gian: {execution_time:.4f}s | Chọn nước: {best_move} | Điểm: {best_score}")
              
        return best_move, best_score

    def _minimax_rec(self, board, depth, is_maximizing, current_score, last_r, last_c, game_logic):
        """
        Hàm đệ quy duyệt cây Minimax theo cách cộng dồn điểm (current_score).
        
        Args:
            board: Bàn cờ hiện tại
            depth: Độ sâu còn lại
            is_maximizing: True (MAX - Máy), False (MIN - Người)
            current_score: Điểm tổng tích lũy từ gốc cây xuống tới node hiện tại
            last_r, last_c: Tọa độ nước đi vừa thực hiện (để kiểm tra kết thúc/thắng)
            game_logic: Đối tượng xử lý luật chơi
        """
        self.node_count += 1
        
        # 1. Kiểm tra điều kiện dừng (Base Cases)
        # Truyền board vào hàm check_winner
        winner, _ = game_logic.check_winner(board)
        if winner == self.MACHINE:
            return 10000000 + depth * 1000  # Ưu tiên thắng càng sớm càng tốt
        elif winner == self.PLAYER:
            return -10000000 - depth * 1000 # Trì hoãn thua càng lâu càng tốt
            
        # Nếu bàn cờ đầy hoặc đã duyệt hết độ sâu cho phép
        if board.is_full() or depth == 0:
            return current_score
            
        # Lấy danh sách ô trống để duyệt tiếp (bán kính 3)
        empty_cells = board.get_empty_cells(radius=3)
        
        # 2. Xử lý logic 2 nhánh MAX và MIN
        if is_maximizing:
            # Nhánh MAX (Lượt Máy)
            max_eval = -float('inf')
            for r, c in empty_cells:
                # Tính điểm phòng thủ trước
                board.make_move(r, c, self.PLAYER)
                defense_score = self.evaluator.evaluate_local(board.grid, r, c)
                board.undo_move(r, c)
                
                # Tính điểm tấn công
                board.make_move(r, c, self.MACHINE)
                attack_score = self.evaluator.evaluate_local(board.grid, r, c)
                
                move_score = attack_score - defense_score
                
                eval_score = self._minimax_rec(board, depth - 1, False, current_score + move_score, r, c, game_logic)
                board.undo_move(r, c)
                max_eval = max(max_eval, eval_score)
                
            return max_eval
            
        else:
            # Nhánh MIN (Lượt Người)
            min_eval = float('inf')
            for r, c in empty_cells:
                # Tính điểm phòng thủ trước (Máy)
                board.make_move(r, c, self.MACHINE)
                defense_score = self.evaluator.evaluate_local(board.grid, r, c)
                board.undo_move(r, c)
                
                # Tính điểm tấn công (Người)
                board.make_move(r, c, self.PLAYER)
                attack_score = self.evaluator.evaluate_local(board.grid, r, c)
                
                move_score = attack_score - defense_score
                
                eval_score = self._minimax_rec(board, depth - 1, True, current_score + move_score, r, c, game_logic)
                board.undo_move(r, c)
                min_eval = min(min_eval, eval_score)
                
            return min_eval
