import pygame
import time
import random
import network.client as client
import threading

global screenColor, Width, Height, Time, tilewidth, tileheight
global screen, clock, tiles, bg
global current_defender,peashooter, sunflower, projectile, projectiles, current_attacker, attackers
global defenderMoney, attackerMoney
global AllPlayersReady
global defend

defenderMoney = 100
attackerMoney = 100
Width = 800
Height = 600
Time = 60
tilewidth = 9
tileheight = 5
screenColor = (26, 138, 35)
current_defender = 0
current_attacker = 0
attackers = []
projectiles = []
AllPlayersReady = False
defend = None

def ConnectToMultiplayerHost(host, port):
    print("Connecting to server...")
    client.init() #self explanatory
    client.ConnectToServer(host, port) #connect to server with host and port
    client.SetEventHandler(ServerEventHandler) #set the event handler to a function that will handle the messages it gets from the server
    client.StartReceiving()

def ServerEventHandler(msg):
    global AllPlayersReady
    global defend
    global tiles
    
    print(f"EventHandler:{msg}")
    if msg == "[MESSAGE]attacker[MESSAGE]":
        defend = False
    elif msg == "[MESSAGE]defender[MESSAGE]":
        defend = True
    elif msg == "[MESSAGE]SERVER FULL[MESSAGE]":
        AllPlayersReady = True
        print("All players are ready")
    elif "[REQUEST]ADD" in msg: #[REQUEST]ADD|0|{salt}[REQUEST]
        msg = msg.replace("[REQUEST]", "").split("|")
        #type = msg[1] (YONA YOU LAZY ADD TYPES OF MONEY ALREADY)
        amount = int(msg[2])
        AddMoney(amount)
    elif "[REQUEST]select" in msg: #[REQUEST]select|index|index|type[REQUEST]
        msg = msg.replace("[REQUEST]", "").split("|")
        index = int(msg[1])
        index2 = int(msg[2])
        type = int(msg[3])
        if type == 1:
            tiles[index][index2] = Defender("sunflower", index - 30, index2 - 15, 10, 100, 100, sunflower)
        elif type == 2:
            tiles[index][index2] = Defender("peashooter", index - 30, index2 - 15, 10, 100, 100, peashooter)

def AddMoney(money):
    global defenderMoney
    global attackerMoney
    if defend:
        defenderMoney += money
    else:
        attackerMoney += money

def setup_defenders():
    global screenColor, Width, Height, Time, tilewidth, tileheight
    global screen, clock, tiles, peashooter, bg, sunflower, sap_proj, defend
    
    peashooter_setup = Defender("peashooter", 0, 0, 1, 5,100, "images/sap.png")
    sunflower_setup = Defender("sunflower", 0, 0, 0, 3,100, "images/sunflower.png")

    peashooter = pygame.image.load("images/sap.png").convert_alpha()
    peashooter = pygame.transform.scale(peashooter, (70, 70))
    sap_proj = pygame.image.load("images/sap pro.png").convert_alpha()
    sap_proj = pygame.transform.scale(sap_proj, (60, 60))

    sunflower = pygame.image.load("images/salt shaker .png").convert_alpha()
    sunflower = pygame.transform.scale(sunflower, (75, 75))
    
    peashooter_thread = threading.Thread(target=peashooter_action)
    peashooter_thread.start()

def select_defender():
    global current_defender
    if pygame.key.get_pressed()[pygame.K_1]:
        current_defender = 1
    if pygame.key.get_pressed()[pygame.K_2]:
        current_defender = 2
def select_attacker():
    global current_attacker
    if pygame.key.get_pressed()[pygame.K_1]:
        current_attacker = 1
    if pygame.key.get_pressed()[pygame.K_2]:
        current_attacker = 2
    if pygame.key.get_pressed()[pygame.K_3]:
        current_attacker = 3
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
    global screen, clock, tiles, peashooter, bg, sunflower, sap_proj, moshe, shlomi, josh
    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode((Width  + 200, Height))

    pygame.display.set_caption("presidents vs nazis")

    clock = pygame.time.Clock()


    shlomi = pygame.image.load("images/golden_Enemy.png").convert_alpha()
    shlomi = pygame.transform.scale(shlomi, (100, 90))

    moshe = pygame.image.load("images/normal_Enemy.png").convert_alpha()
    moshe = pygame.transform.scale(moshe, (100, 90))

    josh = pygame.image.load("images/shotgun_Enemy.png").convert_alpha()
    josh = pygame.transform.scale(josh, (100, 90))

    tiles = [[0 for _ in range(tilewidth)] for _ in range(tileheight)]

    bg = pygame.image.load("images/updatebg.png").convert_alpha()
    bg = pygame.transform.scale(bg, (Width + 200, Height))
    
    setup_defenders()



    #tiles[0][0] = Defender("peashooter", 0, 0, 30, 100, 100, peashooter) # For testing purposes
    #print(tiles[0][0].health)      



    projectiles = []





