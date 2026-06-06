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
                    if s.board[clicks_list[0][0]][clicks_list[0][1]] != "--":
                        move = controllers.Move(clicks_list[0], clicks_list[1], s.board)
                        s.play_move(move)
                    selected_position, clicks_list = (), []
        
        draw_state(screen, s.board, selected_position)
            
        clock.tick(fps)
        p.display.flip()

def draw_state(screen, board, selected_position = None):
    for r in range(8):
        for c in range(8):
            if (r + c) % 2 == 0:
                color = p.Color("white")
            else:
                color = p.Color("grey")
            p.draw.rect(screen, color, p.Rect(c*square_size, r*square_size, square_size, square_size))

            if selected_position == (r, c):
                highlight = p.Surface((square_size, square_size))
                highlight.set_alpha(120)
                highlight.fill(p.Color("yellow"))
                screen.blit(highlight, (c*square_size, r*square_size))
            
            piece = board[r][c]
            if piece != "--":
                screen.blit(images[piece], p.Rect(c*square_size + 6, r*square_size + 6, square_size, square_size))

if __name__ == "__main__":
    main()
