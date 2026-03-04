import socket

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect(("127.0.0.1", 5000))

while True:
    respuesta = cliente.recv(1024)
    print(respuesta.decode())