def update():
    global defenderMoney, projectile, attackerMoney
    select_defender()
    check_attacker_defender_collisions()
    update_projectiles()
    pygame.display.update()
    clock.tick(Time)
    time.sleep(0.05)

def update_attacker():
    global defenderMoney, projectile, attackerMoney, current_attacker
    select_attacker()
    check_attacker_defender_collisions()
    update_projectiles()
    pygame.display.update()
    clock.tick(Time)
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
        print(f"{self.type} damaged for {damage} health. Remaining health: {self.health}")
        self.health -= damage
        if self.health <= 0:
            print(f"{self.type} has been defeated and removed from the game.")
            pass # should be death 
class Attacker:
    def __init__(self, type, x, y, damage, health, price, image, stopped = False):
        self.type = type
        self.x = x
        self.y = y
        self.damage = damage
        self.health = health
        self.image = image
        self.price = price
        self.stopped = False
    def damaged(self, damage):
        self.health -= damage
        print(f"{self.type} damaged for {damage} health. Remaining health: {self.health}")
        if self.health <= 0:
            attackers.remove(self)  # Remove attacker from the list when health is 0
            print(f"{self.type} has been defeated and removed from the game.")
        
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
        for attacker in attackers[:]:
            attacker_rect = pygame.Rect(attacker.x, attacker.y, 60, 60)  # Adjust size as needed
            if projectile.colliderect(attacker_rect):
                attacker.damaged(10)  # Assuming each projectile does 10 damage
                if projectile in projectiles:
                    projectiles.remove(projectile)
                break  # Stop checking other attackers for this projectile

        if projectile.x > Width:
            projectiles.remove(projectile)



def draw_projectiles():
    global projectiles, sap_proj # Ensure projectiles is referenced as global
    for projectile in projectiles:
        # Draw each projectile on the screen
        screen.blit(sap_proj, (projectile.x, projectile.y - 20))

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

def getinput(status, loc = 0):
    global defenderMoney, current_defender, x, y
    global attackerMoney

    if status == "defender":
        if current_defender == 1 and defenderMoney >= 50 and tiles[y][x] == 0:
            defenderMoney -= 50
            client.client_socket.send(f"[REQUEST]select|{y}|{x}|1[REQUEST]".encode())
            tiles[y][x] = Defender("sunflower", x - 30, y - 15, 30, 100, 100, sunflower)
            print(y, x)
            print("placed sunflower and -50 defenderMoney")
        elif current_defender == 2 and defenderMoney >= 100 and tiles[y][x] == 0:
            defenderMoney -= 100
            client.client_socket.send(f"[REQUEST]select|{y}|{x}|2[REQUEST]".encode())
            tiles[y][x] = Defender("peashooter", x - 30, y - 15, 30, 100, 100, peashooter)
            print(y, x)
            print("placed peashooter and -100 defenderMoney")
    
    if status == "attacker":
        print("attacker clicked", loc)
        print("attacker clicked", loc)
        if current_attacker == 1 and attackerMoney >= 50:
            attackerMoney -= 50
            # Place attacker at the right edge, row 'loc'
            attackers.append(Attacker("moshe", Width + 200 - 100, loc * 80 + 100, 10, 10, 50, moshe))
        elif current_attacker == 2 and attackerMoney >= 100:
            attackerMoney -= 100
            attackers.append(Attacker("shlomi", Width + 200 - 100, loc * 80 + 100, 20, 20, 100, shlomi))
        elif current_attacker == 3 and attackerMoney >= 150:
            attackerMoney -= 150
            attackers.append(Attacker("josh", Width + 200 - 100, loc * 80 + 100, 30, 30, 150, josh))
    if status == "test":
        print("test clicked", loc)
        attackers.append(Attacker("josh", Width + 200 - 100, loc * 80 + 100, 30, 30, 150, josh))
    print("boo")

