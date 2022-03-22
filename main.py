import pygame
import os


WIDTH , HEIGHT = 800 , 600
WINDOW = pygame.display.set_mode((WIDTH,HEIGHT))
FPS = 60


pygame.font.init()

font = pygame.font.SysFont('comicsans',20)
winnerFont = pygame.font.SysFont('comicsans' , 40)

pygame.mixer.init()

FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets','Gun+Silencer.mp3'))
HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets','Grenade+1.mp3'))

FIRE_SOUND.set_volume(0.1)
HIT_SOUND.set_volume(0.05)

pygame.display.set_caption("Space Game")

RED_HIT = pygame.USEREVENT + 1
YELLOW_HIT = pygame.USEREVENT + 2

SHIP_WIDTH = 60
SHIP_HEIGHT = 50

BULLET_WIDTH = 30
BULLET_HEIGHT = 35

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (127, 127, 127)
RED = (255, 0, 0)
LINE_COLOR = (110, 80, 242)

VELOCITY = 5
BULLET_VELOCITY = 6

MAX_BULLETS = 5



playerOneImage = pygame.image.load(os.path.join('Assets','spaceship_yellow.png'))
playerOne = pygame.transform.rotate(pygame.transform.scale(playerOneImage,(SHIP_WIDTH,SHIP_HEIGHT)),90)

playerTwoImage = pygame.image.load(os.path.join('Assets','spaceship_red.png'))
playerTwo = pygame.transform.rotate(pygame.transform.scale(playerTwoImage,(SHIP_WIDTH,SHIP_HEIGHT)),270)

spaceImage = pygame.image.load(os.path.join('Assets','space.png'))
space = pygame.transform.scale(spaceImage,(WIDTH,HEIGHT))

yellowBulletImage = pygame.image.load(os.path.join('Assets','yellow_ammo.png'))
yellowBullet = pygame.transform.rotate(pygame.transform.scale(yellowBulletImage,(BULLET_WIDTH,BULLET_HEIGHT)),180)

redBulletImage = pygame.image.load(os.path.join('Assets','red_ammo.png'))
redBullet = pygame.transform.scale(redBulletImage,(BULLET_WIDTH,BULLET_HEIGHT))

rectOne = pygame.Rect(30,HEIGHT/2-(SHIP_WIDTH/2),SHIP_WIDTH-5,SHIP_HEIGHT-15)
rectTwo = pygame.Rect(WIDTH-SHIP_WIDTH-20,HEIGHT/2-(SHIP_WIDTH/2),SHIP_WIDTH-5,SHIP_HEIGHT-5)





line = pygame.Rect(WIDTH/2-10,0,10,HEIGHT)
def drawWindow(redBullets,yellowBullets,playerOneHp,playerTwoHp):

    WINDOW.blit(space,(0,0))
    WINDOW.blit(playerOne,(rectOne.x,rectOne.y))
    WINDOW.blit(playerTwo,(rectTwo.x,rectTwo.y))
    WINDOW.blit(font.render("HP: " + str(playerOneHp) ,False,WHITE) , (20,20))
    WINDOW.blit(font.render("HP:" + str(playerTwoHp),False,WHITE),(WIDTH-20-50,20))
    for red in redBullets:
        WINDOW.blit(redBullet,(red.x,red.y))
    for yellow in yellowBullets:
        WINDOW.blit(yellowBullet,(yellow.x,yellow.y))

    pygame.draw.rect(WINDOW,LINE_COLOR,line)
    pygame.display.update()

def handleMovement():

    pressedKeys = pygame.key.get_pressed()

    #PLAYER ONE MOVEMENT

    if pressedKeys[pygame.K_a] and rectOne.x - VELOCITY > 0: #LEFT
        rectOne.x -= VELOCITY

    if pressedKeys[pygame.K_w] and rectOne.y - VELOCITY > 0: #UP
        rectOne.y -= VELOCITY

    if pressedKeys[pygame.K_d] and rectOne.x + VELOCITY + SHIP_WIDTH  < line.x + 10: #RIGHT
        rectOne.x += VELOCITY

    if pressedKeys[pygame.K_s] and rectOne.y + VELOCITY + SHIP_HEIGHT + 10 < HEIGHT: #DOWN
        rectOne.y += VELOCITY

    #PLAYER TWO MOVEMENT

    if pressedKeys[pygame.K_LEFT] and rectTwo.x - VELOCITY > line.x + 10 : #LEFT
        rectTwo.x -= VELOCITY

    if pressedKeys[pygame.K_UP] and rectTwo.y - VELOCITY > 0: #UP
        rectTwo.y -= VELOCITY

    if pressedKeys[pygame.K_RIGHT] and rectTwo.x + VELOCITY + SHIP_WIDTH < WIDTH : #RIGHT
        rectTwo.x += VELOCITY

    if pressedKeys[pygame.K_DOWN] and rectTwo.y + VELOCITY + SHIP_HEIGHT + 10< HEIGHT: #DOWN
        rectTwo.y += VELOCITY


def handleBullets(redBullets,yellowBullets):

    for red in redBullets:
        red.x -= BULLET_VELOCITY
        if red.colliderect(rectOne) or red.x - BULLET_VELOCITY < 0:
            redBullets.remove(red)
            if(red.x - BULLET_VELOCITY > 0):
                HIT_SOUND.play()
                pygame.event.post(pygame.event.Event(RED_HIT))

    for yellow in yellowBullets:
        yellow.x += BULLET_VELOCITY
        if yellow.colliderect(rectTwo) or yellow.x + BULLET_VELOCITY > WIDTH:
            yellowBullets.remove(yellow)
            if (yellow.x + BULLET_VELOCITY < WIDTH):
                HIT_SOUND.play()
                pygame.event.post(pygame.event.Event(YELLOW_HIT))


def drawWinner(text):
    print(text)
    renderText = winnerFont.render(text,True,WHITE)

    WINDOW.blit(renderText,(WIDTH/2-renderText.get_width()/2,HEIGHT/2 - renderText.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():

    redBullets = []
    yellowBullets = []

    playerOneHp = 10
    playerTwoHp = 10

    clock = pygame.time.Clock()

    flag = True
    while flag:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                flag = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RSHIFT and len(redBullets) < MAX_BULLETS:

                    redBulletRect = pygame.Rect(rectTwo.x , rectTwo.y + SHIP_HEIGHT / 2 - 11 ,BULLET_WIDTH, BULLET_HEIGHT)
                    FIRE_SOUND.play()
                    redBullets.append(redBulletRect)


                if event.key == pygame.K_LSHIFT and len(yellowBullets) < MAX_BULLETS:
                    yellowBulletRect = pygame.Rect(rectOne.x + SHIP_WIDTH - BULLET_WIDTH ,rectOne.y + SHIP_HEIGHT / 2 - 13, BULLET_WIDTH, BULLET_HEIGHT)
                    FIRE_SOUND.play()
                    yellowBullets.append(yellowBulletRect)
            if event.type == RED_HIT:
                playerOneHp -= 1


            if event.type == YELLOW_HIT:
                playerTwoHp -= 1


        handleMovement()
        handleBullets(redBullets,yellowBullets)
        drawWindow(redBullets,yellowBullets,playerOneHp,playerTwoHp)

        winnerText = ""

        if playerTwoHp < 1:
            winnerText = "Player One Won!!!"
        if playerOneHp < 1:
            winnerText = "Player Two Won!!!"

        if winnerText != "":
            drawWinner(winnerText)
            break

    main()

if __name__ == "__main__":
    main()