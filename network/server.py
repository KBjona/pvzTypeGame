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
tiles = [[0 for _ in range(9)] for _ in range(5)]

global cost
cost = [[0, 0, 0], [50, 0, 0], [100, 0, 0], [50, 0, 0], [100, 0, 0], [150, 0, 0]] #0, salt, bolonez, moshe, shlomi, josh

global running
running = False

global ConsoleWriter
ConsoleWriter = None

global SaltTime
SaltTime = 0

global SaltTimes
SaltTimes = []

class player:
	def __init__(self, currency):
		self.currency = currency

def initFunctions():
	global ClientsList
	global ClientsInfo
	global tiles

	ClientsList = []
	ClientsInfo = []
	tiles = [[0 for _ in range(9)] for _ in range(5)]

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

	num = ClientsList.index(client)

	client.close()
	ClientsList.remove(client)
	try:
		ClientsInfo.remove(ClientsList.index(client))
	except:
		pass
	ConsoleWriter(f"Client({num}) disconnected:{client}")

def TellAll(msg):
	global ClientsList

	for client in ClientsList:
		try:
			client.send(msg.encode())
		except Exception as e:
			ConsoleWriter(f"Error while sending message:{e}")
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
			ConsoleWriter(f"Client connected({len(ClientsList)}):{conn} | {address}")
		except:
			continue
		ClientsList.append(conn)
		ClientsInfo.append(player([100, 0, 0]))
		if (len(ClientsList) == MaxClients):
			TellAll("[MESSAGE]SERVER FULL[MESSAGE]")
			break
		else:
			conn.send("[MESSAGE]WAITING FOR OTHER PLAYERS[MESSAGE]".encode())

def Receiver(client):
	global ClientsList
	global MessageTags
	global running
	global server_socket
	UnFinishedMsg = None
	DeathCounter = 0

	server_socket.settimeout(1)

	while running:
		msg = None
		try:
			msg = client.recv(1024).decode()
		except Exception as e:
			ConsoleWriter(f"Error while receiving:{e}")
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
			ConsoleWriter(f"VALID MESSAGE CLIENT({ClientsList.index(client)}):{msg} RESPONDING")
			ClientMessageHandler(client, msg)
			UnFinishedMsg = None
		elif any(msg.startswith(tag) for tag in MessageTags):
			ConsoleWriter("INVALID MESSAGE SAVES TO UNFINISHEDMSG")
			UnFinishedMsg = msg
		else:
			ConsoleWriter("INVALID MESSAGE")

		DeathCounter = 0