def update_attackers():
    global attackers
    for attacker in attackers[:]:
        if not getattr(attacker, "stopped", False):  # Only move if not stopped
            attacker.x -= 5
        if attacker.x < -100:
            attackers.remove(attacker)
            print(f"{attacker.type} has left the screen and been removed from the game. ATTACKERS WONNNNNNN")

def check_attacker_defender_collisions():
    global attackers, tiles
    for attacker in attackers:
        blocked = False
        for y in range(tileheight):
            for x in range(tilewidth):
                defender = tiles[y][x]
                if defender != 0:
                    defender_rect = pygame.Rect(x * 80 + 53, y * 80 + 92, 60, 60)
                    attacker_rect = pygame.Rect(attacker.x, attacker.y - 30, 60, 60)
                    if attacker_rect.colliderect(defender_rect):
                        defender.damaged(attacker.damage)
                        attacker.stopped = True
                        blocked = True
                        if defender.health <= 0:
                            tiles[y][x] = 0
                        break  # Stop checking other defenders for this attacker
            if blocked:
                break
        if not blocked:
            attacker.stopped = False
def draw_attackers():
    global attackers
    for attacker in attackers:
        screen.blit(attacker.image, (attacker.x, attacker.y - 30))

def place_attacker():
    idk = pygame.image.load("images/mize.png").convert_alpha()
    idk = pygame.transform.scale(idk, (70, 70))
    for y in range(tileheight):
        rect = pygame.Rect(850, y * 80 + 100, 60, 60)
        screen.blit(idk, ( 850, y * 80 + 92))
        if pygame.mouse.get_pressed()[0] and rect.collidepoint(pygame.mouse.get_pos()): 
            getinput("attacker", y)
            print("placed attacker")


def display_current(status):
    global current_defender, current_attacker
    if status == "defender":
        draw_text("Current Defender is:", pygame.font.SysFont("Arial", 30), (0, 255, 0), 425, 40)
        if current_defender == 1:
            screen.blit(sunflower, (650, 20))
        elif current_defender == 2:
            screen.blit(peashooter, (650, 20))
        else:
            pass
    elif status == "attacker":
        draw_text("Current Attacker is:", pygame.font.SysFont("Arial", 30), (0, 255, 0), 425, 40)
        if current_attacker == 1:
            screen.blit(moshe, (625, 0))
        elif current_attacker == 2:
            screen.blit(shlomi, (625, 0))
        elif current_attacker == 3:
            screen.blit(josh, (625, 0))
            


def defenderGameLoop():
    attackerSetup()
    setup()
    font = pygame.font.SysFont("Arial", 30)
    running = True
    while running:
        #screen.fill(screenColor)
        screen.blit(bg, (0, 0))
        draw_grid("defender")
        draw_projectiles()
        draw_attackers()
        update_attackers()
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
    update_attacker()
    font = pygame.font.SysFont("Arial", 30)
    running = True
    while running:
        screen.blit(bg, (0, 0))
        draw_grid("attacker")
        place_attacker()
        draw_projectiles()
        draw_attackers()
        update_attackers()        
        draw_text("Money: " + str(attackerMoney), font, (255,255,255), 0,0)
        display_current("attacker")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                print("You clicked the X button")
        update_attacker()

    pygame.quit()


def main():
    global AllPlayersReady
    global defend

    MultiplayerThread = threading.Thread(target=ConnectToMultiplayerHost, args=("127.0.0.1", 4040))
    MultiplayerThread.start()

    while not AllPlayersReady:
        time.sleep(0.5)
        print("Waiting for all players to be ready...")

    print("All players are ready!")

    client.client_socket.send("[MESSAGE]PleaseRespond[MESSAGE]".encode())

    while defend is None:
        time.sleep(0.1)
        print("Waiting for server to assign player role...")

    if defend:
        print("You are a defender")
        defenderGameLoop()
    else:
        print("You are an attacker")
        attackerGameLoop()


if __name__ == "__main__":
    main()  