import socket

PORT = 8080
IP = "127.0.0.1"
MAX_OPEN_REQUESTS = 50

counter = 0

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    serversocket.bind((IP, PORT))
    serversocket.listen(MAX_OPEN_REQUESTS)
    while True:
        print("Waiting for connections at {}, {}".format(IP, PORT))
        (clientsocket, address) = serversocket.accept()

        counter += 1

        print("Connection: {}. From the IP: {}".format(counter, address))

        msg = clientsocket.recv(2048)
        print("Message from client: ", end="")
        print(msg.decode("utf-8"))

        message = "Hello!"
        send_bytes = str.encode(message)
        clientsocket.send(send_bytes)

        clientsocket.close()

except socket.error:
    print("Problems using the port {}.".format(PORT))

except KeyboardInterrupt:
    print("Server stopped by the user")
    serversocket.close()
