import pygame
import threading
import network.client as client
import socket  # For validating hostnames/IPs
import webbrowser  # For opening the tutorial link
import os
import sys

pygame.init()
pygame.mixer.init()

# Load click sound
click_sound = pygame.mixer.Sound("eating-sound-effect-36186.mp3")

# Global variables
global AllPlayersReady
AllPlayersReady = False

# Screen setup
pygame.display.set_caption("pvz?")
screen_width = 1280
screen_height = 768
window_surface = pygame.display.set_mode((screen_width, screen_height))

# Load the background images
background2 = pygame.image.load("images/lazanya (2).png")
background = pygame.image.load("images/Copy of Untitled.png")
background = pygame.transform.scale(background, (1024, 768))  # Keep the background size fixed

# Font for button text
font = pygame.font.Font(None, 36)

# Button definitions
button_definitions = [
    {"rect": pygame.Rect(25, 100, 210, 60), "text": "play multiplayer", "color": "#B87333", "hover_color": "#964B00"},
    {"rect": pygame.Rect(25, 180, 210, 60), "text": "play singleplayer", "color": (0, 255, 0), "hover_color": (0, 200, 0)},
    {"rect": pygame.Rect(25, 260, 210, 60), "text": "tutorial", "color": (255, 0, 0), "hover_color": (200, 0, 0)},
    {"rect": pygame.Rect(3, 340, 250, 60), "text": "server setup tutorial", "color": (71, 55, 28), "hover_color": (36, 25, 8)},
    {"rect": pygame.Rect(25, 420, 210, 60), "text": "credit", "color": "#B87333", "hover_color": "#964B00"},
]

back_button = {
    "rect": pygame.Rect(25, 700, 150, 50),
    "text": "Back",
    "color": (255, 0, 0),
    "hover_color": (200, 0, 0),
}

def connect(host, port):
    args = [sys.executable, "Main.py", host, port]
    os.execvp(args[0], args)

# Second page function
def second_page():
    server_host_rect = pygame.Rect(50, 120, 340, 60)
    server_host_color = (255, 255, 255)
    server_host_border_color = (128, 128, 128)
    server_host_text = ""
    server_host_active = False

    server_port_rect = pygame.Rect(50, 200, 340, 60)
    server_port_color = (255, 255, 255)
    server_port_border_color = (128, 128, 128)
    server_port_text = ""
    server_port_active = False

    connect_button_rect = pygame.Rect(50, 300, 210, 60)
    connect_button_color = (0, 255, 0)
    connect_button_hover_color = (0, 200, 0)
    connect_button_text = "Connect"

    second_page_running = True
    while second_page_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                second_page_running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                second_page_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                server_host_active = server_host_rect.collidepoint(event.pos)
                server_port_active = server_port_rect.collidepoint(event.pos)
                if connect_button_rect.collidepoint(event.pos):
                    click_sound.play()
                    if not server_host_text.strip() == "" and not server_port_text.strip() == "":
                        threading.Thread(target=connect, args=(server_host_text.strip(), server_port_text.strip())).start()
                elif back_button["rect"].collidepoint(event.pos):
                    click_sound.play()
                    second_page_running = False
            elif event.type == pygame.KEYDOWN:
                if server_host_active:
                    if event.key == pygame.K_BACKSPACE:
                        server_host_text = server_host_text[:-1]
                    else:
                        server_host_text += event.unicode
                elif server_port_active:
                    if event.key == pygame.K_BACKSPACE:
                        server_port_text = server_port_text[:-1]
                    else:
                        server_port_text += event.unicode

        # Draw the second page
        window_surface.fill((0, 0, 0))
        pygame.draw.rect(window_surface, (255, 255, 255), (0, 0, 420, screen_height))
        window_surface.blit(background2, (screen_width - 1024, 0))  # Use background2 for the second screen

        # Draw text boxes
        for rect, text, color, border_color, placeholder in [
            (server_host_rect, server_host_text, server_host_color, server_host_border_color, "Server Host (e.g. 127.0.0.1)"),
            (server_port_rect, server_port_text, server_port_color, server_port_border_color, "Server Port (e.g. 4040, 8080)"),
        ]:
            pygame.draw.rect(window_surface, border_color, rect, 2)
            pygame.draw.rect(window_surface, color, rect.inflate(-4, -4))
            if text == "":
                placeholder_surface = font.render(placeholder, True, (128, 128, 128))
                placeholder_rect = placeholder_surface.get_rect(midleft=(rect.x + 10, rect.centery))
                window_surface.blit(placeholder_surface, placeholder_rect)
            else:
                text_surface = font.render(text, True, (0, 0, 0))
                text_rect = text_surface.get_rect(midleft=(rect.x + 10, rect.centery))
                window_surface.blit(text_surface, text_rect)

        # Draw buttons
        for rect, text, color, hover_color in [
            (connect_button_rect, connect_button_text, connect_button_color, connect_button_hover_color),
            (back_button["rect"], back_button["text"], back_button["color"], back_button["hover_color"]),
        ]:
            if rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(window_surface, hover_color, rect)
            else:
                pygame.draw.rect(window_surface, color, rect)
            text_surface = font.render(text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=rect.center)
            window_surface.blit(text_surface, text_rect)

        pygame.display.update()

