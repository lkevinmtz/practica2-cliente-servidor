import socket
import threading

def recibir_msg():
    while True:
        try:
            mensaje = cliente.recv(1024).decode()
            if not mensaje:
                break
            print("\n" + mensaje)
        except:
            break

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect(("127.0.0.1", 5000))

hilo = threading.Thread(target=recibir_msg)
hilo.start()

while True:
    mensaje = input("Escribe un mensaje: ")

    if mensaje.strip() == "":
        print("ERROR: No puedes ingresar una entrada vacía")
        continue

    cliente.send(mensaje.encode())