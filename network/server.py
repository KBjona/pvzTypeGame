import socket
import threading

global server_socket
server_socket = None

global ClientsList
ClientsList = []

global MaxClients
MaxClients = None

global MessageTags
MessageTags = ["[MESSAGE]"]

global ClientsInfo
ClientsInfo = []

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

def AcceptConnections():
	global server_socket
	global ClientsInfo

	for i in range(1):
		conn, address = server_socket.accept()
		ClientsList.append(conn)
		ClientsInfo.append(player([0, 0, 0], [0, 0, 0]))
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
			client.close()
			ClientsList.remove(client)
			print(f"Client disconnected:{client}")
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
	if (msg == "[MESSAGE]PleaseRespond[MESSAGE]"):
		client.send("[MESSAGE]ok[MESSAGE]".encode())
		print("responded to client")

def main():
	global server_socket
	global ClientsList

	host = "0.0.0.0"
	#port = int(input("Enter port to host on:"))
	port = 4040

	init(host, port)
	listen(2)
	AcceptConnections()
	
	for client in ClientsList:
		thread = threading.Thread(target=Receiver, args=(client,))
		thread.start()

main()