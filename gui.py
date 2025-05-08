import pygame
import network.client as client
import threading
pygame.init()

global AllPlayersReady
AllPlayersReady = False

pygame.display.set_caption("pvz?")

# Change the screen size (increase width)
screen_width = 1280  # Increased width
screen_height = 768  # Keep the height the same
window_surface = pygame.display.set_mode((screen_width, screen_height))

# Load the background image
background = pygame.image.load("images/Copy of Untitled.png")
background = pygame.transform.scale(background, (1024, 768))  # Keep the background size fixed

# Define the main button
button_color = ("#B87333")  
button_hover_color = ("#964B00")  # Darker green
button_rect = pygame.Rect(25, 100, 210, 60)  # x, y, width, height
button_text = "play multiplayer"

# Define additional buttons individually with unique colors
button2_rect = pygame.Rect(25, 180, 210, 60)
button2_text = "play singleplayer"
button2_color = (0, 255, 0)  # Red color for Button 2
button2_hover_color = (0, 200,0)  # Darker red for hover

button3_rect = pygame.Rect(25, 260, 210, 60)
button3_text = "tutorial"
button3_color = (255,0,0)  # Green color for Button 3
button3_hover_color = (200,0,0)  # Darker green for hover

button4_rect = pygame.Rect(25, 340, 210, 60)
button4_text = "Button 4"
button4_color = (0, 0, 255)  # Blue color for Button 4
button4_hover_color = (0, 0, 200)  # Darker blue for hover

button5_rect = pygame.Rect(25, 420, 210, 60)
button5_text = "Button 5"
button5_color = (255, 255, 0)  # Yellow color for Button 5
button5_hover_color = (200, 200, 0)  # Darker yellow for hover

# Define the "Back" button
back_button_color = (255, 0, 0)  # Red color
back_button_hover_color = (200, 0, 0)  # Darker red
back_button_rect = pygame.Rect(25, 700, 150, 50)  # Bottom-left corner
back_button_text = "Back"

# Font for button text
font = pygame.font.Font(None, 36)

def EventHandler(msg):
    global AllPlayersReady
                        
    print(f"EventHandler:{msg}")
    if msg == "[MESSAGE]SERVER FULL[MESSAGE]":
        AllPlayersReady = True
        print("All players are ready")

def connect(host, port):
    client.init() #self explanatory
    client.ConnectToServer(host, int(port)) #connect to server with host and port
    client.SetEventHandler(EventHandler) #set the event handler to a function that will handle the messages it gets from the server
    client.StartReceiving() #start the receiver in a new thread so it doesnt block the main thread
    print(f"Connecting to server: {host} on port: {port}")

