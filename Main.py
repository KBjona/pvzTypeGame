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

def setup_defenders():
    global peashooter
    peashooter_setup = Defender("peashooter", 0, 0, 10, 100,100, "images/peashooter.png")
    

def setup():
    global screenColor, Width, Height, Time, tilewidth, tileheight
    global screen, clock, tiles, peashooter, bg
    global money

    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode((Width, Height))

    pygame.display.set_caption("presidents vs nazis")

    clock = pygame.time.Clock()

    tiles = [[0 for _ in range(tilewidth)] for _ in range(tileheight)]

    peashooter = pygame.image.load("images/peashooter.png").convert_alpha()
    peashooter = pygame.transform.scale(peashooter, (60, 60))

    bg = pygame.image.load("images/currentBGimage.png").convert_alpha()
    bg = pygame.transform.scale(bg, (Width, Height))

    setup_defenders()

def update():
    global money
    pygame.display.update()
    clock.tick(Time)
    money += 5
    time.sleep(0.05)
    print(money)

class Defender:
    def __init__(self, type, x, y, damage, health, price, image):
        self.type = type
        self.x = x
        self.y = y
        self.damage = damage
        self.health = health
        self.image = image
        self.price = price
    def damaged(self, damage):
        self.health -= damage
        if self.health <= 0:
            pass # should be death 

def draw_text(text, font, color, x, y):
    # Render the text
    text_surface = font.render(text, True, color)
    # Blit the text surface onto the screen at the specified position
    screen.blit(text_surface, (x, y))




def draw_grid():
    global money
    for x in range(tilewidth):
        for y in range(tileheight):
            sqr = pygame.Rect(x * 80 + + 60 , y * 80 + 100, 60, 60)
            if tiles[y][x] == 0:
                pygame.draw.rect(screen, (36, 200, 100), sqr)
            else:
                defender = tiles[y][x]
                screen.blit(defender.image, (x * 80 + 60, y * 80 + 100))
            if pygame.mouse.get_pressed()[0]:
                if sqr.collidepoint(pygame.mouse.get_pos()):
                    if money >= 100 and tiles[y][x] == 0:
                        money -= 100
                        tiles[y][x] = Defender("peashooter", x, y, 10, 100, 100, peashooter)
                        print(y, x)
                        print("placed peashooter and -100 money")



def main():
    setup()
    font = pygame.font.SysFont("Arial", 30)
    running = True
    while running:
        #screen.fill(screenColor)
        screen.blit(bg, (0, 0))
        draw_grid()
        draw_text("Money: " + str(money), font, (255,255,255), 0,0)
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