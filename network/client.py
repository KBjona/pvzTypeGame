import socket
import threading
import time

global client_socket
client_socket = None

global EventHandler
EventHandler = None

global MessageTags
MessageTags = ["[MESSAGE]", "[RESPONSE]"]

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

def Receiver():
    global client_socket
    global MessageTags
    global EventHandler
    UnFinishedMsg = None
    DeathCounter = 0

    while True:
        msg = None
        try:
            msg = client_socket.recv(1024).decode()
        except Exception as e:
            print(f"Error while receiving:{e}")
            break
		
        if msg == None: continue
        elif msg == "" and DeathCounter >= 10:
            client_socket.close()
            print(f"Disconnected from server")
            break
        elif msg == "" and DeathCounter < 10:
            DeathCounter += 1
            continue

        if UnFinishedMsg != None:
            msg += UnFinishedMsg

        if any(msg.startswith(tag) and msg.endswith(tag) for tag in MessageTags):
            print(f"VALID MESSAGE:{msg}\n EXECUTING EVENT HANDLER")
            if EventHandler != None:
                EventHandler(msg)
            else:
                print("No event handler set, ignoring.")
            UnFinishedMsg = None
        elif any(msg.startswith(tag) for tag in MessageTags):
            print("INVALID MESSAGE SAVES TO UNFINISHEDMSG")
            UnFinishedMsg = msg
        else:
            print("INVALID MESSAGE")

        DeathCounter = 0

def SetEventHandler(func):
    global EventHandler

    if not callable(func):
        raise ValueError("The first argument must be a callable (function).")
    EventHandler = func

def StartReceiving():
    ReceiverThread = threading.Thread(target=Receiver)
    ReceiverThread.start()

def CloseConnection():
    global client_socket

    if client_socket != None:
        client_socket.close()
        print("Connection closed.")
    else:
        print("No connection to close.")

def send(msg):
    global client_socket
    
    if msg == None: return
    elif msg == "":
        print("Message is empty, ignoring.")
        return
    
    try:
        client_socket.send(msg.encode())
    except Exception as e:
        print(f"Error while sending:{e}")
        client_socket.close()
        print("Closed connection.")