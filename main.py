# necessery imports
import pygame
import random
import threading
import time
import tkinter

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

# function to check for collision between the bird and the pipes
def check_collision():
    global running, bird_x, bird_y, pipe_x, pipe_y, bird_y_change, colision
    while running:
        time.sleep(0.01)
        for i in range(3):
            if bird_x+bird.get_width() > pipe_x[i] and bird_x < pipe_x[i]+pipe.get_width():
            #print("Bird is in the same x position as the pipe"+ str(i))
            #print(bird_y, pipe_y[i])
                if bird_y > pipe_y[i]:
                    colision = True
                    #game_over_text = game_over_font.render("Game Over", True, (0, 0, 0))
                    #screen.blit(game_over_text, (300, 250))
                    # stopping everything
                    bird_y_change = 0               
                    # waiting for the player to decide what to do next
                    #checking = True
                    #while checking:
                     #   print("checking")
                      #  for event in pygame.event.get():
                       #     if event.type == pygame.QUIT:
                        #        running = False
                         #
                         #       colision = False
                         #   if event.type == pygame.KEYDOWN:
                          #      if event.key == pygame.K_r:
                           #         print("Game Reseting!")
                            #        reset()
                             #       print("Game Reseted!")
                              #      colision = False
                               #     checking = False
                        #pygame.display.update()
        # checking for collision between the bird and the reversed pipes
        #pipe_x[i], pipe_y[i]-pipe.get_height()-200
        for i in range(3):
            if bird_x+bird.get_width() > pipe_x[i] and bird_x < pipe_x[i]+pipe.get_width():
                #print(pipe_y[i]+pipe.get_height()-200, bird_y)
                if bird_y+5 < pipe_y[i]-200:
                    #print(bird_y, pipe_y[i]-200)
                    colision = True
                    bird_y_change = 0

# function to open the settings window
def settings_window():
    # window setup
    window = tkinter.Tk()
    window.title("Settings")
    window.geometry("800x600")
    window.mainloop()

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
background = pygame.image.load("assets/background.jpg")
# transforming the background to fit the screen
background = pygame.transform.scale(background, (800, 600))
# setting up the bird
bird = pygame.image.load("assets/new_bird.png")
bird_x = 50
bird_y = 300
bird_y_change = 0
# setting up the pipe
pipe = pygame.image.load("assets/new_pipe.png")
pipe_x = []
for i in range(3):
    pipe_x.append(800 + i * 400)
pipe_y = []
for i in range(3):
    pipe_y.append(random.choice(all_pipes_height))
# setting up the score
score = 0
font = pygame.font.Font("freesansbold.ttf", 32)
text_x = 10
text_y = 10
# setting up the game over
game_over_font = pygame.font.Font("freesansbold.ttf", 64)
colision = False

# settings window setup
settings = False
#settings_button = pygame.image.load("assets/settings_button.png")

# setting up a thread to check for collision between the bird and the pipes
coll_thread = threading.Thread(target=check_collision)
coll_thread.start()

# main loop
while running:
    # checking for collisions
    while colision:
        pygame.display.update()
        time.sleep(0.1)
        #print("colision")
        game_over_text = game_over_font.render("Game Over", True, (0, 0, 0))
        score_text = font.render("Score: " + str(score), True, (0, 0, 0))
        title_text = title_font.render("Flappy Bird", True, (0, 0, 0))
        screen.blit(game_over_text, (300, 250))
        screen.blit(score_text, (500, 10))
        screen.blit(title_text, (text_x, text_y))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                colision = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset()
                    colision = False
        pygame.display.update()

    # setting up the background
    screen.blit(background, (0, 0))

    # event checking
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            # destroying the settings window if it is open
            #if settings:
                #   window.destroy()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset()
                pass
            else:
                bird_y_change = -1
        if event.type == pygame.KEYUP:
            bird_y_change = 1
        # checking for the settings button
        if event.type == pygame.MOUSEBUTTONDOWN:
            #if event.pos[0] >= 750-settings_button.get_width() and event.pos[0] <= 750 and event.pos[1] >= 0 and event.pos[1] <= settings_button.get_height():
             #   print("Settings Button Clicked!")
              #  settings = True
                #settings_window()
            pass

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
    # placing the pipes and the reversed  pipes
    for i in range(3):
        screen.blit(pipe, (pipe_x[i], pipe_y[i]))
        screen.blit(pipe, (pipe_x[i], pipe_y[i]-pipe.get_height()-200))
    # pipe boundary checking
    for i in range(3):
        if pipe_x[i] <= -500:
            pipe_x[i] = 800
            pipe_y[i] = random.choice(all_pipes_height)
            score += 1

    # placing the score
    score_text = font.render("Score: " + str(score), True, (0, 0, 0))
    screen.blit(score_text, (500, 10))

    # placing the title of the game
    title_font = pygame.font.Font("freesansbold.ttf", 64)
    title_text = title_font.render("Flappy Bird", True, (0, 0, 0))
    screen.blit(title_text, (text_x, text_y))

    # placing a button in the top right corner to open the settings window
    #screen.blit(settings_button, (750-settings_button.get_width(), 0))
                
    pygame.display.update()

# quitting the game
pygame.quit()
