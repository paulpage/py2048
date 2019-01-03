#!/usr/bin/python2.7
import random
import pygame
import pygame.freetype
import pygame.gfxdraw
from button import Button
from game import Board

#GUI
button_restart = Button("restart.png", 342, 400)
button_help = Button("help.png", 371, 400)

done = False
message = ""
pygame.init()
clock = pygame.time.Clock()
size = (400, 430)
screen = pygame.display.set_mode(size)
GRAY = (150, 150, 150)
auto = False
board = Board(4, 4)
animate_percentage = 0
last_direction = 'up'

# Creates a copy of the board's grid so that it can be compared against a later version
def copy(board):
    grid = []
    for value in board.grid:
        grid.append(value)
    return grid

old_grid = copy(board)

IMAGES = [
    pygame.image.load("0.png"),
    pygame.image.load("2.png"),
    pygame.image.load("4.png"),
    pygame.image.load("8.png"),
    pygame.image.load("16.png"),
    pygame.image.load("32.png"),
    pygame.image.load("64.png"),
    pygame.image.load("128.png"),
    pygame.image.load("256.png"),
    pygame.image.load("512.png"),
    pygame.image.load("1024.png"),
    pygame.image.load("2048.png")
]

BG_COLOR = pygame.Color('#282828')

COLORS = [
    BG_COLOR,
    pygame.Color('#689d6a'),
    pygame.Color('#427b58'),
    pygame.Color('#b16286'),
    pygame.Color('#8f3f71'),
    pygame.Color('#458588'),
    pygame.Color('#076678'),
    pygame.Color('#d79921'),
    pygame.Color('#b57614'),
    pygame.Color('#98971a'),
    pygame.Color('#79740e'),
    pygame.Color('#cc241d'),
    pygame.Color('#9d0006'),
]

def quitGame():
    global done
    done = True

def move(direction):
    global animate_percentage, old_grid, last_direction
    animate_percentage = 0
    old_grid = copy(board)
    if board.move(direction):
        board.new_tile()
    last_direction = direction

def move_left(): move('left')
def move_right(): move('right')
def move_up(): move('up')
def move_down(): move('down')

def autoPlay(): #Random automatic 2048! Partially for debugging, partially for fun
    if auto:
        directions = [move_up, move_right, move_left, move_down]
        random.choice(directions)()

def autoSwitch():
    global auto
    auto = not auto

auto_disallowed_keys = [
    pygame.K_LEFT,
    pygame.K_RIGHT,
    pygame.K_UP,
    pygame.K_DOWN
]

def restart():
    global board
    board = Board(4, 4)
    old_grid = copy(board)
    board.new_tile()
    board.new_tile()

key_action = {
    pygame.K_LEFT : move_left,
    pygame.K_RIGHT : move_right,
    pygame.K_UP : move_up,
    pygame.K_DOWN : move_down,
    pygame.K_r : restart,
    pygame.K_q : quitGame,
    pygame.K_a : autoSwitch,
}

SCALE = 100

