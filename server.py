import socket
import threading

# Función que reenvia los mensajes a los clientes mediante broadcast
def broadcast(mensaje, emisor=None):
    for cliente in clientes:
        try:
            cliente.send(mensaje.encode())
        except:
            clientes.remove(cliente)

def enviar_lista_usuarios():
    lista = "USERS:" + ",".join(usuarios_conectados)
    for cliente in clientes:
        try:
            cliente.send((lista + "\n").encode())
        except:
            pass

# Función que representa al cliente como hilo en el servidor
def manejar_cliente(cliente, direccion):

    # Servidor recibe username
    try:
        username = cliente.recv(1024).decode()
    except:
        cliente.close()
        return
    
    # Username del cliente se almacena como usuario activo
    usuarios[cliente] = username
    usuarios_conectados.append(username)
    enviar_lista_usuarios()

    print(f"{username} se ha conectado desde {direccion}")

    # Envío de los 20 mensajes más recientes
    with lock:
        for msg in mensajes:
            cliente.send((msg + "\n").encode())

    broadcast(f"{username} se ha unido al chat")

    # Bucle principal del cliente en el servidor
    while True:
        try:
            # Recepción del mensaje del cliente
            mensaje = cliente.recv(1024).decode()

            if not mensaje:
                break

            msg_broadcast = f"{username}: {mensaje}"
            print(msg_broadcast)

            # Control de la lista de 20 mensajes más recientes
            with lock:
                mensajes.append(msg_broadcast)
                if len(mensajes) > 20:
                    mensajes.pop(0)

            # Llamado de la función broadcast
            broadcast(msg_broadcast, cliente)

        except:
            break # Excepción para que en caso de desconexion, se controlen los errores generados

    print(f"{username} se ha desconectado")
    
    # Eliminación del hilo cliente y de su entrada de usuario
    broadcast(f"{username} ha salido del chat")

    clientes.remove(cliente)
    usuarios_conectados.remove(username)
    del usuarios[cliente]
    enviar_lista_usuarios()

    cliente.close()

clientes = [] # Hilos cliente
usuarios = {} # Relación socket/usuario
usuarios_conectados = [] # Solo nombre de usuario
mensajes = [] # Mensajes recientes

lock = threading.Lock()

# Creación del socket
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind(("0.0.0.0", 5000))
servidor.listen()

print("Servidor esperando conexión...")

# Bucle principal del servidor recibe y maneja los clientes
while True:
    cliente, direccion = servidor.accept()

    clientes.append(cliente)

    hilo = threading.Thread(target=manejar_cliente, args=(cliente, direccion))
    hilo.start()