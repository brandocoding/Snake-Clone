import os
import pygame
import time
import random 

pygame.init()

os.environ["SDL_VIDEO_CENTERED"] = "1"

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,155,0)

display_width = 800
display_height = 600

clock = pygame.time.Clock()

FPS = 15
block_size = 20
AppleThickness = 30

direction = "right"

gameWindow = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Test Run')

icon = pygame.image.load('apple.png')
pygame.display.set_icon(icon)####BEST SIZE FOR ICON IS 32x32####

img = pygame.image.load('snakehead.png')
appleimg = pygame.image.load('apple.png')

smallfont = pygame.font.SysFont("comicsansms", 25)
medfont = pygame.font.SysFont("comicsansms", 50)
largefont = pygame.font.SysFont("comicsansms", 80)


def pause():

    paused = True

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        gameWindow.fill(white)
        message_to_screen("Paused", black, -100, size = "large")
        message_to_screen("Press C to continue or Q to quit", black, 25)
        pygame.display.update()
        clock.tick(5)
        
def score(score):
    text = smallfont.render("Score: "+str(score), True, black)
    gameWindow.blit(text, [0,0])


def randAppleGen():
    randAppleX = round(random.randrange(0, display_width-AppleThickness))#/10.0)*10.0
    randAppleY = round(random.randrange(0, display_height-AppleThickness))#/10.0)*10.0

    return randAppleX, randAppleY


def game_intro():

    intro = True

    while intro:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                    
        gameWindow.fill(white)
        message_to_screen("Snake Prototype", green, -100, "large")
        message_to_screen("The objective of the game is to eat red apples", black, -30)
        message_to_screen("The more apples you eat the longer you get", black, 10)
        message_to_screen("if you run into yourself or the edges you die", black, 50)
        message_to_screen("Press C to play, P to pause or Q to quit", black, 180)

        pygame.display.update()
        clock.tick(15)

def snake(block_size, snakeList):

    if direction == "right":
        head = pygame.transform.rotate(img, 270)
    if direction == "left":
        head = pygame.transform.rotate(img, 90)
    if direction == "up":
        head = img
    if direction == "down":
        head = pygame.transform.rotate(img, 180)
        
    gameWindow.blit(head, (snakeList[-1][0],snakeList[-1][1]))

    for XnY in snakeList[:-1]:
        pygame.draw.rect(gameWindow, green, [XnY[0],XnY[1],block_size,block_size])

def text_objects(text,color, size):
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    elif size == "medium":
        textSurface = medfont.render(text, True, color)
    elif size == "large":
        textSurface = largefont.render(text, True, color)
  
    return textSurface, textSurface.get_rect()
    
    
def message_to_screen(msg,color, y_displace=0, size = "small"):
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = (display_width / 2),(display_height / 2)+y_displace
    gameWindow.blit(textSurf, textRect)

def gameloop():
    global direction

    direction = "right"
    
    gameExit = False
    gameOver = False

    lead_x = display_width/2
    lead_y = display_height/2

    leadx_change = 10
    leady_change = 0

    snakeList = []
    snakeLength = 1

    randAppleX, randAppleY = randAppleGen()

    
    while not gameExit:

        while gameOver == True:
            gameWindow.fill(white)
            message_to_screen("Game Over", red, -50, size = "large")
            message_to_screen("Press C to play again or Q to quit", black, 50, size = "medium")
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameOver = False
                    gameExit = True
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_c:
                        gameloop()
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    direction = "left"
                    leadx_change = -block_size
                    leady_change = 0 
                if event.key == pygame.K_RIGHT:
                    direction = "right"
                    leadx_change = block_size
                    leady_change = 0
                if event.key == pygame.K_UP:
                    direction = "up"
                    leady_change = -block_size
                    leadx_change = 0
                if event.key == pygame.K_DOWN:
                    direction = "down"
                    leady_change = block_size
                    leadx_change = 0
                if event.key == pygame.K_p:
                    pause()

        if lead_x >= display_width or lead_x < 0 or lead_y >= display_height or lead_y < 0:
            gameOver = True

    
        lead_x += leadx_change
        lead_y += leady_change

        gameWindow.fill(white)

        
        #pygame.draw.rect(gameWindow, red, [randAppleX, randAppleY, AppleThickness, AppleThickness])

        gameWindow.blit(appleimg, (randAppleX, randAppleY))
        
        snakeHead = []
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)
        snakeList.append(snakeHead)

        if len(snakeList) > snakeLength:
            del snakeList[0]

        for eachSegment in snakeList[:-1]:
            if eachSegment == snakeHead:
                gameOver = True
                
            
        snake(block_size, snakeList)

        score(snakeLength-1)

        
        pygame.display.update()

                
        if lead_x > randAppleX and lead_x < randAppleX + AppleThickness or lead_x + block_size > randAppleX and lead_x + block_size < randAppleX + AppleThickness:
            
            if lead_y > randAppleY and lead_y < randAppleY + AppleThickness:
                randAppleX, randAppleY = randAppleGen()
                snakeLength += 1


            elif lead_y + block_size > randAppleY and lead_y + block_size < randAppleY + AppleThickness:
                randAppleX, randAppleY = randAppleGen()
                snakeLength += 1





        clock.tick(FPS)

    pygame.quit()
    quit()
    
game_intro()
gameloop()


