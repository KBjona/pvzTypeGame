import pygame
import threading
import network.client as client
import socket  # For validating hostnames/IPs

pygame.init()

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

# Event handler for server messages
def EventHandler(msg):
    global AllPlayersReady
    print(f"EventHandler: {msg}")
    if msg == "[MESSAGE]SERVER FULL[MESSAGE]":
        AllPlayersReady = True
        print("All players are ready")

# Connect to the server with validation
def connect(host, port):
    try:
        # Validate the host
        socket.gethostbyname(host)  # This will raise an exception if the host is invalid

        # Validate the port
        port = int(port)
        if port < 1 or port > 65535:
            raise ValueError("Port must be between 1 and 65535")

        # Proceed with the connection
        client.init()
        client.ConnectToServer(host, port)
        client.SetEventHandler(EventHandler)
        client.StartReceiving()
        print(f"Connecting to server: {host} on port: {port}")
    except ValueError as ve:
        print(f"Invalid input: {ve}")
    except socket.gaierror:
        print("Invalid host: Unable to resolve hostname or IP address")
    except Exception as e:
        print(f"An error occurred: {e}")

# Second page function
def second_page():
    # Text box definitions
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

    # Connect button
    connect_button_rect = pygame.Rect(50, 300, 210, 60)
    connect_button_color = (0, 255, 0)
    connect_button_hover_color = (0, 200, 0)
    connect_button_text = "Connect"

    # Cancel button
    cancel_button_rect = pygame.Rect(50, 400, 210, 60)
    cancel_button_color = (255, 0, 0)
    cancel_button_hover_color = (200, 0, 0)
    cancel_button_text = "Cancel"

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
                    if server_host_text.strip() == "" or server_port_text.strip() == "":
                        print("Error: Both Server Host and Server Port must be filled")
                    else:
                        threading.Thread(target=connect, args=(server_host_text.strip(), server_port_text.strip())).start()
                elif cancel_button_rect.collidepoint(event.pos):
                    # Clear the text boxes
                    server_host_text = ""
                    server_port_text = ""
                elif back_button["rect"].collidepoint(event.pos):
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
            (cancel_button_rect, cancel_button_text, cancel_button_color, cancel_button_hover_color),
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

# Main loop
is_running = True
while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_definitions[0]["rect"].collidepoint(event.pos):  # "play multiplayer" button
                second_page()

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