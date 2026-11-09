
import pygame as p

import auto_move
import controllers
from RL_AI_move import ChessAI

height = width = 512
square_size = 512//8
fps = 15
images = {}



def load_images():
    for i in ["BR", "BN", "BB", "BQ", "BK", "BP", "WR", "WN", "WB", "WQ", "WK", "WP"]:
        images[i] = p.transform.scale(p.image.load("images\\" + i + ".png"),(square_size - 12, square_size - 12))

def main():
    p.init()
    screen = p.display.set_mode((width, height))
    s = controllers.State()
    ai = ChessAI(
        model_path="chess_model.pth",
        simulations=200
    )
    valid_moves = s.get_valid_moves()
    print(valid_moves, len(valid_moves))
    move_done = False
    screen.fill(p.Color("grey"))
    clock = p.time.Clock()
    load_images()
    active = True
    selected_position = ()
    clicks_list = []
    game_over = False
    white_player = True
    black_player = True

    while active:
        player = (white_player and s.white_turn) or (black_player and not s.white_turn)
        for event in p.event.get():
            if event.type == p.QUIT:
                active = False


            elif event.type == p.MOUSEBUTTONDOWN:
                if not game_over and player:
                    click_coordinates = p.mouse.get_pos()
                    column = click_coordinates[0]//square_size
                    row = click_coordinates[1]//square_size
                    if selected_position != (row, column):
                        selected_position = (row, column)
                        clicks_list.append(selected_position)
                    else:
                        selected_position = ()
                        clicks_list = []

                    if len(clicks_list) == 2:
                        move = controllers.Move(clicks_list[0], clicks_list[1], s.board)
                        if move in valid_moves:
                            s.play_move(move)
                            move_done = True
                            selected_position, clicks_list = (), []
                        else:
                            clicks_list = [selected_position]


            elif event.type == p.KEYDOWN:
                if event.key == p.K_u:
                    s.Undo()
                    move_done = True
                    game_over = False
                if event.key == p.K_r:
                    s = controllers.State()
                    valid_moves = s.get_valid_moves()
                    selected_position, clicks_list = (), []
                    move_done = False
                    game_over = False

        #automatic move
        if not game_over and not player:
            #move,_ = auto_move.Best_move(s, valid_moves)
            move = ai.predict(s)
            if move is None:
                move = auto_move.get_random_move(valid_moves)
            # wait for 1 second before making the move
            # if not white_player and not black_player:
            #     p.time.wait(1000)
            s.play_move(move)
            move_done = True

        if move_done:
            valid_moves = s.get_valid_moves()
            move_done = False

        possible_moves = []
        if selected_position != ():
            r,c = selected_position
            moves = s.get_piece_moves(r, c, s.board[r][c][1])
    
            if moves:
                for m in moves:
                    possible_moves.append((m.to_row,m.to_column))
            #print(possible_moves)

        draw_state(screen, s.board, selected_position, possible_moves)

        if s.checkmate:
            game_over = True
            if s.white_turn:
                draw_text(screen, "Black wins by checkmate")
            else:
                draw_text(screen, "White wins by checkmate")
        
        if s.draw:
            game_over = True
            draw_text(screen, "Draw! Only kings left on the board")
            
        clock.tick(fps)
        p.display.flip()

def draw_state(screen, board, selected_position = None, possible_moves = None):
    for r in range(8):
        for c in range(8):
            if (r + c) % 2 == 0:
                color = p.Color("white")
            else:
                color = p.Color(69, 81, 107)
            p.draw.rect(screen, color, p.Rect(c*square_size, r*square_size, square_size, square_size))

            highlight = p.Surface((square_size, square_size))
            highlight.set_alpha(120)

            if selected_position == (r, c):
                highlight.fill(p.Color("yellow"))
                screen.blit(highlight, (c*square_size, r*square_size))
            
            highlight_p = p.Surface((square_size, square_size),p.SRCALPHA)
            p.draw.circle(highlight_p,(188, 103, 194, 180), (square_size // 2, square_size // 2),square_size // 5.5)

            if possible_moves and ((r, c) in possible_moves):
                #highlight_p.fill(p.Color(112, 185, 186))
                screen.blit(highlight_p, (c*square_size, r*square_size))
            
            piece = board[r][c]
            if piece != "--":
                screen.blit(images[piece], p.Rect(c*square_size + 6, r*square_size + 6, square_size, square_size))

def draw_text(screen, text):
    font = p.font.SysFont("Arial", 32, True, False)
    text_object = font.render(text, 0, p.Color("black"))
    text_location = p.Rect(0, 0, width, height).move(width/2 - text_object.get_width()/2, height/2 - text_object.get_height()/2)
    screen.blit(text_object, text_location)
    text_object = font.render(text, 0, p.Color("red"))
    screen.blit(text_object, text_location.move(2, 2))

if __name__ == "__main__":
    main()
