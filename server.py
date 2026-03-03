import socket
import threading

def broadcast(cliente, direccion):
    print(f"{direccion} se ha conectado")

    while True:
        mensaje = cliente.recv(1024).decode()
        print(f"{[direccion]} dice: {mensaje}")
        mensajes.append(mensaje)

        for cliente in clientes:
            cliente.send(f"{direccion} dice: {mensaje}".encode())

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind(("127.0.0.1", 5000))
servidor.listen()
print("Servidor esperando conexion")

mensajes = []
clientes = []

while True:
    cliente, direccion = servidor.accept()
    clientes.append(cliente)
    hilo = threading.Thread(target=broadcast, args=(cliente, direccion), daemon=True)
    hilo.start()