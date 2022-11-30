import socket
import sys
import threading
import logging as log

# config values
HEADER = 64   # bytes
PORT = 9090
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'

# Define an internet (AF_INET) socket with TCP, STREAM connection
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    '''Runs concurrently for each client'''
    log.info('[NEW CONNECTION] %s connected', addr)
    
    connected = True
    while connected:
        try:
            # Blocks until message is received over the socket
            # The allowed length (in bytes) of the message is determined
            # by you. We use a header to gather how large the message followed
            # by the actual message
            msg_length = conn.recv(HEADER).decode(FORMAT)
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False

            log.info(f'[{addr}] {msg}')
        finally:
            conn.close()

def start():
    server.listen()
    log.info(f'[LISTENING] Server now listening on %s', SERVER)
    while True:
        try:
            # This will block until a connection is accepted
            conn, addr = server.accept()

            # target = function to thread; args = args to pass to function to be threaded
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
            
            # -1 to account for the start() thread
            log.debug(f'[ACTIVE CONNECTIONS] %d', {threading.activeCount() - 1})
        except KeyboardInterrupt:
            # Capture abrupt closed connections like Ctrl-C
            # Send message notifying of closed server
            msg = 'Server closed. Goodbye for now!'
            conn.send(msg.encode('utf-8'))
            sys.exit(0)
        finally:
            conn.close()
            server.close()

def main():
    # should place this logging into a class for more global use
    streamHandler = log.StreamHandler()
    streamHandler.setStream(sys.stdout)
    fileHandler = log.FileHandler('logs/server.log')
    log.basicConfig(format='%(levelname)s:%(asctime)s :: %(message)s', handlers=[streamHandler, fileHandler], level=log.INFO, datefmt='%m/%d/%Y %I:%M:%S %p')

    log.info('[STARTING] Server is starting...')
    start()

if __name__ == '__main__':
    main()
# try:
#     while True:
#         try:
#             msg = client.recv(1024).decode('utf-8')
#             if msg == 'quit':
#                 break
#             else:
#                 print('Client:', msg)
#             client.send(input('Message: ').encode('utf-8'))
#         except KeyboardInterrupt:
#             # Capture abrupt closed connections like Ctrl-C
#             # Send message notifying of closed server
#             msg = 'Server closed. Goodbye for now!'
#             client.send(msg.encode('utf-8'))
#             sys.exit(0)
# finally:
#     client.close()
#     server.close()