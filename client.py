import socket

HEADER = 64   # bytes
PORT = 9090
SERVER = '192.168.1.210'
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(ADDR)

# try:
#     while True:
#         client.send(input("You: ").encode('utf-8'))
#         msg = client.recv(1024).decode('utf-8')

#         if msg == "quit":
#             break
#         else:
#             print("Server:", msg)
# finally:
#     client.close()