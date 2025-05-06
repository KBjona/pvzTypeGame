import pygame
import time

Width = 800
Height = 600
Time = 60
tilewidth = 8
tileheight =5

screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("presidents vs nazis")
clock = pygame.time.Clock()
tiles = [[0 for _ in range(tilewidth)] for _ in range(tileheight)]

def draw_grid():
    for i in range(tilewidth):
        for j in range(tileheight):
            #print(tiles)
                sqr = pygame.rect.Rect(i * 100, j * 100 + 60, 80, 80)
                if tiles[j][i] == 0:
                    pygame.draw.rect(screen, (255, 255, 255), sqr)

                elif tiles[j][i] == 1:
                    pygame.draw.rect(screen, (0, 0, 0), sqr)
                

                if pygame.mouse.get_pressed()[0]:
                    if sqr.collidepoint(pygame.mouse.get_pos()):
                        tiles[j][i] = 1
                        print(j, i)
                        #print("you clicked on the square")

def main():
    pygame.init()
    running = True
    while running:
        screen.fill((26, 138, 35))
        draw_grid()
        for event in pygame.event.get():


            if event.type == pygame.QUIT:
                running = False
                print("you clicked the X button")


        pygame.display.update()
        clock.tick(Time)
    time.sleep(0.05)
    pygame.quit()
try:
    main()
except SystemExit:
    print("you closed the window")
except Exception as e:
    print("An error occurred:", )