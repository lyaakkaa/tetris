import pygame, sys
from copy import deepcopy
from random import choice, randrange
from button import Button
import psycopg2
from config import params



TILE = 35
WIDTH, HEIGHT = 10, 20

GAME_RES = WIDTH * TILE, HEIGHT * TILE
RES = 750, 800
fps = 60

username = input("Enter your name:\n")

db  = psycopg2.connect(**params)
cursor = db.cursor()

pygame.init()
sc = pygame.display.set_mode(RES)
game_sc = pygame.Surface(GAME_RES)
clock = pygame.time.Clock()
sound = pygame.mixer.Sound('sounds\game.mp3')
sound_game_over = pygame.mixer.Sound('sounds\Gameover.wav')

grid  = [pygame.Rect(x * TILE, y * TILE, TILE, TILE) for x in range(WIDTH) for y in range(HEIGHT)]



figures_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
               [(0, -1), (-1, -1), (-1, 0), (0, 0)],
               [(-1, 0), (-1, 1), (0, 0), (0, -1)],
               [(0, 0), (-1, 0), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, 0)]]


figures = [[pygame.Rect(x + WIDTH // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in figures_pos]
figure_rect = pygame.Rect(0, 0, TILE - 2, TILE - 2)
field = [[0 for i in range(WIDTH)] for j in range(HEIGHT)]

anim_count, anim_speed, anim_limit = 0, 60, 2000


bg = pygame.image.load('assets\space.jpg').convert()


game_bg = pygame.image.load('assets\img2.jpg').convert()

main_font = pygame.font.Font('font\worlds.ttf', 65)
font = pygame.font.Font('font\worlds.ttf', 45)


def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("font/worlds.ttf", size)

title_tetris = main_font.render('TETRIS', True, pygame.Color('darkorange'))
title_score = font.render('score:', True, pygame.Color('green'))
title_record = font.render('record:', True, pygame.Color('purple'))


get_color = lambda : (randrange(30, 256), randrange(30, 256), randrange(30, 256))
figure, next_figure = deepcopy(choice(figures)), deepcopy(choice(figures))
color, next_color = get_color(), get_color()

score, lines = 0, 0
scores = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}








def get_record():
    try:
        with open('record') as f:
            return f.readline()
    except FileNotFoundError:
        with open('record', 'w') as f:
            f.write('0')


def set_record(record, score):
    rec = max(int(record), score)
    with open('record', 'w') as f:
        f.write(str(rec))



menu = True

while menu:
    def check_borders():
        if figure[i].x < 0 or figure[i].x > WIDTH - 1:
            return False
        elif figure[i].y > HEIGHT - 1 or field[figure[i].y][figure[i].x]:
            return False
        return True
    while True:
        last_score = score
        play = False
        sc.fill('red')
        MENU_MOUSE_POS = pygame.mouse.get_pos()
      
        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(380, 250), 
                            text_input="PLAY", font=get_font(25), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(380, 400), 
                            text_input="OPTIONS", font=get_font(25), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(380, 550), 
                            text_input="QUIT", font=get_font(25), base_color="#d7fcd4", hovering_color="White")
        LAST_SCORE_TEXT = font.render(f'your last score: {last_score}', True, "white")
        sc.blit(LAST_SCORE_TEXT, (150, -10))
        RECORD_TEXT = font.render(f'your record: {get_record()}', True, "black")
        sc.blit(RECORD_TEXT, (150, 60))
 
        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(sc)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    print('play')
                    play = True
                    
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    print('options')
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
                pass
        
        while play:
            sound.play()
            record = get_record()
            dx, rotate = 0, False
            sc.blit(bg, (0, 0))
            sc.blit(game_sc, (20, 20))
            game_sc.blit(game_bg, (0, 0))

            # delay for full lines
            for i in range(lines):
                pygame.time.wait(200)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN: 
                    if event.key == pygame.K_LEFT:
                        dx = -1
                    elif event.key == pygame.K_RIGHT:
                        dx = 1
                    elif event.key == pygame.K_DOWN:
                        anim_limit = 100
                    elif event.key == pygame.K_UP:
                        rotate = True
            
            
            #move x
            figure_old = deepcopy(figure)
            for i in range(4):
                figure[i].x += dx
                if not check_borders():
                    figure = deepcopy(figure_old)
                    break
            
            
            # move y 
            anim_count += anim_speed
            if anim_count > anim_limit:
                anim_count = 0
                figure_old = deepcopy(figure)
                for i in range(4):
                    figure[i].y += 1
                    if not check_borders():
                        for i in range(4):
                            field[figure_old[i].y][figure_old[i].x] = color
                        figure, color = next_figure, next_color
                        next_figure, next_color = deepcopy(choice(figures)), get_color()
                        anim_limit = 2000
                        break


            # rotate
            center = figure[0]
            figure_old = deepcopy(figure)
            if rotate:
                for i in range(4):
                    x = figure[i].y - center.y
                    y = figure[i].x - center.x
                    figure[i].x = center.x - x
                    figure[i].y = center.y + y
                    if not check_borders():
                        figure = deepcopy(figure_old)
                        break
            

            # check lines
            line, lines = HEIGHT - 1, 0
            for row in range(HEIGHT - 1, -1, -1):
                count = 0
                for i in range(WIDTH):
                    if field[row][i]:
                        count += 1
                    field[line][i] = field[row][i]
                if count < WIDTH:
                    line -= 1
                else:
                    anim_speed += 3
                    lines += 1

            # compute score
            score += scores[lines]
            last_score = score


            # draw grid
            [pygame.draw.rect(game_sc, (40, 40, 40), i_rect, 1) for i_rect in grid]
            
            
            #draw figure
            for i in range(4):
                figure_rect.x = figure[i].x * TILE
                figure_rect.y = figure[i].y * TILE
                pygame.draw.rect(game_sc, color, figure_rect)
            

            # draw next figure
            for i in range(4):
                figure_rect.x = next_figure[i].x * TILE + 380
                figure_rect.y = next_figure[i].y * TILE + 185
                pygame.draw.rect(sc, next_color, figure_rect)

            
            # draw field
            for y, raw in enumerate(field):
                for x, col in enumerate(raw):
                    if col:
                        figure_rect.x, figure_rect.y = x * TILE, y * TILE
                        pygame.draw.rect(game_sc, col, figure_rect)


            # draw titles
            sc.blit(title_tetris, (430, -10))
            sc.blit(title_score, (500, 600))
            sc.blit(font.render(str(score), True, pygame.Color('white')), (500, 650))
            sc.blit(title_record, (500, 450))
            sc.blit(font.render(record, True, pygame.Color('gold')), (500, 500))
            
            #game over
            for i in range(WIDTH):
                if field[0][i]:
                    set_record(record, score)
                    sound.stop()
                    sound_game_over.play()
                    play = False
                    field = [[0 for i in range(WIDTH)] for i in range(HEIGHT)]
                    anim_count, anim_speed, anim_limit = 0, 60, 2000
                    score = 0
                    for i_rect in grid:
                        pygame.draw.rect(game_sc, get_color(), i_rect)
                        sc.blit(game_sc, (20, 20))
                        pygame.display.flip()
                        clock.tick(200)
            pygame.display.update()
            pygame.display.flip()
            clock.tick(fps)

        pygame.display.update()



    

