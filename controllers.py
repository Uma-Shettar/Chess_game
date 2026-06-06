
class State():
    def __init__(self):
        self.board = [
            ["BR", "BN", "BB", "BQ", "BK", "BB", "BN", "BR"],
            ["BP", "BP", "BP", "BP", "BP", "BP", "BP", "BP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["WP", "WP", "WP", "WP", "WP", "WP", "WP", "WP"],
            ["WR", "WN", "WB", "WQ", "WK", "WB", "WN", "WR"]
        ]
        self.log = []
        self.white_turn = True
    
    def play_move(self, move):
        self.board[move.from_row][move.from_column] = "--"
        self.board[move.to_row][move.to_column] = move.piece_moved
        self.log.append(move)
        self.white_turn = not self.white_turn
    
    def Undo(self):
        if len(self.log) != 0:
            move = self.log.pop()
            self.board[move.from_row][move.from_column] = move.piece_moved
            self.board[move.to_row][move.to_column] = move.piece_taken
            self.white_turn = not self.white_turn

class Move():
    def __init__(self, from_pos, to_pos, board):
        self.from_row = from_pos[0]
        self.from_column = from_pos[1]
        self.to_row = to_pos[0]
        self.to_column = to_pos[1]
        self.piece_taken = board[self.to_row][self.to_column]
        self.piece_moved = board[self.from_row][self.from_column]
        