def draw_tile(x, y, offsetx=0, offsety=0, scale=100):

    padding = int(SCALE / 20)
    width = SCALE + padding
    height = SCALE + padding
    r = int(0.20 * SCALE) # Radius of the rounded corners
    color = COLORS[board.get(x, y)]

    rounded_rect = pygame.Surface((width, height))
    rounded_rect.fill(BG_COLOR)

    circle_centers = [
        (r, r),
        (r, height - r),
        (width - r, r),
        (width - r, height - r),
    ]

    rects = [
        (r, 0, width - (2 * r), height),
        (0, r, width, height - (2 * r)),
    ]

    for center in circle_centers:
        pygame.gfxdraw.aacircle(rounded_rect, center[0], center[1], r - 0, color)
        pygame.gfxdraw.filled_circle(rounded_rect, center[0], center[1], r - 0, color)
        # pygame.draw.circle(rounded_rect, COLORS[board.get(x, y)], center, r)

    for rect in rects:
        pygame.draw.rect(rounded_rect, COLORS[board.get(x, y)], rect)

    # rounded_rect.fill((255, 255, 255, 0.5), special_flags=pygame.BLEND_RGBA_MAX)
    # rounded_rect.fill((255,255,255, 0.5),special_flags=pygame.BLEND_RGBA_MIN)

    font_size = SCALE / 5 * scale / 100
    font = pygame.freetype.Font(None, size=font_size)
    text = font.render(str(2 ** board.get(x, y)), fgcolor=(255, 255, 255), size=font_size)[0]
    text_rect = text.get_rect(center=(width / 2, height / 2))
    rounded_rect.blit(text, text_rect)

    # scale_offset = SCALE / 2 * (100 - scale) / 100

    # top    = (y * SCALE + r + padding) + offsetx
    # bottom = (y * SCALE + SCALE - r - padding) - offsetx
    # left   = (x * SCALE + r + padding) + offsety
    # right  = (x * SCALE + SCALE - r - padding) - offsety

    # circle_centers = [
    #     (left, top),
    #     (left, bottom),
    #     (right, top),
    #     (right, bottom),
    # ]

    # small = SCALE - (padding + scale_offset + r) * 2
    # large = SCALE - (padding + scale_offset) * 2

    # rects = [
    #     (left - r, top, large, small),
    #     (left, top - r, small, large),
    # ]

    # for center in circle_centers:
    #     pygame.draw.circle(screen, COLORS[board.get(x, y)], center, r)

    # for rect in rects:
    #     pygame.draw.rect(screen, COLORS[board.get(x, y)], rect)

    # font_size = SCALE / 5 * scale / 100
    # font = pygame.freetype.Font(None, size=font_size)
    # text = font.render(str(2 ** board.get(x, y)), fgcolor=(255, 255, 255), size=font_size)[0]
    # text_rect = text.get_rect(center=(x * SCALE + SCALE / 2, y * SCALE + SCALE / 2))
    # screen.blit(text, text_rect)
    
    # text = str(2 ** board.get(x, y))
    # rendered_text = font.render(text)
    # text_bounds = font.get_rect(rendered_text, size=int(SCALE / 5 * (100 - scale) / 100))
    # font.render_to(screen, ((x * SCALE - text_bounds.width) / 2, (y * SCALE - text_bounds.height) / 2), None, fgcolor=(255, 255, 255))

    screen.blit(
            pygame.transform.smoothscale(
                rounded_rect,
                (scale * 90 / 100, scale * 90 / 100)),
            ((x * 100 + .5 * (100 - scale) + 5) + offsetx, (y * 100 + (.5 * (100 - scale) + 5)) + offsety))

def draw(direction):
    global animate_percentage
    pygame.display.set_caption("Score: " + str(board.score) + "        " + message)
    screen.fill(BG_COLOR)
    button_restart.draw(screen)
    button_help.draw(screen)
    changed = board
    ranges = {
        'left': range(board.width),
        'right': range(board.width),
        'up': range(board.height),
        'down': range(board.height),
    }

    if direction == 'left' or direction == 'right':
        for y in range(board.height):
            animated = False
            for x in ranges[direction]:
                if board.get(x, y) != old_grid[y * board.width + x]:
                    animated = True
                if animated and board.get(x, y) != 0:
                    if direction == 'left':
                        draw_tile(x, y, 1 * (100 - animate_percentage), 0, max(animate_percentage, 50))
                    else:
                        draw_tile(x, y, -(1 * (100 - animate_percentage)), 0, max(animate_percentage, 50))
                elif board.get(x, y) != 0:
                    draw_tile(x, y)
    else:
        for x in range(board.width):
            animated = False
            for y in ranges[direction]:
                if board.get(x, y) != old_grid[y * board.width + x]:
                    animated = True
                if animated and board.get(x, y) != 0:
                    if direction == 'up':
                        draw_tile(x, y, 0, 1 * (100 - animate_percentage), max(animate_percentage, 50))
                    else:
                        draw_tile(x, y, 0, -(1 * (100 - animate_percentage)), max(animate_percentage, 50))
                elif board.get(x, y) != 0:
                    draw_tile(x, y)
    animate_percentage = min(100, animate_percentage + 12) #Make sure that the animation percentage doesn't go above 100
    pygame.display.flip()

if __name__ == "__main__":
    restart()
    message = "Use arrow keys to move."

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                try:
                    if auto and not event.key in auto_disallowed_keys:
                        #Don't allow movement while auto is on
                        key_action[event.key]()
                    elif not auto:
                        key_action[event.key]()
                except KeyError:
                    pass
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_restart.clickable():
                    restart()
                elif button_help.clickable():
                    message = "Use arrow keys to move."

        if auto and animate_percentage >= 100:
            autoPlay()
            message = "Auto is on."
        draw(last_direction)
        clock.tick(60)
    pygame.quit()
