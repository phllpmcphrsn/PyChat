import socket
import sys

# Define an internet (AF_INET) socket with TCP, STREAM connection
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost",9999))
server.listen()
print("Server now listening")

# This will block until a connection is accepted
client, addr = server.accept()
print("Client connected to", addr[0],':',addr[1])

try:
    while True:
        try:
            msg = client.recv(1024).decode('utf-8')
            if msg == 'quit':
                break
            else:
                print("Client:", msg)
            client.send(input("Message: ").encode('utf-8'))
        except KeyboardInterrupt:
            # Capture abrupt closed connections like Ctrl-C
            # Send message notifying of closed server
            msg = "Server closed. Goodbye for now!"
            client.send(msg.encode('utf-8'))
            sys.exit(0)
finally:
    client.close()
    server.close()