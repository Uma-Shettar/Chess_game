import controllers
import pygame as p

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
    valid_moves = s.get_valid_moves()
    print(valid_moves, len(valid_moves))
    move_done = False
    screen.fill(p.Color("grey"))
    clock = p.time.Clock()
    load_images()
    active = True
    selected_position = ()
    clicks_list = []

    while active:
        for event in p.event.get():
            if event.type == p.QUIT:
                active = False
            elif event.type == p.MOUSEBUTTONDOWN:
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
                        print("play")
                        s.play_move(move)
                        move_done = True
                        selected_position, clicks_list = (), []
                    else:
                        clicks_list = [selected_position]
            elif event.type == p.KEYDOWN:
                if event.key == p.K_u:
                    s.Undo()
                    move_done = True
        if move_done:
            print("-----------------------\n---------------------------")
            valid_moves = s.get_valid_moves()
            print("enter", valid_moves)
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

if __name__ == "__main__":
    main()
