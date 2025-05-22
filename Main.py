import pygame
import time
import random
import network.client as client
import threading

global screenColor, Width, Height, Time, tilewidth, tileheight
global screen, clock, tiles, bg
global current_defender,peashooter, sunflower, projectile, projectiles
global defenderMoney, attackerMoney


defenderMoney = 500
attackerMoney = 500
Width = 800
Height = 600
Time = 60
tilewidth = 9
tileheight = 5
screenColor = (26, 138, 35)
current_defender = 0
projectiles = []


def setup_defenders():
    global screenColor, Width, Height, Time, tilewidth, tileheight
    global screen, clock, tiles, peashooter, bg, sunflower, sap_proj
    
    peashooter_setup = Defender("peashooter", 0, 0, 1, 5,100, "images/sap.png")
    sunflower_setup = Defender("sunflower", 0, 0, 0, 3,100, "images/sunflower.png")

    peashooter = pygame.image.load("images/sap.png").convert_alpha()
    peashooter = pygame.transform.scale(peashooter, (70, 70))
    sap_proj = pygame.image.load("images/sap pro.png").convert_alpha()
    sap_proj = pygame.transform.scale(sap_proj, (60, 60))

    sunflower = pygame.image.load("images/salt shaker .png").convert_alpha()
    sunflower = pygame.transform.scale(sunflower, (75, 75))

    sunflower_thread = threading.Thread(target=sunflower_action)
    sunflower_thread.start()
    peashooter_thread = threading.Thread(target=peashooter_action)
    peashooter_thread.start()

def select_defender():
    global current_defender
    if pygame.key.get_pressed()[pygame.K_1]:
        current_defender = 1
    if pygame.key.get_pressed()[pygame.K_2]:
        current_defender = 2

def setup():
    global screenColor, Width, Height, Time, tilewidth, tileheight
    global screen, clock, tiles, peashooter, bg, sunflower, sap_proj

    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode((Width, Height))

    pygame.display.set_caption("presidents vs nazis")

    clock = pygame.time.Clock()

    tiles = [[0 for _ in range(tilewidth)] for _ in range(tileheight)]

    bg = pygame.image.load("images/yuvalsbg.png").convert_alpha()
    bg = pygame.transform.scale(bg, (Width, Height))

    setup_defenders()

    projectiles = []

def attackerSetup():
    global screenColor, Width, Height, Time, tilewidth, tileheight
    global screen, clock, tiles, peashooter, bg, sunflower, sap_proj

    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode((Width  + 200, Height))

    pygame.display.set_caption("presidents vs nazis")

    clock = pygame.time.Clock()

    tiles = [[0 for _ in range(tilewidth)] for _ in range(tileheight)]

    bg = pygame.image.load("images/updatebg.png").convert_alpha()
    bg = pygame.transform.scale(bg, (Width + 200, Height))
    
    setup_defenders()

    projectiles = []

def update():
    global defenderMoney, projectile, attackerMoney
    select_defender()
    update_projectiles()
    pygame.display.update()
    clock.tick(Time)
    attackerMoney += 3
    time.sleep(0.05)
 

class Defender:
    def __init__(self, type, x, y, damage, health, price, image, time = 0):
        self.type = type
        self.x = x
        self.y = y
        self.damage = damage
        self.health = health
        self.image = image
        self.price = price
        self.time = time
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
        for y in range(tileheight):
            for x in range(tilewidth):
                if tiles[y][x] != 0:
                    if tiles[y][x].type == "peashooter":
                        tiles[y][x].time += 0.001
                        if tiles[y][x].time >= 2000:
                            tiles[y][x].time = 0
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
    global projectiles, sap_proj # Ensure projectiles is referenced as global
    for projectile in projectiles:
        # Draw each projectile on the screen
        screen.blit(sap_proj, (projectile.x, projectile.y - 20))

def sunflower_action():
    global tiles, defenderMoney
    while True:
        time.sleep(random.randint(4,6))
        for y in range(tileheight):
            for x in range(tilewidth):
                if tiles[y][x] != 0:
                    if tiles[y][x].type == "sunflower":
                            defenderMoney += 50

def draw_grid(status):
    global defenderMoney, current_defender,x ,y
    for x in range(tilewidth):
        for y in range(tileheight):
            sqr = pygame.Rect(x * 80 + 60 , y * 80 + 100, 60, 60)
            if tiles[y][x] == 0:
                pass
            else:
                defender = tiles[y][x]
                screen.blit(defender.image, (x * 80 + 53, y * 80 + 92))
    
            if pygame.mouse.get_pressed()[0] and sqr.collidepoint(pygame.mouse.get_pos()): 
                getinput(status)

def getinput(status):
    global defenderMoney, current_defender, x, y

    if status == "defender":
        if current_defender == 1 and defenderMoney >= 50 and tiles[y][x] == 0:
            defenderMoney -= 50
            tiles[y][x] = Defender("sunflower", x - 30, y - 15, 10, 100, 100, sunflower)
            print(y, x)
            print("placed sunflower and -50 defenderMoney")
        elif current_defender == 2 and defenderMoney >= 100 and tiles[y][x] == 0:
            defenderMoney -= 100
            tiles[y][x] = Defender("peashooter", x - 30, y - 15, 10, 100, 100, peashooter)
            print(y, x)
            print("placed peashooter and -100 defenderMoney")


def place_attacker():
    idk = pygame.image.load("images/mize.png").convert_alpha()
    idk = pygame.transform.scale(idk, (70, 70))
    for y in range(tileheight):
        screen.blit(idk, ( 850, y * 80 + 92))


def display_current(status):
    global current_defender
    if status == "defender":
        draw_text("Current Defender is:", pygame.font.SysFont("Arial", 30), (0, 255, 0), 425, 40)
        if current_defender == 1:
            screen.blit(sunflower, (700, 20))
        elif current_defender == 2:
            screen.blit(peashooter, (700, 20))
        else:
            pass
    elif status == "attacker":
        draw_text("Current Attacker is:", pygame.font.SysFont("Arial", 30), (0, 255, 0), 425, 40)


def defenderGameLoop():
    setup()
    font = pygame.font.SysFont("Arial", 30)
    running = True
    while running:
        #screen.fill(screenColor)
        screen.blit(bg, (0, 0))
        draw_grid("defender")
        draw_projectiles()
        draw_text("Money: " + str(defenderMoney), font, (255,255,255), 0,0)
        display_current("defender")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                print("You clicked the X button")
        update()

    pygame.quit()

def attackerGameLoop():
    attackerSetup()
    font = pygame.font.SysFont("Arial", 30)
    running = True
    while running:
        screen.blit(bg, (0, 0))
        draw_grid("attacker")
        place_attacker()
        draw_projectiles()
        draw_text("Money: " + str(attackerMoney), font, (255,255,255), 0,0)
        display_current("attacker")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                print("You clicked the X button")
        update()

    pygame.quit()


def main():
    defenderGameLoop()
    attackerGameLoop()


if __name__ == "__main__":
    main()  