import client as client
import time

host = "localhost"
port = 4040

def EventHandler(msg):
    print(f"EventHandler:{msg}")

client.init()
client.ConnectToServer(host, port)
client.SetEventHandler(EventHandler)
client.StartReceiving()

time.sleep(1)
client.client_socket.send("[REQUEST]collect|0|50[REQUEST]".encode())