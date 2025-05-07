import pygame
import time
import network.client as client

global screenColor, Width, Height, Time, tilewidth, tileheight
global screen, clock, tiles, bg
global peashooter
global money

money = 0 
Width = 800
Height = 600
Time = 60
tilewidth = 9
tileheight = 5
screenColor = (26, 138, 35)

def setup():
    global screenColor, Width, Height, Time, tilewidth, tileheight
    global screen, clock, tiles, peashooter, bg
    global money

    pygame.init()

    screen = pygame.display.set_mode((Width, Height))

    pygame.display.set_caption("presidents vs nazis")

    clock = pygame.time.Clock()

    tiles = [[0 for _ in range(tilewidth)] for _ in range(tileheight)]

    peashooter = pygame.image.load("images/peashooter.png").convert_alpha()
    peashooter = pygame.transform.scale(peashooter, (60, 60))

    bg = pygame.image.load("images/currentBGimage.png").convert_alpha()
    bg = pygame.transform.scale(bg, (Width, Height))

def update():
    global money
    pygame.display.update()
    clock.tick(Time)
    money += 5
    time.sleep(0.05)
    print(money)


class Defender:
    def __init__(self, type, x, y, damage, health, image):
        self.type = type
        self.x = x
        self.y = y
        self.damage = damage
        self.health = health
        self.image = image
    def damaged(self, damage):
        self.health -= damage
        if self.health <= 0:
            pass # should be death 






def draw_grid():
    global money
    for x in range(tilewidth):
        for y in range(tileheight):
            sqr = pygame.Rect(x * 80 + + 60 , y * 80 + 100, 60, 60)
            if tiles[y][x] == 0:
                pygame.draw.rect(screen, (36, 200, 100), sqr)
            elif tiles[y][x] == 1:
                screen.blit(peashooter, (x * 80 + 60, y * 80 + 100))
            if pygame.mouse.get_pressed()[0]:
                if sqr.collidepoint(pygame.mouse.get_pos()):
                    if money >= 100 and tiles[y][x] == 0:
                        money -= 100
                        tiles[y][x] = 1
                        print(y, x)
                        print("placed peashooter and -100 money")
def main():
    setup()
    running = True
    while running:
        #screen.fill(screenColor)
        screen.blit(bg, (0, 0))
        draw_grid()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                print("You clicked the X button")
        update()
    pygame.quit()

try:
    main()
except SystemExit:
    print("You closed the window")
except Exception as e:
    print("An error occurred:", e)