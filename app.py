import pygame
import time
import random
pygame.init()
white=(255,255,255)
black=(0,0,0)
red=(255,0,0)
green=(0,155,0)
screenWidth=800
screenHeight=600
gameDisplay=pygame.display.set_mode((screenWidth,screenHeight))

img=pygame.image.load('./imgs/snakehead.png')
imapple=pygame.image.load('./imgs/apple.png')
icon=pygame.image.load('./imgs/snake.png')

pygame.display.set_caption('Slither')
pygame.display.set_icon(icon)

clock=pygame.time.Clock()

smallfont=pygame.font.SysFont('comicsansms',25)
midfont=pygame.font.SysFont('comicsansms',35)
largefont=pygame.font.SysFont('comicsansms',45)

def text_object(msg,color,size):
    if size=='small':
        textSurface=smallfont.render(msg,True,color)
    elif size=='mid':
        textSurface=midfont.render(msg,True,color)
    elif size=='large':
        textSurface=largefont.render(msg,True,color)
    return textSurface,textSurface.get_rect()

def displaymsg(msg,color,ydisplace=0,size='small'):
    surftext,textRect=text_object(msg,color,size)
    textRect.center=(screenWidth/2),(screenHeight/2)+ydisplace
    gameDisplay.blit(surftext,textRect)

def intro():
    while True:
        gameDisplay.fill(white)
        displaymsg("Welcome to Slither",green,ydisplace=-40,size='large')
        displaymsg("press 'p' to play or press 'q' to quit",black,ydisplace=6,size='small')
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_p:
                    gameloop()
                elif event.key==pygame.K_q:
                    pygame.quit()
                    quit()
        pygame.display.update()
        clock.tick(15)
    
def snake(block_size,snakelist):
    if direction=='right':
        head=pygame.transform.rotate(img,270)
    elif direction=='left':
        head=pygame.transform.rotate(img,90)
    elif direction=='up':
        head=img
    else:
        head=pygame.transform.rotate(img,180)
    gameDisplay.blit(head,(snakelist[-1][0],snakelist[-1][1]))
    for xny in snakelist[:-1]:
        pygame.draw.rect(gameDisplay,green,[xny[0],xny[1],block_size,block_size])
        
def apple():
    applex=round(random.randrange(0,screenWidth-block_size)/10.0)*10.0
    appley=round(random.randrange(0,screenHeight-block_size)/10.0)*10.0
    return applex,appley

def printscore(score):
    text=smallfont.render("Score: "+str(score),True,black)
    gameDisplay.blit(text,[0,0])
    
def pause():
    paused=True
    while paused:
        displaymsg("Paused",black,ydisplace=-40,size='large')
        displaymsg("press Q to quit and c to Continue",black,20,'small')
        pygame.display.update()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_q:
                    pygame.quit()
                    quit()
                if event.key==pygame.K_c:
                    paused=False
    
def gameloop():
    global direction,fps,score,block_size
    fps=10
    score=0
    direction="right"
    applelen=1
    gameExit=False
    gameOver=False
    block_size=10
    lead_x=screenWidth/2
    lead_y=screenHeight/2
    lead_x_change=10
    lead_y_change=0
    snakelist=[]
    applex,appley=apple()
    while not gameExit:
        displaymsg(msg=str(score),color=black,ydisplace=-290)
        while gameOver==True:
            gameDisplay.fill(white)
            displaymsg("Game Over!",red,size='large')
            displaymsg("press 'q' to QUIT or 'c' to play again.",black,50,size='mid')
            pygame.display.update()
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    gameOver=False
                    gameExit=True
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_c:
                        gameloop()
                    if event.key==pygame.K_q:
                        gameExit=True
                        gameOver=False
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                gameExit=True
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_LEFT:
                    direction="left"
                    lead_x_change=-block_size
                    lead_y_change=0
                elif event.key==pygame.K_RIGHT:
                    direction="right"
                    lead_x_change=block_size
                    lead_y_change=0
                elif event.key==pygame.K_UP:
                    direction="up"
                    lead_y_change=-block_size
                    lead_x_change=0
                elif event.key==pygame.K_DOWN:
                    direction="down"
                    lead_y_change=block_size
                    lead_x_change=0
                elif event.key==pygame.K_p:
                    pause()
        if lead_x>800 or lead_x<0 or lead_y>600 or lead_y<0:
            gameOver=True
        lead_x+=lead_x_change
        lead_y+=lead_y_change
        gameDisplay.fill(white)
        if applelen%5==0:
            pygame.draw.rect(gameDisplay,red,(applex,appley,30,30))
        else:
            gameDisplay.blit(imapple,(applex,appley))
        snakehead=[]
        snakehead.append(lead_x)
        snakehead.append(lead_y)
        snakelist.append(snakehead)
        snake(block_size,snakelist)
        pygame.display.update()
        if len(snakelist)>applelen:
            del snakelist[0]
        for eachSegment in snakelist[:-1]:
            if snakehead==eachSegment:
                gameOver=True
        snake(block_size,snakelist)
        printscore(score)
        pygame.display.update()
        if applelen%5==0:
            if lead_x>=applex and lead_x<=applex+20 and lead_y>=appley and lead_y<=appley+20:
                applex,appley=apple()
                applelen+=1
                fps+=5
                score+=5
        elif lead_x>=applex and lead_x<=applex+15 and lead_y>=appley and lead_y<=appley+15:
            applex,appley=apple()
            applelen+=1
            score+=1
        clock.tick(fps)
    pygame.quit()
    quit()

intro()