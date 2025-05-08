import socket
import threading
import time

global server_socket
server_socket = None

global ClientsList
ClientsList = []

global MaxClients
MaxClients = None

global MessageTags
MessageTags = ["[MESSAGE]", "[REQUEST]"]

global ClientsInfo
ClientsInfo = []

global tiles
tiles = [[0 for _ in range(8)] for _ in range(5)]

global cost
cost = [[0, 0, 0], [0, 0, 0], [75, 0, 0]]

global running
running = False

class player:
	def __init__(self, currency, AvaiableCurrency):
		self.currency = currency
		self.AvaiableCurrency = AvaiableCurrency

def initFunctions():
	global ClientsList
	global ClientsInfo
	global tiles

	ClientsList = []
	ClientsInfo = []
	tiles = [[0 for _ in range(8)] for _ in range(5)]

def init(LHOST, LPORT):
	global server_socket
	global running
	initFunctions()
	running = True
	server_socket = socket.socket()
	server_socket.bind((LHOST, LPORT))

def listen(MaxClients):
	global server_socket
	server_socket.listen(MaxClients)

def RemoveClient(client):
	global ClientsList
	global ClientsInfo

	client.close()
	ClientsList.remove(client)
	try:
		ClientsInfo.remove(ClientsList.index(client))
	except:
		pass
	print(f"Client disconnected:{client}")

def TellAll(msg):
	global ClientsList

	for client in ClientsList:
		try:
			client.send(msg.encode())
		except Exception as e:
			print(f"Error while sending message:{e}")
			RemoveClient(client)

def AcceptConnections():
	global server_socket
	global ClientsInfo
	global ClientsList
	global MaxClients
	global running

	server_socket.settimeout(1)

	while not len(ClientsList) == MaxClients and running:
		try:
			conn, address = server_socket.accept()
		except:
			continue
		ClientsList.append(conn)
		ClientsInfo.append(player([0, 0, 0], [100, 0, 0]))
		if (len(ClientsList) == MaxClients):
			TellAll("[MESSAGE]SERVER FULL[MESSAGE]")
			break
		else:
			conn.send("[MESSAGE]WAITING FOR OTHER PLAYERS[MESSAGE]".encode())
		print(f"Client connected:{conn} | {address}")

def Receiver(client):
	global ClientsList
	global MessageTags
	global running
	UnFinishedMsg = None
	DeathCounter = 0

	while running:
		msg = None
		try:
			msg = client.recv(1024).decode()
		except Exception as e:
			print(f"Error while receiving:{e}")
			RemoveClient(client)
			break
		
		if msg == None: continue
		elif msg == "" and DeathCounter >= 10:
			RemoveClient(client)
			break
		elif msg == "" and DeathCounter < 10:
			DeathCounter += 1
			continue

		if UnFinishedMsg != None:
			msg += UnFinishedMsg

		if any(msg.startswith(tag) and msg.endswith(tag) for tag in MessageTags):
			print(f"VALID MESSAGE:{msg} RESPONDING")
			ClientMessageHandler(client, msg)
			UnFinishedMsg = None
		elif any(msg.startswith(tag) for tag in MessageTags):
			print("INVALID MESSAGE SAVES TO UNFINISHEDMSG")
			UnFinishedMsg = msg
		else:
			print("INVALID MESSAGE")

		DeathCounter = 0

def ClientMessageHandler(client, msg):
	global ClientsList
	global ClientsInfo
	global tiles

	if (msg == "[MESSAGE]PleaseRespond[MESSAGE]"):
		client.send("[MESSAGE]ok[MESSAGE]".encode())
		print("responded to client")
	elif ("collect" in msg): #[REQUEST]collect|index(int)|amount(int)[REQUEST]
		try:
			msg = msg.replace("[REQUEST]", "").split("|")
			index = int(msg[1])
			amount = int(msg[2])
		except:
			client.send("[RESPONSE]ERR:FORMAT ERROR[RESPONSE]".encode())
			return
		PlayerInfo = ClientsInfo[ClientsList.index(client)]
		if (PlayerInfo.AvaiableCurrency[index] >= amount):
			PlayerInfo.AvaiableCurrency[index] -= amount
			PlayerInfo.currency[index] += amount
			client.send("[RESPONSE]OK:COLLECTED[RESPONSE]".encode())
			print(f"Currect client info: {PlayerInfo.currency} | {PlayerInfo.AvaiableCurrency}")
		else:
			client.send("[RESPONSE]ERR:MISMATCH INFO WITH SERVER[RESPONSE]".encode())
	elif ("select" in msg): # [REQUEST]select|index|index|type[REQUEST] (1=salt, 2=Bolonez)
		try:
			msg = msg.replace("[REQUEST]", "").split("|")
			index = int(msg[1])
			index2 = int(msg[2])
			type = int(msg[3])
		except:
			client.send("[RESPONSE]ERR:FORMAT ERROR[RESPONSE]".encode())
			return
		
		PlayerInfo = ClientsInfo[ClientsList.index(client)]
		if all(PlayerInfo.currency[i] >= cost[type][i] for i in range(len(cost[type]))):
			for i in range(len(cost[type])):
				PlayerInfo.currency[i] -= cost[type][i]
			tiles[index][index2] = 1
			client.send("[RESPONSE]OK:SELECTED[RESPONSE]".encode())
			print(f"Selected tile: {index} | {index2}\ntiles:{tiles}\nPlayerInfo: {PlayerInfo.currency}")
		else:
			print("Mismatch info with server")
			client.send("[RESPONSE]ERR:MISMATCH INFO WITH SERVER[RESPONSE]".encode())
	else:
		client.send("[RESPONSE]ERR:FORMAT ERROR[RESPONSE]".encode())

def StartReceiving():
	global ClientsList

	while IsAllReady() == False:
		time.sleep(0.1)
		if not running:
			return

	for client in ClientsList:
		thread = threading.Thread(target=Receiver, args=(client,))
		thread.start()

def SetMaxClients(num):
	global MaxClients
	MaxClients = num

def IsAllReady():
	global ClientsList
	global MaxClients

	if len(ClientsList) == MaxClients:
		return True
	else:
		return False
	
def StopServer():
	global server_socket
	global ClientsList
	global running
	running = False

	for client in ClientsList:
		client.close()
	server_socket.close()
	print("Server stopped.")
#MaxClients = 2
# def main():
# 	global server_socket
# 	global ClientsList
# 	global MaxClients

# 	host = "0.0.0.0"
# 	#port = int(input("Enter port to host on:"))
# 	port = 4040

# 	MaxClients = 1

# 	init(host, port)
# 	listen(MaxClients)
# 	AcceptConnections()
	
# 	StartReceiving()
# main()
