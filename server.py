import socket
import threading

def broadcast(cliente, mensaje, h_broadcast):
    for cliente in clientes:
            cliente.send(f"{direccion} dice: {mensaje}".encode())
    h_broadcast.close()


def recibir_mensaje(cliente, direccion):
    print(f"{direccion} se ha conectado")

    while True:
        mensaje = cliente.recv(1024).decode()
        print(f"{[direccion]} dice: {mensaje}")
        mensajes.append(mensaje)

        if mensaje != mensajes[-1]:
            h_broadcast = threading.Thread(target=broadcast, args=(cliente, mensaje, h_broadcast))
            h_broadcast.start()

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind(("127.0.0.1", 5000))
servidor.listen()
print("Servidor esperando conexion")

mensajes = []
clientes = []

while True:
    cliente, direccion = servidor.accept()
    clientes.append(cliente)
    hilo = threading.Thread(target=recibir_mensaje, args=(cliente, direccion), daemon=True)
    hilo.start()