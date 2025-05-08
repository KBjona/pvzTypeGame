import network.server as server
import tkinter as tk
from tkinter import scrolledtext
import threading

def WriteToConsole(message):
    ConsoleText.config(state=tk.NORMAL)
    ConsoleText.insert(tk.END, message + "\n")
    ConsoleText.config(state=tk.DISABLED)
    ConsoleText.see(tk.END)

def StartOrStopServer():
    if StartBtnText.get() == "Start":
        port = PortEntry.get()
        if not port.isdigit():
            WriteToConsole("Port must be a number.")
            StartBtnText.set("Start")
            return
        StartBtnText.set("Stop")
        WriteToConsole(f"Starting server on local port {port}...")
        server.init("0.0.0.0", int(port))
        WriteToConsole("Server initialized. Listening for clients...")
        server.listen(2)
        WriteToConsole("Starting receiver thread...\nWaiting for players...")
        AcceptThread = threading.Thread(target=server.AcceptConnections)
        AcceptThread.start()
        ReceiverThread = threading.Thread(target=server.StartReceiving)
        ReceiverThread.start()
    else:
        server.StopServer()
        WriteToConsole("Stopping server...")
        StartBtnText.set("Start")

server.SetMaxClients(2)

width = 800
height = 400

root = tk.Tk()
root.title("Server GUI")
root.geometry(f"{width}x{height}")

PortLabel = tk.Label(root, text="Local Port:")
PortLabel.pack(pady=5)

PortEntry = tk.Entry(root)
PortEntry.pack(pady=5)

StartBtnText = tk.StringVar()
StartBtnText.set("Start")

StartButton = tk.Button(root, textvariable=StartBtnText, command=StartOrStopServer)
StartButton.pack(pady=5)

ConsoleText = scrolledtext.ScrolledText(root, state=tk.DISABLED, height=15, width=50)
ConsoleText.pack(side=tk.BOTTOM, anchor="w", padx=10, pady=10)

root.mainloop()