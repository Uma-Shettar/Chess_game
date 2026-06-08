
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
        self.white_king = (7,4)
        self.black_king = (0,4)
        self.checks = []
        self.pins = []
        self.check = False
    
    def play_move(self, move):
        self.board[move.from_row][move.from_column] = "--"
        self.board[move.to_row][move.to_column] = move.piece_moved
        self.log.append(move)
        self.white_turn = not self.white_turn
        if move.piece_moved == "WK":
            self.white_king = (move.to_row, move.to_column)
        if move.piece_moved == "BK":
            self.black_king = (move.to_row, move.to_column)
    
    def Undo(self):
        if len(self.log) != 0:
            move = self.log.pop()
            self.board[move.from_row][move.from_column] = move.piece_moved
            self.board[move.to_row][move.to_column] = move.piece_taken
            self.white_turn = not self.white_turn
            if move.piece_moved == "WK":
                self.white_king = (move.from_row, move.from_column)
            if move.piece_moved == "BK":
                self.black_king = (move.from_row, move.from_column)
        
    def get_valid_moves(self):  # check validity considering checks
        moves = []
        self.check, self.pins, self.checks = self.get_checks()
        print("check", self.check,"pins",self.pins, "checks",self.checks)
        if self.white_turn :
            king_r = self.white_king[0]
            king_c = self.white_king[1]
        else:
            king_r = self.black_king[0]
            king_c = self.black_king[1]
        
        
        if self.check:
            if len(self.checks) == 1:
                moves = self.get_all_moves_possible()
                check_info = self.checks[0]
                piece = self.board[check_info[0]][check_info[1]]
                valid_positions = []
                if piece[1] == "N":
                    valid_positions.append((check_info[0], check_info[1]))
                else:
                    for i in range(1, 8):
                        position = (king_r + i*check_info[2], king_c + i*check_info[3])
                        valid_positions.append(position)
                        if check_info[0] == position[0] and check_info[1] == position[1]:
                            break
                for i in range(len(moves) -1, -1, -1):
                    if moves[i].piece_moved[1] != "K":
                        if not (moves[i].to_row, moves[i].to_column) in valid_positions:
                            moves.remove(moves[i])
              
            else:
                moves = self.valid_king_moves(king_r, king_c)
        else:
            moves = self.get_all_moves_possible()
        king_moves = self.valid_king_moves(king_r, king_c)
        for i in range(len(moves) -1, -1, -1):
            print("bef",moves[i].to_row)
            if moves[i].piece_moved[1] == "K":
                if not moves[i] in king_moves:
                    print("rem",moves[i].piece_moved, moves[i].from_row,moves[i].from_column,moves[i].to_row,moves[i].to_column)
                    moves.remove(moves[i])
        return moves

    def valid_king_moves(self,r,c):
        king_moves = self.get_king_moves(r,c)
        for i in range(len(king_moves)-1,-1,-1):
            self.play_move(king_moves[i])
            self.white_turn = not self.white_turn
            check,_,_ = self.get_checks()
            print("check",check,"B", self.black_king,"W", self.white_king)
            print(self.board)
            if check :
                print('removed',king_moves[i], king_moves[i].from_row,king_moves[i].from_column,king_moves[i].to_row,king_moves[i].to_column)
                king_moves.remove(king_moves[i])
            self.white_turn = not self.white_turn
            self.Undo()
        return king_moves

    def get_checks(self):
        checks = []
        pins = []
        check = False
        
        if self.white_turn :
            opponent_color = "B"
            row = self.white_king[0]
            column = self.white_king[1]
        else:
            opponent_color = "W"
            row = self.black_king[0]
            column = self.black_king[1]

        directions = [(-1,-1), (-1,1), (1,-1), (1,1), (0,1), (0,-1),(1,0), (-1,0)]
        for j in range(len(directions)):
            d = directions[j]
            pin = ()
            for i in range(1, 8):
                row_position = row + d[0]*i
                column_position = column + d[1]*i

                if 0 <= row_position <= 7 and 0 <= column_position <= 7:
                    piece = self.board[row_position][column_position]
                    if piece[0] != opponent_color and piece[0] != "-":
                        print(4)
                        if pin == ():
                            pin = (row_position, column_position)
                        else:
                            break
                    elif piece[0] == opponent_color:
                        print(5)
                        Piece_type = piece[1]
                        if ((i == 1 and Piece_type == "P" and ((opponent_color == "B" and 0<= j <= 1) or (opponent_color == "W" and 2 <= j <= 3))) or (0 <= j <= 3 and Piece_type == "B") or (4 <= j <= 7 and Piece_type == "R") or (i == 1 and Piece_type == "K")) or (Piece_type == "Q"):

                            if pin == ():
                                print(pin)
                                check = True
                                checks.append((row_position, column_position, d[0], d[1]))
                                break
                            else:
                                print(7)
                                print("R",row,"C",column, "i",i,"PT", Piece_type,"j",j)
                                pins.append(pin)
                                break
                        else:
                            break
                    
        move_directions = [(-2, -1), (-2, 1), (2, -1), (2, 1), (1, -2), (-1, -2), (1, 2), (-1, 2)]
        for md in move_directions:
            to_row = row + md[0]
            to_column = column + md[1]
            if 0<= to_row <= 7 and 0 <= to_column <= 7:
                piece = self.board[to_row][to_column]
                if piece[0] == opponent_color and piece[1] == "N":
                    check = True
                    checks.append((to_row, to_column, md[0], md[1]))
        return check, pins, checks
                         
    
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
        return self.get_moves_function[piece](r, c)
    
    def get_pawn_moves(self, r, c):
        moves=[]
        if self.white_turn and self.board[r][c][0] == 'W':
            if self.board[r-1][c] == "--":
                moves.append(Move((r,c),(r-1,c),self.board))
                if self.board[r-2][c] == "--" and r == 6:
                    moves.append(Move((r,c),(r-2,c),self.board))
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
    
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_id == other.move_id
        return False
        