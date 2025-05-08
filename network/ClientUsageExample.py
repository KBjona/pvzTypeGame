import client as client
import time

host = "localhost"
port = 4040

global AllPlayersReady
AllPlayersReady = False

def EventHandler(msg):
    global AllPlayersReady
    
    print(f"EventHandler:{msg}")
    if msg == "[MESSAGE]SERVER FULL[MESSAGE]":
        AllPlayersReady = True
        print("All players are ready")

client.init() #self explanatory
client.ConnectToServer(host, port) #connect to server with host and port
client.SetEventHandler(EventHandler) #set the event handler to a function that will handle the messages it gets from the server
client.StartReceiving() #start the receiver in a new thread so it doesnt block the main thread

while AllPlayersReady == False:
    time.sleep(1)

time.sleep(1)
client.client_socket.send("[REQUEST]collect|0|50[REQUEST]".encode()) #request to collect currency syntax: collect|Which currency(0-2)|how much
time.sleep(1)
client.client_socket.send("[REQUEST]select|0|3|1[REQUEST]".encode()) #request to select a tile syntax: select|index|index

client.CloseConnection() #close the connection to the server
