import pygame
import random
import webbrowser

pygame.init()

# Colors
White = (255, 255, 255)
Black = (0, 0, 0)
Red = (255, 0, 0)
Red_Stage_1 = (100, 70, 10)
Red_Stage_2 = (150, 100, 0)
Red_Stage_3 = (200, 60, 70)
Green = (0, 255, 0)
Blue = (0, 0, 255)
BG = (255, 255, 200)
boundary_color = (50, 60, 150)
boundary_width = 3

# Icon
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

# Screen
screen_width = 1280
screen_height = 720
Surface = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

# Caption
pygame.display.set_caption('Catch that Mice')

pygame.display.update()
clock = pygame.time.Clock()

# Game Variable
Exit = False
fps = 60
score = 0
game_over = False
high_score = 0

with open('highscore.txt') as f:
    high_score = int(f.read())

# Snake Variable
snake_x = 50
snake_y = 695
snake_w_h = 20
snake_mov_x = 0
snake_mov_y = 0
snake_color = Red_Stage_1

# Mice
mice = pygame.image.load('mice.png')

# Retry Image
retry = pygame.image.load('retry.png')

# Snake
snake = pygame.image.load('snake.png')

# Start Image
start_image = pygame.image.load('start.png')

# Eat sound
eat = pygame.mixer.Sound('eat.wav')

# Boundaries
x_left_boundary = 0
x_right_boundary = 1280
y_top_boundary = 40
y_down_boundary = 720


def retry_function():
    global score, high_score
    score = 0

    with open('highscore.txt') as f:
        high_score = int(f.read())

    global  snake_w_h, snake_color, snake_mov_y, snake_mov_x, snake_y, snake_x
    snake_x = 50
    snake_y = 695
    snake_w_h = 20
    snake_mov_x = 0
    snake_mov_y = 0
    snake_color = Red_Stage_1


def valid_move():
    global x_left_boundary, x_right_boundary, y_top_boundary, y_down_boundary
    if (snake_x > x_left_boundary) and (snake_x < x_right_boundary) and (snake_y > y_top_boundary) and (snake_y < y_down_boundary):
        return True
    return False


# Level font
level_text = pygame.font.SysFont(None,50,True,False)


def display_level():
    global score
    # Stage1
    if score < 50:
        text = level_text.render('Level 1', True, Green, None)
        Surface.blit(text, (20, 20))
    # Stage 2
    elif score < 100:
        text = level_text.render('Level 2', True, Blue, None)
        Surface.blit(text, (20, 20))
    # Stage 3
    elif score < 200:
        text = level_text.render('Level 3', True, Red, None)
        Surface.blit(text, (20, 20))
    # Max stage
    else:
        text = level_text.render('Max Level', True, Black, None)
        Surface.blit(text, (20, 20))


def speed():
    global snake_color, Red_Stage_2, Red_Stage_3, Red, level_text, boundary_color
    # Stage1
    if score < 50:
        return 4 # Snake speed
    # Stage 2
    elif score < 100:
        snake_color = Red_Stage_2
        boundary_color = (140, 200, 85)
        return 7 # Snake speed
    # Stage 3
    elif score < 200:
        snake_color = Red_Stage_3
        boundary_color = (255, 90, 160)
        return 9 # Snake speed
    # Max stage
    else:
        snake_color = Red
        boundary_color = (175, 200, 100)
        return 12 # Max speed


def move(direction):
    if valid_move():
        global snake_mov_x
        global snake_mov_y
        if direction == 'right':
            snake_mov_x = speed()
            snake_mov_y = 0
        elif direction == 'left':
            snake_mov_x = - speed()
            snake_mov_y = 0
        elif direction == 'up':
            snake_mov_y = - speed()
            snake_mov_x = 0
        elif direction == 'down':
            snake_mov_y = speed()
            snake_mov_x = 0
    else:
        global game_over
        game_over = True
        display_game_over()


# Mice initial pos
mice_x = 455
mice_y = 455


def move_mice():
    global mice_x, mice_y
    mice_x = random.randint(100,1200)
    mice_y = random.randint(100,650)


def snake_eat():
    global score
    if abs(mice_x - snake_x) <= 45 and abs(mice_y - snake_y) <= 45:
        score += 5
        pygame.mixer.Sound.play(eat)
        return True
    else :
        return False


score_text = pygame.font.SysFont(None,50,True,False)


def display_score():
    text = score_text.render('SCORE IS : '+str(score),True,Green,None)
    Surface.blit(text,(900,20))


def display_game_over():
    global Surface, high_score
    Surface.fill(BG)
    game_over_text = pygame.font.SysFont(None,80,True,True)
    Surface.blit(retry, (600, 550))
    if high_score > score:
        high_score_display = pygame.font.SysFont(None, 80, True, True)
        high_score_display_object = high_score_display.render('HIGH SCORE IS :: '+str(high_score),True,Black,None)
        Surface.blit(high_score_display_object,(80,250))
    else :
        with open('highscore.txt','w') as f:
            f.write(str(score))
            high_score_display = pygame.font.SysFont(None, 80, True, True)
            high_score_display_object = high_score_display.render('Congrats! YOU MADE HIGH SCORE', True, Black, None)
            Surface.blit(high_score_display_object, (80, 250))
    text = game_over_text.render('GAME OVER FINAL SCORE IS :: '+str(score),True,Black,None)
    pause = True
    while pause:
        mouse = pygame.mouse.get_pos()
        X = int(mouse[0])
        Y = int(mouse[1])
        if (X > 600) and (X < 650) and (Y > 550) and (Y < 600):
            button = pygame.mouse.get_pressed()
            if button[0] == True:
                retry_function()
                break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pause = False
            Surface.blit(text,(80,350))
            pygame.display.update()


def start_function():
    Surface.blit(start_image, (0, 0))
    pygame.display.update()
    not_play = True
    while not_play:
        x, y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if (x > 475) and (x < 830) and (y > 530) and (y < 655):
                l, r, m = pygame.mouse.get_pressed()
                if l == True:
                    game_loop()
            if (x > 1130) and (x < 1250) and (y > 575) and (y < 700):
                l, r, m = pygame.mouse.get_pressed()
                if l == True:
                    webbrowser.open('https://www.linkedin.com/in/ashutoshkmrsingh/')
                    pygame.quit()
                    quit()


# Game Loop
def game_loop():
    global Exit,game_over, snake_x, snake_y, snake_mov_x, snake_mov_y, snake_color, snake_w_h
    global Surface, White,boundary_color, boundary_width, x_left_boundary, x_right_boundary, y_top_boundary, y_down_boundary
    global mice, mice_x, mice_y, snake, clock
    while not Exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Exit = True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    move('right')
                elif event.key == pygame.K_LEFT:
                    move('left')
                elif event.key == pygame.K_UP:
                    move('up')
                elif event.key == pygame.K_DOWN:
                    move('down')

            elif game_over == True:
                #Exit = True
                pass

        snake_x += snake_mov_x
        snake_y += snake_mov_y

        Surface.fill(White)
        pygame.draw.rect(Surface, snake_color, [snake_x, snake_y, snake_w_h, snake_w_h])
        pygame.draw.rect(Surface, boundary_color, [x_left_boundary, y_top_boundary + 15, x_right_boundary, y_down_boundary], boundary_width)
        if snake_eat():
            move_mice()
        Surface.blit(mice, (mice_x, mice_y))
        display_score()
        display_level()
        Surface.blit(snake,(850,0))
        pygame.display.update()
        clock.tick(fps)


start_function()
pygame.quit()
quit()
