
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
        self.castling_rights = Castling(True, True, True, True)
        self.castling_log = [Castling(self.castling_rights.w_oo, self.castling_rights.b_oo, self.castling_rights.w_ooo, self.castling_rights.b_ooo)]


    def play_move(self, move):
        self.board[move.from_row][move.from_column] = "--"
        self.board[move.to_row][move.to_column] = move.piece_moved
        self.log.append(move)
        self.white_turn = not self.white_turn
        if move.piece_moved == "WK":
            self.white_king = (move.to_row, move.to_column)
        if move.piece_moved == "BK":
            self.black_king = (move.to_row, move.to_column)

        # Castling
        self.change_castling_rights(move.piece_moved, move.from_row, move.from_column)
        self.castling_log.append(Castling(self.castling_rights.w_oo, self.castling_rights.b_oo, self.castling_rights.w_ooo, self.castling_rights.b_ooo)) 
        
        if move.piece_moved[1] == "K":
            if move.to_column - move.from_column == 2:
                self.board[move.from_row][move.to_column - 1] = self.board[move.from_row][move.to_column + 1]
                self.board[move.from_row][move.to_column + 1] = "--"
            elif move.to_column - move.from_column == -2:
                self.board[move.from_row][move.to_column + 1] = self.board[move.from_row][move.to_column - 2]
                self.board[move.from_row][move.to_column - 2] = "--"
        print("Do",move.move_id, "log_size", len(self.castling_log))
        print("Castling Rights",self.castling_rights.w_oo, self.castling_rights.b_oo, self.castling_rights.w_ooo, self.castling_rights.b_ooo)

    
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

            self.castling_log.pop()
            rights = self.castling_log[-1]
            self.castling_rights = Castling(rights.w_oo,rights.b_oo,rights.w_ooo,rights.b_ooo)
                
            
            if move.piece_moved[1] == "K":
                if move.to_column - move.from_column == 2:
                    self.board[move.from_row][move.to_column + 1] = self.board[move.from_row][move.to_column - 1]
                    self.board[move.from_row][move.to_column - 1] = "--"
                elif move.to_column - move.from_column == -2:
                    self.board[move.from_row][move.to_column - 2] = self.board[move.from_row][move.to_column + 1]
                    self.board[move.from_row][move.to_column + 1] = "--"
            print("undo",move.move_id, "log_size", len(self.castling_log))
            print("Castling Rights",self.castling_rights.w_oo, self.castling_rights.b_oo, self.castling_rights.w_ooo, self.castling_rights.b_ooo)


    def change_castling_rights(self, piece, row, column):
        if piece == "BK":
            self.castling_rights.b_oo = False
            self.castling_rights.b_ooo = False
        elif piece == "WK":
            self.castling_rights.w_oo = False
            self.castling_rights.w_ooo = False
        elif piece == "WR":
            if row == 7:
                if column == 0:
                    self.castling_rights.w_ooo = False
                elif column == 7:
                    self.castling_rights.w_oo = False
        elif piece == "BR":
            if row == 0:
                if column == 0:
                    self.castling_rights.b_ooo = False
                elif column == 7:
                    self.castling_rights.b_oo = False
        
    def get_valid_moves(self):  # check validity considering checks
        moves = []
        self.check, self.pins, self.checks = self.get_checks()
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
                moves = self.get_king_moves(king_r, king_c)
        else:
            moves = self.get_all_moves_possible()
        king_moves = self.get_king_moves(king_r, king_c)
        for i in range(len(moves) -1, -1, -1):
            if moves[i].piece_moved[1] == "K":
                if not moves[i] in king_moves:
                    print("rem",moves[i].piece_moved, moves[i].from_row,moves[i].from_column,moves[i].to_row,moves[i].to_column)
                    moves.remove(moves[i])
        return moves


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
                        if pin == ():
                            pin = (row_position, column_position)
                        else:
                            break
                    elif piece[0] == opponent_color:
                        Piece_type = piece[1]
                        if ((i == 1 and Piece_type == "P" and ((opponent_color == "B" and 0<= j <= 1) or (opponent_color == "W" and 2 <= j <= 3))) or (0 <= j <= 3 and Piece_type == "B") or (4 <= j <= 7 and Piece_type == "R") or (i == 1 and Piece_type == "K")) or (Piece_type == "Q"):

                            if pin == ():
                                check = True
                                checks.append((row_position, column_position, d[0], d[1]))
                                break
                            else:
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
        elif not self.white_turn and self.board[r][c][0] == 'B':
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
        # check if move leads to king being in a square which is under attack and remove it from moves list 
            for i in range(len(moves)-1,-1,-1):
                self.play_move(moves[i])
                self.white_turn = not self.white_turn
                check,_,_ = self.get_checks()
                if check :
                    print('removed',moves[i], moves[i].from_row,moves[i].from_column,moves[i].to_row, moves[i].to_column)
                    moves.remove(moves[i])
                self.white_turn = not self.white_turn
                self.Undo()

            # Castling moves
            check,_,_ = self.get_checks()
            if not check:
                if (self.white_turn and self.castling_rights.w_oo) or (not self.white_turn and self.castling_rights.b_oo):
                    list = (c+1,c+2)
                    if 0<= c+2 <= 7:
                        if self.check_castle_condition(r,c,list):
                            moves.append(Move((r,c), (r,c+2), self.board))

                if (self.white_turn and self.castling_rights.w_ooo) or (not self.white_turn and self.castling_rights.b_ooo):
                    list = (c-1,c-2,c-3)
                    if 0<= c-3 <= 7:
                        if self.check_castle_condition(r,c,list):
                            moves.append(Move((r,c), (r,c-2), self.board))

        return moves

    def check_castle_condition(self,r,c,list):
        king = self.board[r][c]
        self.board[r][c] = "--"
        condition = True
        for col_p in list:
            if self.board[r][col_p] != "--":
                condition = False
                break
            self.board[r][col_p] = king
            check,_,_ = self.get_checks()
            self.board[r][col_p] = "--"
            if check:
                condition = False
                break
        self.board[r][c] = king
        return condition
    
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
        

class Castling():
    def __init__(self, w_oo, b_oo, w_ooo, b_ooo):
        self.w_oo = w_oo  # white short castling
        self.b_oo = b_oo  # black short castling

        self.w_ooo = w_ooo # white long castling
        self.b_ooo = b_ooo # black long castling