def ClientMessageHandler(client, msg):
	global ClientsList
	global ClientsInfo
	global tiles
	global SaltTimes
	global SaltTime

	if (msg == "[MESSAGE]PleaseRespond[MESSAGE]"):
		if ClientsList.index(client) == 0:
			mode = "defender"
		else:
			mode = "attacker"
		client.send(f"[MESSAGE]{mode}[MESSAGE]".encode())
		ConsoleWriter(f"responded to client({ClientsList.index(client)})")
	elif ("select" in msg): # [REQUEST]select|index|index|type[REQUEST] (1=salt, 2=Bolonez, 3=pepper)
		try:
			msg = msg.replace("[REQUEST]", "").split("|")
			index = int(msg[1])
			index2 = int(msg[2])
			type = int(msg[3])
		except:
			client.send("[RESPONSE]ERR:FORMAT ERROR[RESPONSE]".encode())
			return
		
		if type in [0, 1, 2] and not ClientsList.index(client) == 0:
			client.send("[RESPONSE]ERR:FORMAT ERROR[RESPONSE]".encode())
			return
		elif type in [3, 4, 5] and not ClientsList.index(client) == 1:
			client.send("[RESPONSE]ERR:FORMAT ERROR[RESPONSE]".encode())
			return

		PlayerInfo = ClientsInfo[ClientsList.index(client)]
		if all(PlayerInfo.currency[i] >= cost[type][i] for i in range(len(cost[type]))):
			for i in range(len(cost[type])):
				PlayerInfo.currency[i] -= cost[type][i]
			tiles[index][index2] = type
			if type == 1:
				SaltTimes.append(f"{SaltTime}|{index}|{index2}")
				ConsoleWriter(str(SaltTimes))
			client.send("[RESPONSE]OK:SELECTED[RESPONSE]".encode())
			ConsoleWriter(f"Selected tile: {index} | {index2}\ntiles:{tiles}\nPlayerInfo: {PlayerInfo.currency}")
			if ClientsList.index(client) == 0:
				ClientsList[1].send(f"[REQUEST]select|{index}|{index2}|{type}[REQUEST]".encode())
			else:
				ClientsList[0].send(f"[REQUEST]select|{index}|{index2}|{type}[REQUEST]".encode())
		else:
			ConsoleWriter(f"Client{ClientsList.index(client)}:Mismatch info with server")
			client.send("[RESPONSE]ERR:MISMATCH INFO WITH SERVER[RESPONSE]".encode())
	elif ("damage" in msg):
		if ClientsList.index(client) == 0:
			try:
				msg = msg.replace("[REQUEST]", "").split("|")
				id = int(msg[1])
				amount = int(msg[2])
			except:
				client.send("[RESPONSE]ERR:FORMAT ERROR[RESPONSE]".encode())
			return
		
			#damage logic here
		else:
			try:
				msg = msg.replace("[REQUEST]", "").split("|")
				index = int(msg[1])
				index2 = int(msg[2])
				amount = int(msg[3])
			except:
				client.send("[RESPONSE]ERR:FORMAT ERROR[RESPONSE]".encode())
			return
		
			#damage logic here
	else:
		client.send("[RESPONSE]ERR:FORMAT ERROR[RESPONSE]".encode())

def BrainsManager():
	global ClientsList
	global ClientsInfo
	global running

	attacker = ClientsList[1]
	AttackerInfo = ClientsInfo[1]

	brains = 75
	time.sleep(15)
	while running:
		time.sleep(5)
		AttackerInfo.currency[0] += brains
		try:
			attacker.send(f"[REQUEST]ADD|0|{brains}[REQUEST]".encode()) #Add currency request syntax: ADD|type|amount (0=salt, 1=pepper)
		except Exception as e:
			ConsoleWriter(f"Error while sending message:{e}")
			RemoveClient(attacker)
			break

def SaltManager():
	global ClientsList
	global ClientsInfo
	global running
	global SaltTimes
	global SaltTime

	defender = ClientsList[0]
	DefenderInfo = ClientsInfo[0]

	while running:
		time.sleep(0.01)
		SaltTime += 1
		if SaltTime >= 500:
			SaltTime = 0
		salt = 0
		for i in SaltTimes:
			i = i.split("|")[0]
			if int(i) == SaltTime:
				salt += 50
		if salt <= 0:
			continue
		DefenderInfo.currency[0] += salt
		try:
			defender.send(f"[REQUEST]ADD|0|{salt}[REQUEST]".encode()) #Add currency request syntax: ADD|type|amount (0=salt, 1=pepper)
		except Exception as e:
			ConsoleWriter(f"Error while sending message:{e}")
			RemoveClient(defender)
			break

def StartReceivingAndSending():
	global ClientsList

	while IsAllReady() == False:
		time.sleep(0.1)
		if not running:
			return

	SaltThread = threading.Thread(target=SaltManager)
	SaltThread.start()

	BrainThread = threading.Thread(target=BrainsManager)
	BrainThread.start()

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
		RemoveClient(client)
	server_socket.close()
	ConsoleWriter("Server stopped.")

def GetTiles():
	global tiles
	return tiles

def SetConsoleWriter(func):
    global ConsoleWriter

    if not callable(func):
        raise ValueError("The first argument must be a callable (function).")
    ConsoleWriter = func
