import tkinter as tk
from tkinter import ttk, messagebox
import json
import math
from typing import Dict, Tuple, List, Optional

class InfiniteBoard:
    """Quản lý bàn cờ vô tận"""
    
    def __init__(self):
        self.cells = {}  # (x, y) -> 'X' or 'O'
        self.moves_history = []
        self.current_player = 'X'
        self.game_over = False
        self.winner = None
        self.boundaries = {
            'min_x': 0, 'max_x': 0, 
            'min_y': 0, 'max_y': 0
        }
    
    def make_move(self, x: int, y: int, player: str) -> bool:
        """Thực hiện nước đi"""
        if self.game_over or (x, y) in self.cells:
            return False
            
        self.cells[(x, y)] = player
        self.moves_history.append((x, y, player))
        self.expand_boundaries(x, y)
        
        if self.check_win(x, y, player):
            self.game_over = True
            self.winner = player
        elif len(self.moves_history) >= 225:  # 15x15 board max
            self.game_over = True
            self.winner = 'DRAW'
            
        self.current_player = 'O' if player == 'X' else 'X'
        return True
    
    def expand_boundaries(self, x: int, y: int):
        """Mở rộng biên bàn cờ"""
        self.boundaries['min_x'] = min(self.boundaries['min_x'], x)
        self.boundaries['max_x'] = max(self.boundaries['max_x'], x)
        self.boundaries['min_y'] = min(self.boundaries['min_y'], y)
        self.boundaries['max_y'] = max(self.boundaries['max_y'], y)
    
    def check_win(self, x: int, y: int, player: str) -> bool:
        """Kiểm tra chiến thắng từ vị trí (x,y)"""
        directions = [
            [(1, 0), (-1, 0)],   # Horizontal
            [(0, 1), (0, -1)],   # Vertical
            [(1, 1), (-1, -1)],  # Diagonal \
            [(1, -1), (-1, 1)]   # Diagonal /
        ]
        
        for dir_pair in directions:
            count = 1  # Current cell
            
            # Check both directions
            for dx, dy in dir_pair:
                temp_x, temp_y = x, y
                for _ in range(4):  # Check 4 more in this direction
                    temp_x += dx
                    temp_y += dy
                    if self.cells.get((temp_x, temp_y)) == player:
                        count += 1
                    else:
                        break
            
            if count >= 5:
                return True
                
        return False
    
    def get_board_state(self) -> Dict:
        """Trả về trạng thái bàn cờ"""
        return {
            'cells': self.cells.copy(),
            'current_player': self.current_player,
            'game_over': self.game_over,
            'winner': self.winner,
            'boundaries': self.boundaries.copy()
        }
    
    def undo_move(self) -> bool:
        """Hoàn tác nước đi cuối"""
        if not self.moves_history:
            return False
            
        x, y, player = self.moves_history.pop()
        del self.cells[(x, y)]
        self.current_player = player
        self.game_over = False
        self.winner = None
        self.update_boundaries()
        return True
    
    def update_boundaries(self):
        """Cập nhật lại biên sau khi undo"""
        if not self.cells:
            self.boundaries = {'min_x': 0, 'max_x': 0, 'min_y': 0, 'max_y': 0}
            return
            
        coords = list(self.cells.keys())
        self.boundaries['min_x'] = min(x for x, y in coords)
        self.boundaries['max_x'] = max(x for x, y in coords)
        self.boundaries['min_y'] = min(y for x, y in coords)
        self.boundaries['max_y'] = max(y for x, y in coords)

class MinimaxAI:
    """AI sử dụng thuật toán Minimax"""
    
    def __init__(self, difficulty: str = 'MEDIUM'):
        self.difficulty = difficulty
        self.depth = self.get_depth_by_difficulty()
        self.player = 'O'  # AI là O
    
    def get_depth_by_difficulty(self) -> int:
        """Xác định độ sâu theo cấp độ"""
        return {
            'EASY': 2,
            'MEDIUM': 3,
            'HARD': 4
        }.get(self.difficulty, 2)
    
    def get_best_move(self, board: InfiniteBoard) -> Tuple[int, int]:
        """Tìm nước đi tốt nhất"""
        best_score = -math.inf
        best_move = None
        
        # Lấy các nước đi khả thi (xung quanh các quân đã đánh)
        possible_moves = self.get_possible_moves(board)
        
        for move in possible_moves:
            x, y = move
            board.make_move(x, y, self.player)
            score = self.minimax(board, self.depth - 1, False, -math.inf, math.inf)
            board.undo_move()
            
            if score > best_score:
                best_score = score
                best_move = (x, y)
        
        return best_move if best_move else self.get_fallback_move(board)
    
    def get_possible_moves(self, board: InfiniteBoard) -> List[Tuple[int, int]]:
        """Lấy danh sách nước đi khả thi"""
        moves = set()
        occupied_cells = board.cells.keys()
        
        # Thêm các ô xung quanh quân cờ hiện có
        for x, y in occupied_cells:
            for dx in range(-2, 3):
                for dy in range(-2, 3):
                    if dx == 0 and dy == 0:
                        continue
                    new_x, new_y = x + dx, y + dy
                    if (new_x, new_y) not in occupied_cells:
                        moves.add((new_x, new_y))
        
        # Nếu bàn cờ trống, đánh ở trung tâm
        if not moves:
            moves.add((0, 0))
            
        return list(moves)
    
    def minimax(self, board: InfiniteBoard, depth: int, is_maximizing: bool, alpha: float, beta: float) -> float:
        """Thuật toán Minimax với Alpha-Beta pruning"""
        if depth == 0 or board.game_over:
            return self.evaluate_board(board)
        
        possible_moves = self.get_possible_moves(board)
        
        if is_maximizing:
            max_score = -math.inf
            for move in possible_moves:
                x, y = move
                board.make_move(x, y, self.player)
                score = self.minimax(board, depth - 1, False, alpha, beta)
                board.undo_move()
                max_score = max(max_score, score)
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
            return max_score
        else:
            min_score = math.inf
            opponent = 'X' if self.player == 'O' else 'O'
            for move in possible_moves:
                x, y = move
                board.make_move(x, y, opponent)
                score = self.minimax(board, depth - 1, True, alpha, beta)
                board.undo_move()
                min_score = min(min_score, score)
                beta = min(beta, score)
                if beta <= alpha:
                    break
            return min_score
    
    def evaluate_board(self, board: InfiniteBoard) -> float:
        """Đánh giá trạng thái bàn cờ"""
        if board.game_over:
            if board.winner == self.player:
                return 1000
            elif board.winner and board.winner != self.player:
                return -1000
            else:
                return 0
        
        score = 0
        patterns = {
            'XXXXX': 1000, 'OOOOO': -1000,
            'XXXX': 100, 'OOOO': -100,
            'XXX': 10, 'OOO': -10,
            'XX': 1, 'OO': -1
        }
        
        # Đơn giản hóa evaluation function
        # Trong thực tế cần implement pattern detection đầy đủ
        return score
    
    def get_fallback_move(self, board: InfiniteBoard) -> Tuple[int, int]:
        """Nước đi dự phòng nếu không tìm được nước tốt"""
        possible_moves = self.get_possible_moves(board)
        return possible_moves[0] if possible_moves else (0, 0)
