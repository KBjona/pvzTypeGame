import client as client
import time

host = "localhost"
port = 4040

def EventHandler(msg):
    print(f"EventHandler:{msg}")

client.init() #self explanatory
client.ConnectToServer(host, port) #connect to server with host and port
client.SetEventHandler(EventHandler) #set the event handler to a function that will handle the messages it gets from the server
client.StartReceiving() #start the receiver in a new thread so it doesnt block the main thread

time.sleep(1)
client.client_socket.send("[REQUEST]collect|0|50[REQUEST]".encode()) #request to collect currency syntax: collect|Which currency(0-2)|how much