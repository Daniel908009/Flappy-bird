# necessery imports
import pygame
import random


# function to reset the game
def reset():
    global bird_y, bird_y_change, pipe_x, pipe_y, score
    bird_y = 300
    bird_y_change = 0
    pipe_x = 800
    pipe_y = random.choice(all_pipes_height)
    score = 0
    print("Game Reseted!")


# variables
running = True
# this list will be used in the future to store all the pipes on the screen
pipes_on_screen = []

all_pipes_height = [150, 200, 250, 300, 350, 400, 450, 500]

# initialize pygame
pygame.init()
# creating and setting up the screen
screen = pygame.display.set_mode((800, 600))
# setting up the title and icon
pygame.display.set_caption("Flappy Bird")
icon = pygame.image.load("assets/icon.png")
pygame.display.set_icon(icon)
# setting up the background
#background = pygame.image.load("assets/background.png")
# setting up the bird
bird = pygame.image.load("assets/bird.png")
bird_x = 50
bird_y = 300
bird_y_change = 0
# setting up the pipe
pipe = pygame.image.load("assets/pipe.png")
pipe_x = 800
pipe_y = random.choice(all_pipes_height)
pipe_y_change = 0
# setting up the ground
#ground = pygame.image.load("assets/ground.png")
ground_x = 0
ground_y = 500
ground_x_change = -1
# setting up the score
score = 0
font = pygame.font.Font("freesansbold.ttf", 32)
text_x = 10
text_y = 10
# setting up the game over
game_over_font = pygame.font.Font("freesansbold.ttf", 64)

# main loop
while running:
    # setting up the background
    screen.fill((255, 255, 255))

    # displaying the main title
    title = font.render("Flappy Bird", True, (0, 0, 0))
    screen.blit(title, (10, 10))

    # displaying the score on the center of the screen
    score_text = font.render("Score: " + str(score), True, (0, 0, 0))
    screen.blit(score_text, (350, 10))


    # event checking
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset()
                pass
            else:
                bird_y_change = -1
        if event.type == pygame.KEYUP:
            bird_y_change = 1

    # placing the bird
    screen.blit(bird, (bird_x, bird_y))
    # bird movement, up and down
    bird_y += bird_y_change
    # bird boundary checking
    if bird_y <= 0:
        bird_y = 0
    elif bird_y >= 500:
        bird_y = 500
    # moving the pipes closer to the bird
    pipe_x += -1
    # placing the pipe
    screen.blit(pipe, (pipe_x, pipe_y))
    # pipe boundary checking
    if pipe_x <= -500:
        score += 1
        pipe_x = 800
        pipe_y = random.choice(all_pipes_height)

    # checking for collision between the bird and the pipe, temporary solution...
    #if bird_x >= pipe_x and bird_x <= pipe_x+100 and bird_y >= pipe_y:
    if bird_x >= pipe_x and bird_y <= pipe_y:
        if bird_y <= pipe_y + 500 or bird_y + 64 >= pipe_y + 600:
            game_over_text = game_over_font.render("Game Over", True, (0, 0, 0))
            screen.blit(game_over_text, (300, 250))
            end_screen = True
            # stoping all moving objects
            bird_y_change = 0
            pipe_x = 0
            while end_screen:
                # event checking
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        end_screen = False
                        running = False
                    # checking for the reset key
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            end_screen = False
                            reset()                          
                pygame.display.update()
    print("main loop running...")
    pygame.display.update()

pygame.quit()