# Define a function for the second page
def second_page():
    # Define the "Server Host" text box
    server_host_rect = pygame.Rect(10, 100, 340, 60)  # x, y, width, height
    server_host_color = (255, 255, 255)  # White background for the text box
    server_host_border_color = (128, 128, 128)  # Gray border
    server_host_text = ""  # Text inside the text box
    server_host_active = False  # Whether the text box is active for input

    # Define the "Server Port" text box
    server_port_rect = pygame.Rect(10, 180, 340, 60)  # x, y, width, height
    server_port_color = (255, 255, 255)  # White background for the text box
    server_port_border_color = (128, 128, 128)  # Gray border
    server_port_text = ""  # Text inside the text box
    server_port_active = False  # Whether the text box is active for input

    # Define the "Connect" button
    connect_button_rect = pygame.Rect(400, 180, 210, 60)  # x, y, width, height
    connect_button_color = (0, 255, 0)  # Green color
    connect_button_hover_color = (0, 200, 0)  # Darker green for hover
    connect_button_text = "Connect"
    
    cancel_button_rect = pygame.Rect(400, 100, 210, 60)  # x, y, width, height
    cancel_button_color = (255, 0, 0)  # Green color
    cancel_button_hover_color = (200, 0, 0)  # Darker green for hover
    cancel_button_text = "cancel"

    second_page_running = True
    while second_page_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                second_page_running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                second_page_running = False  # Close the second page on Esc
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if server_host_rect.collidepoint(event.pos):  # Check if the "Server Host" text box is clicked
                    server_host_active = True
                    server_port_active = False
                elif server_port_rect.collidepoint(event.pos):  # Check if the "Server Port" text box is clicked
                    server_port_active = True
                    server_host_active = False
                elif cancel_button_rect.collidepoint(event.pos):  # Check if the "Cancel" button is clicked
                    client.CloseConnection()
                elif connect_button_rect.collidepoint(event.pos):  # Check if the "Connect" button is clicked
                    ConnectThread = threading.Thread(target=connect, args=(server_host_text, server_port_text))
                    ConnectThread.start()
                elif back_button_rect.collidepoint(event.pos):  # Check if the "Back" button is clicked
                    client.CloseConnection()
                    second_page_running = False  # Go back to the main page
                else:
                    server_host_active = False
                    server_port_active = False  # Deactivate both text boxes if clicked elsewhere
            elif event.type == pygame.KEYDOWN:
                if server_host_active:
                    if event.key == pygame.K_BACKSPACE:
                        server_host_text = server_host_text[:-1]  # Remove the last character
                    else:
                        server_host_text += event.unicode  # Add the typed character
                elif server_port_active:
                    if event.key == pygame.K_BACKSPACE:
                        server_port_text = server_port_text[:-1]  # Remove the last character
                    else:
                        server_port_text += event.unicode  # Add the typed character

        # Fill the screen with a different color for the second page
        window_surface.fill((0, 0, 0))  # Black background

        # Draw the "Back" button
        mouse_pos = pygame.mouse.get_pos()
        if back_button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(window_surface, back_button_hover_color, back_button_rect)  # Hover color
        else:
            pygame.draw.rect(window_surface, back_button_color, back_button_rect)  # Normal color

        # Draw the "Back" button text
        back_text_surface = font.render(back_button_text, True, (255, 255, 255))  # White text
        back_text_rect = back_text_surface.get_rect(center=back_button_rect.center)
        window_surface.blit(back_text_surface, back_text_rect)

        # Draw the "Server Host" text box
        pygame.draw.rect(window_surface, server_host_border_color, server_host_rect, 2)  # Border
        pygame.draw.rect(window_surface, server_host_color, server_host_rect.inflate(-4, -4))  # Inner box
        if server_host_text == "":
            placeholder_surface = font.render("Server Host (e.g. 127.0.0.1)", True, (128, 128, 128))  # Gray placeholder text
            placeholder_rect = placeholder_surface.get_rect(midleft=(server_host_rect.x + 10, server_host_rect.centery))
            window_surface.blit(placeholder_surface, placeholder_rect)
        else:
            server_host_text_surface = font.render(server_host_text, True, (0, 0, 0))  # Black text
            server_host_text_rect = server_host_text_surface.get_rect(midleft=(server_host_rect.x + 10, server_host_rect.centery))
            window_surface.blit(server_host_text_surface, server_host_text_rect)

        # Draw the "Server Port" text box
        pygame.draw.rect(window_surface, server_port_border_color, server_port_rect, 2)  # Border
        pygame.draw.rect(window_surface, server_port_color, server_port_rect.inflate(-4, -4))  # Inner box
        if server_port_text == "":
            placeholder_surface = font.render("Server Port (e.g. 4040, 8080)", True, (128, 128, 128))  # Gray placeholder text
            placeholder_rect = placeholder_surface.get_rect(midleft=(server_port_rect.x + 10, server_port_rect.centery))
            window_surface.blit(placeholder_surface, placeholder_rect)
        else:
            server_port_text_surface = font.render(server_port_text, True, (0, 0, 0))  # Black text
            server_port_text_rect = server_port_text_surface.get_rect(midleft=(server_port_rect.x + 10, server_port_rect.centery))
            window_surface.blit(server_port_text_surface, server_port_text_rect)

        # Draw the "Connect" button
        if connect_button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(window_surface, connect_button_hover_color, connect_button_rect)  # Hover color
        else:
            pygame.draw.rect(window_surface, connect_button_color, connect_button_rect)  # Normal color

        connect_button_text_surface = font.render(connect_button_text, True, (255, 255, 255))  # White text
        connect_button_text_rect = connect_button_text_surface.get_rect(center=connect_button_rect.center)
        window_surface.blit(connect_button_text_surface, connect_button_text_rect)

        if cancel_button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(window_surface, cancel_button_hover_color, cancel_button_rect)  # Hover color
        else:
            pygame.draw.rect(window_surface, cancel_button_color, cancel_button_rect)  # Normal color

        cancel_button_text_surface = font.render(cancel_button_text, True, (255, 255, 255))  # White text
        cancel_button_text_rect = cancel_button_text_surface.get_rect(center=cancel_button_rect.center)
        window_surface.blit(cancel_button_text_surface, cancel_button_text_rect)


        pygame.display.update()

is_running = True
while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
            client.CloseConnection()  # Close the connection when quitting
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):  # Check if the main button is clicked
                second_page()  # Open the second page

    # Fill the screen with white where there is no background
    window_surface.fill((255, 255, 255))  # White background

    # Draw the background (stick to the right)
    background_x = screen_width - 1024  # Align the background with the right edge
    window_surface.blit(background, (background_x, 0))

    # Draw the main button
    mouse_pos = pygame.mouse.get_pos()
    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(window_surface, button_hover_color, button_rect)  # Hover color
    else:
        pygame.draw.rect(window_surface, button_color, button_rect)  # Normal color

    # Draw the main button text
    button_text_surface = font.render(button_text, True, (255, 255, 255))  # White text
    button_text_rect = button_text_surface.get_rect(center=button_rect.center)
    window_surface.blit(button_text_surface, button_text_rect)

    # Draw additional buttons with unique colors
    for rect, text, color, hover_color in [
        (button2_rect, button2_text, button2_color, button2_hover_color),
        (button3_rect, button3_text, button3_color, button3_hover_color),
        (button4_rect, button4_text, button4_color, button4_hover_color),
        (button5_rect, button5_text, button5_color, button5_hover_color),
    ]:
        if rect.collidepoint(mouse_pos):
            pygame.draw.rect(window_surface, hover_color, rect)  # Hover color
        else:
            pygame.draw.rect(window_surface, color, rect)  # Normal color

        # Draw button text
        button_text_surface = font.render(text, True, (255, 255, 255))  # White text
        button_text_rect = button_text_surface.get_rect(center=rect.center)
        window_surface.blit(button_text_surface, button_text_rect)

    pygame.display.update()
