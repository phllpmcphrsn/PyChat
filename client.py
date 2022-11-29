import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(("localhost", 9999))

try:
    while True:
        client.send(input("You: ").encode('utf-8'))
        msg = client.recv(1024).decode('utf-8')

        if msg == "quit":
            break
        else:
            print("Server:", msg)
finally:
    client.close()