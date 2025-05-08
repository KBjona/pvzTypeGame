import pygame
import time
import random
import network.client as client
import threading

global screenColor, Width, Height, Time, tilewidth, tileheight
global screen, clock, tiles, bg
global current_defender,peashooter, sunflower, projectile, projectiles
global money


money = 0 
Width = 800
Height = 600
Time = 60
tilewidth = 9
tileheight = 5
screenColor = (26, 138, 35)
current_defender = 0
projectiles = []


def setup_defenders():
    global peashooter, sunflower
    peashooter_setup = Defender("peashooter", 0, 0, 10, 100,100, "images/peashooter.png")
    sunflower_setup = Defender("sunflower", 0, 0, 10, 100,100, "images/sunflower.png")

def select_defender():
    global current_defender
    print(current_defender)
    if pygame.key.get_pressed()[pygame.K_1]:
        current_defender = 1
    if pygame.key.get_pressed()[pygame.K_2]:
        current_defender = 2

def setup():
    global screenColor, Width, Height, Time, tilewidth, tileheight
    global screen, clock, tiles, peashooter, bg, sunflower
    global money

    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode((Width, Height))

    pygame.display.set_caption("presidents vs nazis")

    clock = pygame.time.Clock()

    tiles = [[0 for _ in range(tilewidth)] for _ in range(tileheight)]

    peashooter = pygame.image.load("images/peashooter.png").convert_alpha()
    peashooter = pygame.transform.scale(peashooter, (60, 60))
    sunflower = pygame.image.load("images/sunflower.png").convert_alpha()
    sunflower = pygame.transform.scale(sunflower, (60, 60))

    bg = pygame.image.load("images/yuvalsbg.png").convert_alpha()
    bg = pygame.transform.scale(bg, (Width, Height))

    sunflower_thread = threading.Thread(target=sunflower_action)
    sunflower_thread.start()
    peashooter_thread = threading.Thread(target=peashooter_action)
    peashooter_thread.start()

    setup_defenders()

    projectiles = []

def update():
    global money, projectile
    select_defender()
    update_projectiles()
    pygame.display.update()
    clock.tick(Time)
    money += 1
    time.sleep(0.05)
 

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
def peashooter_action():
    global tiles, projectile, projectiles
    while True:
        time.sleep(random.randint(2,4))
        for y in range(tileheight):
            for x in range(tilewidth):
                if tiles[y][x] != 0:
                    if tiles[y][x].type == "peashooter":
                            projectile = pygame.rect.Rect(x * 80 + 60, y * 80 + 115, 10, 10)
                            projectiles.append(projectile)
                            print("peashooter shot")
def update_projectiles():
    global projectiles
    for projectile in projectiles[:]:
        # Move the projectile to the right
        projectile.x += 10
        # Remove the projectile if it goes off-screen
        if projectile.x > Width:
            projectiles.remove(projectile)



def draw_projectiles():
    global projectiles  # Ensure projectiles is referenced as global
    for projectile in projectiles:
        # Draw each projectile on the screen
        pygame.draw.rect(screen, (0, 255, 0), projectile)

def sunflower_action():
    global tiles, money
    while True:
        time.sleep(random.randint(4,6))
        for y in range(tileheight):
            for x in range(tilewidth):
                if tiles[y][x] != 0:
                    if tiles[y][x].type == "sunflower":
                            money += 50

def draw_grid():
    global money, current_defender
    for x in range(tilewidth):
        for y in range(tileheight):
            sqr = pygame.Rect(x * 80 + 60 , y * 80 + 100, 60, 60)
            if tiles[y][x] == 0:
                pass
            else:
                defender = tiles[y][x]
                screen.blit(defender.image, (x * 80 + 60, y * 80 + 100))
            if pygame.mouse.get_pressed()[0]:
                if sqr.collidepoint(pygame.mouse.get_pos()):
                    if current_defender == 1:
                        if money >= 50 and tiles[y][x] == 0:
                            money -= 50
                            tiles[y][x] = Defender("sunflower", x, y, 10, 100, 100, sunflower)
                            print(y, x)
                            print("placed sunflower and -50 money")
                    elif current_defender == 2:
                        if money >= 100 and tiles[y][x] == 0:
                            money -= 100
                            tiles[y][x] = Defender("peashooter", x, y, 10, 100, 100, peashooter)
                            print(y, x)
                            print("placed peashooter and -100 money")

def display_current_defender():
    global current_defender
    draw_text("Current Defender is:", pygame.font.SysFont("Arial", 30), (0, 255, 0), 425, 40)
    if current_defender == 1:
        screen.blit(sunflower, (700, 20))
    elif current_defender == 2:
        screen.blit(peashooter, (700, 20))
    else:
        pass

def main():
    global current_defender
    setup()
    font = pygame.font.SysFont("Arial", 30)
    running = True
    while running:
        #screen.fill(screenColor)
        screen.blit(bg, (0, 0))
        draw_grid()
        draw_projectiles()
        draw_text("Money: " + str(money), font, (255,255,255), 0,0)
        display_current_defender()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                print("You clicked the X button")
        update()
    pygame.quit()

main()
