import socket
import threading
import time
#hehe
global client_socket
client_socket = None

def init():
    global client_socket
    client_socket = socket.socket()
    client_socket.settimeout(60)

def ConnectToServer(RHOST, RPORT):
    global client_socket

    while True:
        try:
            client_socket.connect((RHOST, RPORT))
            break
        except:
            print("Connection failed, retrying in 1 seconds...")
            time.sleep(1)

def main():
    global client_socket

    #host = input("Enter the server's ip address:")
    #port = int(input("Enter the server's port:"))
    host = "localhost"
    port = 4040

    init()
    ConnectToServer(host, port)

    time.sleep(1)
    client_socket.send("[MESSAGE]hello[MESSAGE]".encode())
    client_socket.send("hello".encode())

main()
