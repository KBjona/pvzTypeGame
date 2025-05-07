import pygame
import time
import network.client as client

global screenColor, Width, Height, Time, tilewidth, tileheight
global screen, clock, tiles, bg

Width = 800
Height = 600
Time = 60
tilewidth = 8
tileheight = 5
screenColor = (26, 138, 35)

def setup():
    global screenColor, Width, Height, Time, tilewidth, tileheight
    global screen, clock, tiles, bg
    pygame.init()
    screen = pygame.display.set_mode((Width, Height))
    pygame.display.set_caption("presidents vs nazis")
    clock = pygame.time.Clock()
    tiles = [[0 for _ in range(tilewidth)] for _ in range(tileheight)]
    bg = pygame.image.load("images/peashooter.png").convert_alpha()
    print("BOOO")
    bg = pygame.transform.scale(bg, (70, 70))


def update():
    pygame.display.update()
    clock.tick(Time)
    time.sleep(0.05)


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
    for x in range(tilewidth):
        for y in range(tileheight):
            sqr = pygame.Rect(x * 95 + 10, y * 95 + 70, 70, 70)
            if tiles[y][x] == 0:
                pygame.draw.rect(screen, (36, 200, 100), sqr)
            elif tiles[y][x] == 1:
                screen.blit(bg, (x * 95 + 10, y * 95 + 70))
            if pygame.mouse.get_pressed()[0]:
                if sqr.collidepoint(pygame.mouse.get_pos()):
                    tiles[y][x] = 1
                    print(y, x)

def main():
    setup()
    running = True
    while running:
        screen.fill(screenColor)
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