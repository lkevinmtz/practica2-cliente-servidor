import socket
import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext, colorchooser

# Función para recibir los mensajes de otros clientes
def recibir_msg():
    while True:
        try:
            mensaje = cliente.recv(1024).decode()
            if not mensaje:
                break
            print("\n" + mensaje)
        except:
            break

# Definición de Socket
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect(("127.0.0.1", 5000))

# Definición de Hilo
hilo = threading.Thread(target=recibir_msg)
hilo.start()

# # Loop para enviar mensajes
# while True:
#     mensaje = input("Escribe un mensaje: ")

#     # No se permiten mensajes vacíos
#     if mensaje.strip() == "":
#         print("ERROR: No puedes ingresar una entrada vacía")
#         continue

#     cliente.send(mensaje.encode())

# Iniciar la interfaz
root = tk.Tk()
root.title("Discord Chafa")
root.geometry("300x400")
root.resizable(False, False)

# Título
tk.Label(root, text="Walkie Talkie", font=("Arial", 18, "bold"), fg='white', bg='black').pack(pady=20)

root.mainloop()
