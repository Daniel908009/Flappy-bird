# necessery imports
import pygame
import random
import threading
import time
import tkinter
import os
import sys
if hasattr(sys, '_MEIPASS'):
    base_path = sys._MEIPASS
else:
    base_path = os.path.abspath(".")

# function to reset the game
def reset():
    global bird_y, bird_y_change, pipe_x, pipe_y, score, colision
    bird_y = 300
    bird_y_change = 0
    colision = False
    # clearing the pipes list
    pipe_x.clear()
    pipe_y.clear()
    # setting up the pipes list
    for i in range(numb_of_pipes):
        pipe_x.append(800 + i * 450) 
        pipe_y.append(random.choice(all_pipes_height))
    score = 0

# function to check for collision between the bird and the pipes
def check_collision():
    global running, bird_x, bird_y, pipe_x, pipe_y, bird_y_change, colision
    while running:
        while settings:
            pass
        time.sleep(0.01)
        for i in range(numb_of_pipes):
            if bird_x+bird.get_width() > pipe_x[i] and bird_x < pipe_x[i]+pipe.get_width():
                if bird_y+bird.get_height() > pipe_y[i]:
                    colision = True
                    bird_y_change = 0               
        for i in range(numb_of_pipes):
            if bird_x+bird.get_width() > pipe_x[i] and bird_x < pipe_x[i]+pipe.get_width():
                if bird_y+5 < pipe_y[i]-200:
                    colision = True
                    bird_y_change = 0

# function to apply the settings
def apply(pipes, window, speed):
    global numb_of_pipes, settings, bird_speed
    # checking if the input is valid                # origanaly I wanted to verify the speed as well, but it is more fun if I don't
    if int(pipes) < 1 or int(pipes) > 3:            #or float(speed) < 1 or float(speed) > 2:
        return
    else:
        numb_of_pipes = int(pipes)
        bird_speed = float(speed)
    settings = False
    window.destroy()
    reset()

# function to open the settings window, could be enhanced with more settings, but for now it is enough
def settings_window():
    # window setup
    window = tkinter.Tk()
    window.title("Settings")
    window.geometry("750x200")
    window.resizable(False, False)
    window.iconbitmap(os.path.join(base_path, "assets/setting.ico"))
    # creating the main label
    label = tkinter.Label(window, text="Settings", font=("Arial", 32))
    label.pack()
    # creating a frame for the settings
    frame = tkinter.Frame(window)
    frame.pack()
    # creating a label for the number of pipes
    pipes_label = tkinter.Label(frame, text="Number of Pipes", font=("Arial", 16))
    pipes_label.grid(row=0, column=0)
    # creating a entry for the number of pipes
    e1 = tkinter.StringVar()
    e1.set(str(numb_of_pipes))
    pipes_entry = tkinter.Entry(frame, font=("Arial", 16), textvariable=e1)
    pipes_entry.grid(row=0, column=1)
    # creating a label for instructions
    instructions_label = tkinter.Label(frame, text="Enter a number between 1 and 3", font=("Arial", 16))
    instructions_label.grid(row=0, column=2)
    # creating a label for the speed of the bird
    speed_label = tkinter.Label(frame, text="Speed of the Bird", font=("Arial", 16))
    speed_label.grid(row=1, column=0)
    # creating a entry for the speed of the bird
    e2 = tkinter.StringVar()
    e2.set(str(bird_speed))
    speed_entry = tkinter.Entry(frame, font=("Arial", 16), textvariable=e2)
    speed_entry.grid(row=1, column=1)
    # creating a label for instructions
    instructions_label2 = tkinter.Label(frame, text="Recomended speed is between 1-2", font=("Arial", 16))
    instructions_label2.grid(row=1, column=2)
    # creating the apply button
    apply_button = tkinter.Button(window, text="Apply", font=("Arial", 16), command=lambda: apply(pipes_entry.get(), window, speed_entry.get()))
    apply_button.pack(side="bottom")
    window.mainloop()

# function to move the pipes
def move_pipes():
    global running, pipe_x, pipe_y, numb_of_pipes, score
    while running:
        # if there is a collision or the settings window is open the pipes will not move
        while colision:
            pass
        time.sleep(0.005)
        while settings:
            pass

        for i in range(numb_of_pipes):
            pipe_x[i] += -1
        for i in range(numb_of_pipes):
            # if the pipe reaches the end it will reappear at the start with a new height
            if pipe_x[i] <= -550:
                pipe_x[i] = 800
                pipe_y[i] = random.choice(all_pipes_height)
                score += 1


