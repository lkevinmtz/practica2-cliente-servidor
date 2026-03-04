import socket
import threading

def broadcast(mensaje, emisor=None):
    for cliente in clientes:
        if cliente != emisor:
            try:
                cliente.send(mensaje.encode())
            except:
                clientes.remove(cliente)

def manejar_cliente(cliente, direccion):
    print(f"{direccion} se ha conectado")

    with lock:
        for msg in mensajes:
            cliente.send((msg + "\n").encode())

    while True:
        try:
            mensaje = cliente.recv(1024).decode()
            if not mensaje:
                break

            msg_broadcast = f"{direccion} dice: {mensaje}"
            print(msg_broadcast)

            with lock:
                mensajes.append(msg_broadcast)
                if len(mensajes) > 20:
                    mensajes.pop(0)

            broadcast(msg_broadcast, cliente)

        except:
            break

    print(f"{direccion} se ha desconectado")
    clientes.remove(cliente)
    cliente.close()

clientes = []
mensajes = []
lock = threading.Lock()

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind(("127.0.0.1", 5000))
servidor.listen()

print("Servidor esperando conexión...")

while True:
    cliente, direccion = servidor.accept()
    clientes.append(cliente)
    hilo = threading.Thread(target=manejar_cliente, args=(cliente, direccion))
    hilo.start()