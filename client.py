import socket
import threading

<<<<<<< HEAD
# Función para recibir los mensajes de otros clientes
=======
# Hilo que se ejecuta de fondo para recibir mensajes
>>>>>>> 43e70cd (Logica terminada y comentada)
def recibir_msg():
    while True:
        try:
            mensaje = cliente.recv(1024).decode()
            if not mensaje:
                break
            print("\n" + mensaje)
        except:
            break

<<<<<<< HEAD
# Definición de Socket
=======
# Solicitar datos de conexión
username = input("Ingresa tu nombre de usuario: ")
host = input("Ingresa la dirección del servidor: ")
puerto = 5000

# Creacion del socket
>>>>>>> 43e70cd (Logica terminada y comentada)
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((host, puerto))

# Enviar username al servidor
cliente.send(username.encode())

# Definición de Hilo
hilo = threading.Thread(target=recibir_msg)
hilo.start()

# Bucle principal de envio de mensajes
while True:
    mensaje = input("Escribe un mensaje: ")

    # No se permiten mensajes vacíos
    if mensaje.strip() == "":
        print("ERROR: No puedes ingresar una entrada vacía")
        continue

    cliente.send(mensaje.encode())