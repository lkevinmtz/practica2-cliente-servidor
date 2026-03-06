import socket
import threading

# Función para reenviar un mensaje recibido de parte de un cliente al resto de clientes
def broadcast(mensaje, emisor=None):
    for cliente in clientes:
        if cliente != emisor:
            try:
                cliente.send(mensaje.encode())
            except:
                clientes.remove(cliente)

# Recibir clientes nuevos
def manejar_cliente(cliente, direccion):
    print(f"{direccion} se ha conectado")

    # Enviar mensaje y hacer un salto de línea
    with lock:
        for msg in mensajes:
            cliente.send((msg + "\n").encode())

    # Loop para recibir mensajes y llamar a la función de broadcast
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

    # Manejar desconexión de cliente
    print(f"{direccion} se ha desconectado")
    clientes.remove(cliente)
    cliente.close()

# Creación de Listas y Lock
clientes = []
mensajes = []
lock = threading.Lock()

# Creación de Socket y empezar la escucha de clientes
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind(("127.0.0.1", 5000))
servidor.listen()

print("Servidor esperando conexión...")

# Loop para aceptar clientes y crear hilos para ellos
while True:
    cliente, direccion = servidor.accept()
    clientes.append(cliente)
    hilo = threading.Thread(target=manejar_cliente, args=(cliente, direccion))
    hilo.start()