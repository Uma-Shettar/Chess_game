import random


# Chooses a random move from the legal-move list.
def get_random_move(valid_moves):
    return valid_moves[random.randint(0, len(valid_moves) - 1)]

PIECE_SCORE = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "P": 1}
CHECKMATE = 1000
DEPTH = 3

# Positive score means white is winning, negative score means black is winning
def score_board(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == "W":
                score += PIECE_SCORE[square[1]]
            elif square[0] == "B":
                score -= PIECE_SCORE[square[1]]
    return score

# Searches legal moves and returns the best move and its score.
def Best_move(s, valid_moves, depth = DEPTH):
    global next_move
    next_move = None
    if not valid_moves:
        return None, 0
    random.shuffle(valid_moves)
    best_score = Find_move(
        s,
        valid_moves,
        depth,
        1 if s.white_turn else -1,
        is_root=True
    )
    return next_move, best_score

# Recursively scores move sequences.
def Find_move(s, valid_moves, depth, turn_sign, is_root=False):
    global next_move
    if s.checkmate:
        return -CHECKMATE
    if s.draw:
        return 0
    if not valid_moves:
        return 0
    if depth <= 0:
        return turn_sign * score_board(s.board)

    max_score = -CHECKMATE
    for move in valid_moves:
        s.play_move(move)
        next_moves = s.get_valid_moves()
        score = -Find_move(s, next_moves, depth - 1, -turn_sign)
        if score > max_score:
            max_score = score
            if is_root:
                next_move = move
        s.Undo()
    return max_score
        
