
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
        self.get_moves_function = {'P' : self.get_pawn_moves, 'R': self.get_rook_moves, 'N': self.get_knight_moves,
                                   'B': self.get_bishop_moves, 'Q': self.get_queen_moves, 'K': self.get_king_moves, '-': self.return_empty}
    
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
    
    def get_valid_moves(self):  # check validity considerin checks
        print("valid moves")
        return self.get_all_moves_possible() # for now ignoring checks
    
    def get_all_moves_possible(self):
        moves = []
        print("get_all_moves")
        for r in range(len(self.board)):
            for c in range(len(self.board)):
                piece_color = self.board[r][c][0]
                if (piece_color == 'W' and self.white_turn) or (piece_color == 'B' and not self.white_turn):
                    piece = self.board[r][c][1]
                    moves = moves + self.get_piece_moves(r, c, piece) 
        return moves
    
    def get_piece_moves(self, r, c, piece):
        print("get_piece_moves")
        return self.get_moves_function[piece](r, c)
    
    def get_pawn_moves(self, r, c):
        print("get_pawn_moves")
        moves=[]
        if self.white_turn and self.board[r][c][0] == 'W':
            if self.board[r-1][c] == "--":
                print("1")
                moves.append(Move((r,c),(r-1,c),self.board))
                if self.board[r-2][c] == "--" and r == 6:
                    moves.append(Move((r,c),(r-2,c),self.board))
                    print("2")
            if c-1>=0:
                if self.board[r-1][c-1][0] == "B":
                    moves.append(Move((r,c),(r-1,c-1),self.board))
            if c+1<=7:
                if self.board[r-1][c+1][0] == "B":
                    moves.append(Move((r,c),(r-1,c+1),self.board))
        elif self.board[r][c][0] == 'B':
            if self.board[r+1][c] == "--":
                moves.append(Move((r,c),(r+1,c),self.board))
                if self.board[r+2][c] == "--" and r == 1:
                    moves.append(Move((r,c),(r+2,c),self.board))
            if c-1>=0:
                if self.board[r+1][c-1][0] == "W":
                    moves.append(Move((r,c),(r+1,c-1),self.board))
            if c+1<=7:
                if self.board[r+1][c+1][0] == "W":
                    moves.append(Move((r,c),(r+1,c+1),self.board))
        return moves
        

    def get_rook_moves(self, r, c):
        moves = []
        move_directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        opponent_color = 'B' if self.white_turn else 'W'
        if self.board[r][c][0] != opponent_color:
            for md in move_directions:
                for i in range(1,8):
                    to_row = r + md[0]*i
                    to_column = c + md[1]*i
                    if 0<= to_row <= 7 and 0 <= to_column <= 7:
                        square = self.board[to_row][to_column]
                        if square == "--":
                            moves.append(Move((r,c),(to_row, to_column),self.board))
                        elif square[0] == opponent_color:
                            moves.append(Move((r,c),(to_row, to_column),self.board))
                            break
                        else:
                            break
                    else:
                        break

            return moves

    def get_knight_moves(self, r, c):
        moves = []
        move_directions = [(-2, -1), (-2, 1), (2, -1), (2, 1), (1, -2), (-1, -2), (1, 2), (-1, 2)]
        opponent_color = 'B' if self.white_turn else 'W'
        if self.board[r][c][0] != opponent_color:
            for md in move_directions:
                to_row = r + md[0]
                to_column = c + md[1]
                if 0<= to_row <= 7 and 0 <= to_column <= 7:
                    square = self.board[to_row][to_column]
                    if square == "--":
                        moves.append(Move((r,c),(to_row, to_column),self.board))
                    elif square[0] == opponent_color:
                        moves.append(Move((r,c),(to_row, to_column),self.board))

        return moves

    def get_bishop_moves(self, r, c):
        moves = []
        move_directions = [(-1, -1), (1, 1), (1, -1), (-1, 1)]
        opponent_color = 'B' if self.white_turn else 'W'
        if self.board[r][c][0] != opponent_color:
            for md in move_directions:
                for i in range(1,8):
                    to_row = r + md[0]*i
                    to_column = c + md[1]*i
                    if 0<= to_row <= 7 and 0 <= to_column <= 7:
                        square = self.board[to_row][to_column]
                        if square == "--":
                            moves.append(Move((r,c),(to_row, to_column),self.board))
                        elif square[0] == opponent_color:
                            moves.append(Move((r,c),(to_row, to_column),self.board))
                            break
                        else:
                            break
                    else:
                        break

            return moves

    def get_queen_moves(self, r, c):
        moves = []
        opponent_color = 'B' if self.white_turn else 'W'
        if self.board[r][c][0] != opponent_color:
            moves += self.get_rook_moves(r, c)
            moves += self.get_bishop_moves(r, c)
        return moves

    def get_king_moves(self, r, c):
        moves = []
        move_directions = [(-1, -1), (-1, 1), (-1, 0), (0,1), (0, -1), (1, -1), (1, 1), (1, 0)]
        opponent_color = 'B' if self.white_turn else 'W'
        if self.board[r][c][0] != opponent_color:
            for md in move_directions:
                to_row = r + md[0]
                to_column = c + md[1]
                if 0<= to_row <= 7 and 0 <= to_column <= 7:
                    square = self.board[to_row][to_column]
                    if square == "--":
                        moves.append(Move((r,c),(to_row, to_column),self.board))
                    elif square[0] == opponent_color:
                        moves.append(Move((r,c),(to_row, to_column),self.board))

        return moves
    
    def return_empty(self,r,c):
        return []

class Move():
    def __init__(self, from_pos, to_pos, board):
        self.from_row = from_pos[0]
        self.from_column = from_pos[1]
        self.to_row = to_pos[0]
        self.to_column = to_pos[1]
        self.piece_taken = board[self.to_row][self.to_column]
        self.piece_moved = board[self.from_row][self.from_column]
        self.move_id = 1000*self.from_row + 100*self.from_column + 10*self.to_row + 1*self.to_column
        print(self.move_id)
    
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_id == other.move_id
        return False
        