# Credit page function
def credit_page():
    credit_running = True
    while credit_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                credit_running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                credit_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button["rect"].collidepoint(event.pos):
                    click_sound.play()
                    credit_running = False

        window_surface.fill((30, 30, 30))
        # Draw credit text
        credit_text = [
            " FancyBread - networking(coolest thing ever) also ServerGUI and helped in random stuff.(chatgpt hater)",
            "red_head_redemption (first ginger) -  did the game gui and the game design.(chatgpt hater) "              ,
            "zohar - did the character design.(chatgpt hater)",
            "jonathan - did the game.(chatgpt hater)",
            "sharon frailich - our loved teacher (;",
            "itay meron tsarfaty - did the sound effects and the music.",
        ]
        for i, line in enumerate(credit_text):
            text_surface = font.render(line, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(screen_width // 2, 200 + i * 50))
            window_surface.blit(text_surface, text_rect)

        # Draw back button
        rect = back_button["rect"]
        if rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(window_surface, back_button["hover_color"], rect)
        else:
            pygame.draw.rect(window_surface, back_button["color"], rect)
        text_surface = font.render(back_button["text"], True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=rect.center)
        window_surface.blit(text_surface, text_rect)

        pygame.display.update()

# Main loop
is_running = True
while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_definitions[0]["rect"].collidepoint(event.pos):  # "play multiplayer" button
                click_sound.play()
                second_page()
            elif button_definitions[1]["rect"].collidepoint(event.pos):  # "play singleplayer" button
                click_sound.play()
                # Add your singleplayer logic here
            elif button_definitions[2]["rect"].collidepoint(event.pos):  # "tutorial" button
                click_sound.play()
                webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
            elif button_definitions[3]["rect"].collidepoint(event.pos):  # "server setup tutorial" button
                click_sound.play()
                webbrowser.open("https://www.youtube.com/watch?v=HHOLpVQFsiA")
                webbrowser.open("https://www.youtube.com/watch?v=VBlFHuCzPgY")                   
            elif button_definitions[4]["rect"].collidepoint(event.pos):  # "credit" button
                click_sound.play()
                credit_page()

    # Draw the main page
    window_surface.fill((255, 255, 255))
    window_surface.blit(background, (screen_width - 1024, 0))  # Stick background to the right

    # Draw buttons
    mouse_pos = pygame.mouse.get_pos()
    for button in button_definitions:
        rect, text, color, hover_color = button["rect"], button["text"], button["color"], button["hover_color"]
        if rect.collidepoint(mouse_pos):
            pygame.draw.rect(window_surface, hover_color, rect)
        else:
            pygame.draw.rect(window_surface, color, rect)
        text_surface = font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=rect.center)
        window_surface.blit(text_surface, text_rect)

    pygame.display.update()