# variables
running = True
# this list will be used to store all the pipes on the screen
pipes_on_screen = []

# list of all the possible heights for the pipes
all_pipes_height = [150, 200, 250, 300, 350, 400, 450, 500]

# initialize pygame
pygame.init()
# creating and setting up the screen
screen = pygame.display.set_mode((800, 600))
# setting up the title and icon
pygame.display.set_caption(os.path.join(base_path,"Flappy Bird"))
icon = pygame.image.load(os.path.join(base_path, "assets/icon.png"))
pygame.display.set_icon(icon)
# setting up the background
background = pygame.image.load(os.path.join(base_path, "assets/background.jpg"))
# transforming the background to fit the screen
background = pygame.transform.scale(background, (800, 600))
# setting up the bird
bird = pygame.image.load(os.path.join(base_path, "assets/new_bird.png"))
bird_x = 50
bird_y = 300
bird_y_change = 0
bird_speed = 1.5
# setting up the pipes
pipe = pygame.image.load(os.path.join(base_path, "assets/new_pipe.png"))
pipe_x = []
pipe_y = []
numb_of_pipes = 3
for i in range(numb_of_pipes):
    pipe_x.append(800 + i * 450)
    pipe_y.append(random.choice(all_pipes_height))
# setting up the score
score = 0
font = pygame.font.Font("freesansbold.ttf", 32)
text_x = 10
text_y = 10
# setting up the game over text
game_over_font = pygame.font.Font("freesansbold.ttf", 64)

# variable used to check if a collision happened
colision = False

# settings window setup
settings = False
settings_button = pygame.image.load(os.path.join(base_path, "assets/setting.png"))

# setting up a thread to check for collision between the bird and the pipes
coll_thread = threading.Thread(target=check_collision)
coll_thread.start()
# setting up a thread to move the pipes
move_thread = threading.Thread(target=move_pipes)
move_thread.start()

# main loop
while running:
    # if a collision is detected the game over screen will be displayed
    while colision:
        pygame.display.update()
        time.sleep(0.1)
        game_over_text = game_over_font.render("Game Over", True, (254, 21, 24))
        score_text = font.render("Score: " + str(score), True, (210, 1, 3))
        title_text = title_font.render("Flappy Bird", True, (0, 0, 0))
        screen.blit(game_over_text, (300, 250))
        screen.blit(score_text, (500, 10))
        screen.blit(title_text, (text_x, text_y))
        # event checking inside the game over screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                colision = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset()
                    colision = False
            # checking if the player has hit the settings button
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] >= 750-settings_button.get_width() and event.pos[0] <= 750 and event.pos[1] >= 0 and event.pos[1] <= settings_button.get_height():
                    settings = True
                    settings_window()
        pygame.display.update()

    # settings window check
    if settings:
        settings = False

    # setting up the background
    screen.blit(background, (0, 0))

    # event checking
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset()
            else:
                bird_y_change = bird_speed * -1
        if event.type == pygame.KEYUP:
            # this previously caused a bug where the bird would not stop moving after reseting the game
            if event.key == pygame.K_r:
                pass
            else:
                bird_y_change = bird_speed
        # checking for the settings button
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.pos[0] >= 800-settings_button.get_width() and event.pos[0] <= 800 and event.pos[1] >= 0 and event.pos[1] <= settings_button.get_height():
                settings = True
                settings_window()

    # placing the bird
    screen.blit(bird, (bird_x, bird_y))
    # bird movement, up and down
    bird_y += bird_y_change
    # bird boundary checking
    if bird_y <= 0:
        bird_y = 0
    # checking if the bird has hit the ground
    elif bird_y >= 500:
        colision = True

    # placing the pipes and the reversed  pipes
    for i in range(numb_of_pipes):
        screen.blit(pipe, (pipe_x[i], pipe_y[i]))
        screen.blit(pipe, (pipe_x[i], pipe_y[i]-pipe.get_height()-200))

    # placing the score
    score_text = font.render("Score: " + str(score), True, (210, 1, 3))
    screen.blit(score_text, (500, 10))

    # placing the title of the game
    title_font = pygame.font.Font("freesansbold.ttf", 64)
    title_text = title_font.render("Flappy Bird", True, (0, 0, 0))
    screen.blit(title_text, (text_x, text_y))

    # placing a button in the top right corner to open the settings window
    screen.blit(settings_button, (800-settings_button.get_width(), 0))

    # updating the screen            
    pygame.display.update()

# quitting the game
pygame.quit()