# necessery imports
import pygame
import random


# function to reset the game
def reset():
    global bird_y, bird_y_change, pipe_x, pipe_y, score
    bird_y = 300
    bird_y_change = 0
    for i in range(3):
        pipe_x[i] = 800 + i * 400
    for i in range(3):
        pipe_y[i] = random.choice(all_pipes_height)
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
pipe_x = []
for i in range(3):
    pipe_x.append(800 + i * 400)
pipe_y = []
for i in range(3):
    pipe_y.append(random.choice(all_pipes_height))
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
    for i in range(3):
        pipe_x[i] += -1
    # placing the pipe if there is less than 3 pipes on the screen
    if len(pipes_on_screen) < 1:
        pipes_on_screen.append([pipe_x, pipe_y])
    # placing the pipes
    for i in range(3):
        screen.blit(pipe, (pipe_x[i], pipe_y[i]))
    # pipe boundary checking
    for i in range(3):
        if pipe_x[i] <= -500:
            pipe_x[i] = 800
            pipe_y[i] = random.choice(all_pipes_height)
            score += 1

    # checking for collision between the bird and the pipes, temporary solution...
    for i in range(3):
        #print(bird_y, pipe_y[i])
        if pipe_y[i] < bird_y:
            #print("Bird is bellow the pipe")
            if bird_x-50 > pipe_x[i]:
                game_over_text = game_over_font.render("Game Over", True, (0, 0, 0))
                screen.blit(game_over_text, (300, 250))
                checking = True
                # setting the speeds to 0
                bird_y_change = 0
                pipe_y_change = 0

                # waiting for what player wants to do
                while checking:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                            checking = False
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_r:
                                reset()
                                checking = False
                    pygame.display.update()
            pygame.display.update()
        pygame.display.update()

pygame.quit()
