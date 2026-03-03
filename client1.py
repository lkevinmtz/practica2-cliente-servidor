import socket
import threading

def recibir_msg():
    respuesta = cliente.recv(1024)
    print(respuesta.decode())

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect(("127.0.0.1", 5000))

hilo = threading.Thread(target=recibir_msg, daemon=True)
hilo.start()

while True:

    mensaje = input(str("\nEscribe un mensaje: "))

    if mensaje.strip() == "":
        print("ERROR: No puedes ingresar una entrada vacia")
        continue

    cliente.send(mensaje.encode())