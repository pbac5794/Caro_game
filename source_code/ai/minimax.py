import time
import math

class MinimaxAgent:
    """
    Class AI sử dụng thuật toán Minimax tích lũy điểm dọc theo các nhánh tìm kiếm.
    Cấu trúc có cắt tỉa Alpha-Beta (Alpha-Beta Pruning).
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
        alpha = -float('inf')
        beta = float('inf')
        
        # Giảm radius xuống 2 để thu hẹp không gian tìm kiếm, loại bỏ các nước đi rác
        empty_cells = board.get_empty_cells(radius=2)
        
        # Sắp xếp nước đi (Move Ordering)
        ordered_moves = self._get_ordered_moves(board, empty_cells, True)
        
        for move_score, r, c in ordered_moves:
            board.make_move(r, c, self.MACHINE)
            
            # Gọi đệ quy hàm minimax
            score = self._minimax_rec(board, self.max_depth - 1, False, move_score, r, c, alpha, beta, game_logic)
            
            # Rút lại nước đi để làm sạch trạng thái bàn cờ
            board.undo_move(r, c)
            
            # Cập nhật nước đi tốt nhất
            if score > best_score:
                best_score = score
                best_move = (r, c)
                
            alpha = max(alpha, best_score)
                
        execution_time = time.time() - start_time
        
        # Báo cáo ra terminal
        print(f"[Minimax] Độ sâu: {self.max_depth} | Trạng thái đã xét: {self.node_count} "
              f"| Thời gian: {execution_time:.4f}s | Chọn nước: {best_move} | Điểm: {best_score}")
              
        return best_move, best_score

    def _minimax_rec(self, board, depth, is_maximizing, current_score, last_r, last_c, alpha, beta, game_logic):
        """
        Hàm đệ quy duyệt cây Minimax theo cách cộng dồn điểm (current_score).
        Có áp dụng cắt tỉa Alpha-Beta.
        
        Args:
            board: Bàn cờ hiện tại
            depth: Độ sâu còn lại
            is_maximizing: True (MAX - Máy), False (MIN - Người)
            current_score: Điểm tổng tích lũy từ gốc cây xuống tới node hiện tại
            last_r, last_c: Tọa độ nước đi vừa thực hiện (để kiểm tra kết thúc/thắng)
            alpha: Giá trị tốt nhất của MAX trên nhánh tìm kiếm
            beta: Giá trị tốt nhất của MIN trên nhánh tìm kiếm
            game_logic: Đối tượng xử lý luật chơi
        """
        self.node_count += 1
        
        # 1. Kiểm tra điều kiện dừng (Base Cases)
        # Truyền board và tọa độ vừa đánh vào hàm check_winner để tối ưu
        winner, _ = game_logic.check_winner(board, last_r, last_c)
        if winner == self.MACHINE:
            return 1000000000 + depth * 10000000 + current_score  # Ưu tiên thắng càng sớm càng tốt
        elif winner == self.PLAYER:
            return -1000000000 - depth * 10000000 + current_score # Trì hoãn thua càng lâu càng tốt
            
        # Nếu bàn cờ đầy hoặc đã duyệt hết độ sâu cho phép
        if board.is_full() or depth == 0:
            return current_score
            
        # Lấy danh sách ô trống để duyệt tiếp (bán kính 2 để tối ưu)
        empty_cells = board.get_empty_cells(radius=2)
        
        # 2. Xử lý logic 2 nhánh MAX và MIN
        if is_maximizing:
            # Nhánh MAX (Lượt Máy)
            max_eval = -float('inf')
            ordered_moves = self._get_ordered_moves(board, empty_cells, True)
            
            for move_score, r, c in ordered_moves:
                board.make_move(r, c, self.MACHINE)
                eval_score = self._minimax_rec(board, depth - 1, False, current_score + move_score, r, c, alpha, beta, game_logic)
                board.undo_move(r, c)
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
                
            return max_eval
            
        else:
            # Nhánh MIN (Lượt Người)
            min_eval = float('inf')
            ordered_moves = self._get_ordered_moves(board, empty_cells, False)
            
            for move_score, r, c in ordered_moves:
                board.make_move(r, c, self.PLAYER)
                eval_score = self._minimax_rec(board, depth - 1, True, current_score + move_score, r, c, alpha, beta, game_logic)
                board.undo_move(r, c)
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
                
            return min_eval

    def _get_ordered_moves(self, board, empty_cells, is_maximizing):
        """
        Sắp xếp các nước đi (Move Ordering) dựa trên điểm đánh giá cục bộ.
        Việc này giúp các nhánh tốt nhất được duyệt trước, tối ưu hóa quá trình tính toán.
        """
        moves_with_scores = []
        for r, c in empty_cells:
            if is_maximizing:
                # MAX muốn điểm tấn công cao và đối thủ bị chặn
                board.make_move(r, c, self.MACHINE)
                attack_score = self.evaluator.evaluate_local(board.grid, r, c)
                board.undo_move(r, c)
                
                board.make_move(r, c, self.PLAYER)
                defense_score = self.evaluator.evaluate_local(board.grid, r, c)
                board.undo_move(r, c)
                
                score = attack_score - defense_score
            else:
                # MIN muốn điểm tấn công của mình cao (âm nhiều) và đối thủ (MAX) bị chặn
                board.make_move(r, c, self.PLAYER)
                attack_score = self.evaluator.evaluate_local(board.grid, r, c)
                board.undo_move(r, c)
                
                board.make_move(r, c, self.MACHINE)
                defense_score = self.evaluator.evaluate_local(board.grid, r, c)
                board.undo_move(r, c)
                
                score = attack_score - defense_score
                
            moves_with_scores.append((score, r, c))
            
        # Sắp xếp: MAX ưu tiên điểm cao (giảm dần), MIN ưu tiên điểm thấp (tăng dần)
        moves_with_scores.sort(key=lambda x: x[0], reverse=is_maximizing)
        return moves_with_scores
