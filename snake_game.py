import pygame
import random
import os
#Starting the pygame module
pygame.init()
pygame.mixer.init()

#In order to set a game window, do below, set_mode() takes a tuple (width,height)
screen_width =  900
screen_height = 600
game_window = pygame.display.set_mode((screen_width, screen_height))

#Add game title
game_title = pygame.display.set_caption("Play Snakes with Sayan")

back_img = pygame.image.load("background.jpg")
back_img = pygame.transform.scale(back_img,(screen_width,screen_height)).convert_alpha()

welcome_img = pygame.image.load("welcome.jpg")
welcome_img = pygame.transform.scale(welcome_img,(screen_width,screen_height)).convert_alpha()

over_img = pygame.image.load("game_over.jpg")
over_img = pygame.transform.scale(over_img,(screen_width,screen_height)).convert_alpha()

#Below are the colours to be used in RGB format
white = (255,255,255)
black = (0,0,0)
red = (255, 0, 0)

font = pygame.font.SysFont('Harrington', 35)
fps = 30

clock = pygame.time.Clock()

def print_screen(text, color, x, y):
    text_screen = font.render(text, True, color)
    game_window.blit(text_screen, (x,y))

def welcome_screen():
    pygame.mixer.music.load("intro_outro.mp3")
    pygame.mixer.music.play()
    exit_game = False
    while not exit_game:
        game_window.fill(white)
        game_window.blit(welcome_img,(0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_loop()
        pygame.display.update()
        clock.tick(fps)


def game_over_validate(snake_x, snake_y, snake_list):
    if ([snake_x, snake_y] in snake_list[0:-1]) or (snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height):
        return True
    return False

def draw_snake(snake_list, color, snake_size):
    for x,y in snake_list:
        pygame.draw.rect(game_window, black, [x, y, snake_size, snake_size])

def game_loop():
    # Game variables
    exit_game = False
    game_over = False
    snake_x = 50
    snake_y = 50
    snake_size = 20
    vel_x = 0
    vel_y = 0
    food_x = random.randint(10, screen_width / 2)
    food_y = random.randint(10, screen_height / 2)
    food_size = 20
    score = 0
    last_key = 0
    snake_list = []
    snake_len = 1
    snake_list.append([snake_x, snake_y])
    pygame.mixer.music.load("back.mp3")
    pygame.mixer.music.play()
    #check if file exists
    if (not os.path.exists("high_score.txt")):
        with open("high_score.txt", "w") as f:
            f.write("0")
    with open("high_score.txt") as f:
        high_score = f.read()
    while not exit_game:
        if game_over:
            with open("high_score.txt", "w") as f:
                f.write(str(high_score))
            game_window.fill(white)
            game_window.blit(over_img,(0,0))
            # pygame.mixer.music.load("intro_outro.mp3")
            # pygame.mixer.music.play()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.mixer.music.load("intro_outro.mp3")
                    pygame.mixer.music.play()
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        game_loop()
                        exit_game = True
        else:
            #Whatever events we do, pygame.event.get() takes that event as an i/p and "event" is that event
            #It will enter the below for loop only if we give any event
            for event in pygame.event.get():
                #Handle all events here, anything you do i.e move mouse up, down, press any key from keyboard etc.. it is an event
                #if event type is pygame.Quit, this means screen will go off on clicking close button
                if event.type == pygame.QUIT:
                    exit_game = True
                #if event type is pygame.keydown, this means I have pressed any key, event type pygame.keyup means I have released any key
                #Whenever you press any key, 1st event is KEYDOWN and then when we release that key, immediately next event is KEYUP
                if event.type == pygame.KEYDOWN:
                    #co-ordinate (0,0) start from top left of the screen
                    #So, right means increase x, left means decrease x, up menas decrease y and down means increase y
                    if event.key == pygame.K_LEFT and last_key != pygame.K_RIGHT:
                        vel_x = -5
                        vel_y = 0
                        last_key = event.key
                    elif event.key == pygame.K_RIGHT and last_key != pygame.K_LEFT:
                        vel_x = 5
                        vel_y = 0
                        last_key = event.key
                    if event.key == pygame.K_DOWN and last_key != pygame.K_UP:
                        vel_y = 5
                        vel_x = 0
                        last_key = event.key
                    if event.key == pygame.K_UP and last_key != pygame.K_DOWN:
                        vel_y = -5
                        vel_x = 0
                        last_key = event.key
                    if event.key == pygame.K_r:
                        score = score + 5

            # We want that if we press right key once, it will continue to move to right until we press another key
            #So, update the snake pos below, which will be executed when we are not doing anything
            snake_x = snake_x + vel_x
            snake_y = snake_y + vel_y

            #It will be out of the above for loop when no event is happening
            # Fill the game window with white colour
            game_window.fill(white)
            game_window.blit(back_img,(0,0))
            if abs(snake_x - food_x) < 8 and abs(snake_y - food_y) < 8:
                score = score + 10
                if score > int(high_score):
                    high_score = score
                snake_len = snake_len + 5
                food_x = random.randint(10, screen_width/2)
                food_y = random.randint(10, screen_height/2)

            snake_list.append([snake_x, snake_y])
            if len(snake_list) > snake_len:
                del snake_list[0]
            #Draw a rectangle which will be the head of the snake
            draw_snake(snake_list,black,snake_size)

            #Draw the food
            pygame.draw.rect(game_window, red, [food_x, food_y, food_size, food_size])

            print_screen(f"Score: {score}", black, 10, 10)
            print_screen(f"High Score: {high_score}", black, 600, 10)

            if game_over_validate(snake_x,snake_y,snake_list):
                pygame.mixer.music.load("game_over.mp3")
                pygame.mixer.music.play()
                game_over = True

        #After changing everything in display, do display.update()
        pygame.display.update()
        clock.tick(fps)

welcome_screen()
pygame.quit()



