import socket
import threading

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

class player:
	def __init__(self, currency, AvaiableCurrency):
		self.currency = currency
		self.AvaiableCurrency = AvaiableCurrency

def init(LHOST, LPORT):
	global server_socket
	server_socket = socket.socket()
	server_socket.bind((LHOST, LPORT))
	server_socket.settimeout(60)

def listen(MaxClients):
	global server_socket
	server_socket.listen(MaxClients)

def RemoveClient(client):
	global ClientsList
	global ClientsInfo

	client.close()
	ClientsList.remove(client)
	ClientsInfo.remove(ClientsList.index(client))
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
	global MaxClients

	for i in range(MaxClients):
		conn, address = server_socket.accept()
		ClientsList.append(conn)
		ClientsInfo.append(player([0, 0, 0], [100, 0, 0]))
		if (i == MaxClients - 1):
			TellAll("[MESSAGE]SERVER FULL[MESSAGE]")
		else:
			conn.send("[MESSAGE]WAITING FOR OTHER PLAYERS[MESSAGE]".encode())
		print(f"Client connected:{conn} | {address}")

def Receiver(client):
	global ClientsList
	global MessageTags
	UnFinishedMsg = None
	DeathCounter = 0

	while True:
		msg = None
		try:
			msg = client.recv(1024).decode()
		except Exception as e:
			print(f"Error while receiving:{e}")
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
		msg = msg.replace("[REQUEST]", "").split("|")
		index = int(msg[1])
		amount = int(msg[2])
		PlayerInfo = ClientsInfo[ClientsList.index(client)]
		if (PlayerInfo.AvaiableCurrency[index] >= amount):
			PlayerInfo.AvaiableCurrency[index] -= amount
			PlayerInfo.currency[index] += amount
			client.send("[RESPONSE]OK:COLLECTED[RESPONSE]".encode())
			print(f"Currect client info: {PlayerInfo.currency} | {PlayerInfo.AvaiableCurrency}")
		else:
			client.send("[RESPONSE]ERR:MISMATCH INFO WITH SERVER[RESPONSE]".encode())
	elif ("select" in msg): # [REQUEST]select|index|index[REQUEST]
		msg = msg.replace("[REQUEST]", "").split("|")
		index = int(msg[1])
		index2 = int(msg[2])
		#VALIDATION CODE HERE
		if (True):
			tiles[index][index2] = 1
			client.send("[RESPONSE]OK:SELECTED[RESPONSE]".encode())
			print(f"Selected tile: {index} | {index2}")
		else:
			client.send("[RESPONSE]ERR:MISMATCH INFO WITH SERVER[RESPONSE]".encode())


def main():
	global server_socket
	global ClientsList
	global MaxClients

	host = "0.0.0.0"
	#port = int(input("Enter port to host on:"))
	port = 4040

	MaxClients = 2

	init(host, port)
	listen(MaxClients)
	AcceptConnections()
	
	for client in ClientsList:
		thread = threading.Thread(target=Receiver, args=(client,))
		thread.start()

main()