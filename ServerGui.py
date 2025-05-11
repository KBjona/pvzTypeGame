import network.server as server
import tkinter as tk
from tkinter import scrolledtext
import threading
import time

global UpdateTiles
UpdateTiles = False

TileImages = {}

def LoadImages():
    global TileImages

    images = {
        1: tk.PhotoImage(file="images/salt shaker .png"),
        2: tk.PhotoImage(file="images/sap.png")
    }

    scale = 100 / 10

    for key, img in images.items():
        TileImages[key] = img.subsample(int(scale), int(scale))

def WriteToConsole(message):
    ConsoleText.config(state=tk.NORMAL)
    ConsoleText.insert(tk.END, message + "\n")
    ConsoleText.config(state=tk.DISABLED)
    ConsoleText.see(tk.END)

def StartOrStopServer():
    global GridCanvas
    global UpdateTiles

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
        ReceiverAndSenderThread = threading.Thread(target=server.StartReceivingAndSending)
        ReceiverAndSenderThread.start()
        UpdateTiles = True
        UpdateGameTilesThread = threading.Thread(target=UpdateGameTiles)
        UpdateGameTilesThread.start()
    else:
        server.StopServer()
        UpdateTiles = False
        GridCanvas.delete("all")
        StartBtnText.set("Start")

def DrawGameInMini(TilesData=[[0 for _ in range(9)] for _ in range(5)]):
    global GridCanvas
    global TileImages

    GridCanvas.delete("all")

    CellWidth = 50
    CellHeight = 50
    for row in range(len(TilesData)):
        for col in range(len(TilesData[row])):
            x1 = col * CellWidth
            y1 = row * CellHeight
            x2 = x1 + CellWidth
            y2 = y1 + CellHeight

            GridCanvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="#d9d9d9")

            if TilesData[row][col] != 0 and TilesData[row][col] in TileImages:
                GridCanvas.create_image(
                    x1 + CellWidth // 2,
                    y1 + CellHeight // 2,
                    image=TileImages[TilesData[row][col]]
                )

def UpdateGameTiles():
    global UpdateTiles

    while UpdateTiles:
        DrawGameInMini(server.GetTiles())
        time.sleep(1)

server.SetConsoleWriter(WriteToConsole)

server.SetMaxClients(2)

width = 910
height = 400

root = tk.Tk()
root.title("Server GUI")
root.geometry(f"{width}x{height}")
root.resizable(False, False)

PortLabel = tk.Label(root, text="Local Port:")
PortLabel.pack(pady=5)

PortEntry = tk.Entry(root)
PortEntry.pack(pady=5)

StartBtnText = tk.StringVar()
StartBtnText.set("Start")

StartButton = tk.Button(root, textvariable=StartBtnText, command=StartOrStopServer)
StartButton.pack(pady=5)

BottomFrame = tk.Frame(root)
BottomFrame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

ConsoleText = scrolledtext.ScrolledText(BottomFrame, state=tk.DISABLED, height=15, width=50)
ConsoleText.pack(side=tk.LEFT, padx=(0, 10))

GridCanvas = tk.Canvas(BottomFrame, width=450, height=250, bg="#d9d9d9")
GridCanvas.pack(side=tk.RIGHT)

LoadImages()

DrawGameInMini()

root.mainloop()