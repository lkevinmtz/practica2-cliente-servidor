import socket
import threading
import tkinter as tk
from tkinter import colorchooser, messagebox, scrolledtext

# Hilo que se ejecuta de fondo para recibir mensajes
class AplicacionCliente:
    def __init__(self, root):
    # Variables
        self.root = root
        self.root.withdraw()
        self.socketCliente = None
        self.nombreUser = ""
    
    # Login
        # Ventana
        self.Wlogin = tk.Toplevel(self.root)
        self.Wlogin.geometry("300x200")
        self.Wlogin.resizable(False, False)
        self.Wlogin.title("Login")

        # Contenido de la ventana
        tk.Label(self.Wlogin, text="IP del Server:", fg="black").pack(pady=(10, 5))
        self.entryIPServer = tk.Entry(self.Wlogin)
        self.entryIPServer.insert(0, "127.0.0.1")
        self.entryIPServer.pack()
        tk.Label(self.Wlogin, text="Usuario:", fg="black").pack(pady=(15, 5))
        self.entryNombreUsuario = tk.Entry(self.Wlogin)
        self.entryNombreUsuario.pack()

        # Botón y acción
        tk.Button(self.Wlogin, text="Conectarse", command=self.conectarServer, bg="#d5efd0", fg="black",
                  font=("Arial", 13), relief="raised").pack(padx=20, pady=20)
        self.root.protocol("WM_DELETE_WINDOW")
        self.Wlogin.protocol("WM_DELETE_WINDOW")

    def conectarServer(self):
    # Conexión inicial
        self.nombreUser = self.entryNombreUsuario.get()
        host = self.entryIPServer.get()
        puerto = 5000

        # No permitir usuarios vacíos
        if self.nombreUser.strip() == "":
            messagebox.showerror("Error", "Ingresa un nombre de usuario")
            return

        # Conexión al socket
        try:
            self.socketCliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socketCliente.connect((host, puerto))
            self.socketCliente.send(self.nombreUser.encode())

        except:
            messagebox.showerror("Error", "No se pudo conectar al servidor")
            return
        
        # Salir del login y entrar al chat
        self.Wlogin.destroy()
        self.crearVentanaChat()

        # Hilo para empezar a recibir mensajes
        hilo = threading.Thread(target=self.recibirMensajes)
        hilo.daemon = True
        hilo.start()
    
    def crearVentanaChat(self):
    # Ventana para el chat
        self.root.deiconify()
        self.root.title("Chat LAN")
        self.root.geometry("900x600")

        framePrincipal = tk.Frame(self.root)
        framePrincipal.pack(fill=tk.BOTH, expand=True)

        # Área de chat
        self.areaChat = scrolledtext.ScrolledText(framePrincipal)
        self.areaChat.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.areaChat.config(state=tk.DISABLED)

        # Lista de usuarios
        frameUsuarios = tk.Frame(framePrincipal, width=150)
        frameUsuarios.pack(side=tk.RIGHT, fill=tk.Y)

        tk.Label(frameUsuarios, text="Usuarios").pack()

        self.listaUsuarios = tk.Listbox(frameUsuarios)
        self.listaUsuarios.pack(fill=tk.Y, expand=True)

        # Área inferior
        frameInferior = tk.Frame(self.root)
        frameInferior.pack(fill=tk.X)

        self.entryMensaje = tk.Entry(frameInferior)
        self.entryMensaje.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)

        botonEnviar = tk.Button(frameInferior, text="Enviar", command=self.enviarMensaje)
        botonEnviar.pack(side=tk.RIGHT, padx=5)

        self.root.protocol("WM_DELETE_WINDOW", self.cerrarCliente)

    def enviarMensaje(self):
    # Envío de mensajes
        mensaje = self.entryMensaje.get()

        # No se permiten mensajes vacíos y en caso de desconexión, muestra el error
        if mensaje.strip() == "":
            return
        try:
            self.socketCliente.send(mensaje.encode())
        except:
            messagebox.showerror("Error", "Conexión perdida")

        self.entryMensaje.delete(0, tk.END)

    def recibirMensajes(self):
    # Lógica para recepción de mensajes
        while True:
            try:
                datos = self.socketCliente.recv(1024).decode()
                mensajes = datos.split("\n")

                for mensaje in mensajes:
                    if mensaje.strip() == "":
                        continue
                    
                    # Lista de usuarios
                    if mensaje.startswith("USERS:"):
                        usuarios = mensaje.replace("USERS:", "").split(",")
                        self.listaUsuarios.delete(0, tk.END)
                        for u in usuarios:
                            self.listaUsuarios.insert(tk.END, u)
                    else:
                        self.mostrarMensaje(mensaje)

            except:
                messagebox.showerror("Error", "Se perdió conexión con el servidor")
                break

    def mostrarMensaje(self, mensaje):
    # Lógica para mostrar mensajes
        self.areaChat.config(state=tk.NORMAL)

        # Evitar mostrar mensajes propios (duplicados)
        if mensaje.startswith(self.nombreUser + ":"):
            self.areaChat.insert(tk.END, mensaje + "\n", "propio")

        # Mensaje exclusivo para usuarios nuevos o usuarios desconectados
        elif "se ha unido" in mensaje or "ha salido" in mensaje:
            self.areaChat.insert(tk.END, mensaje + "\n", "notificacion")

        # Mensajes de otros usuarios
        else:
            self.areaChat.insert(tk.END, mensaje + "\n")

        # Incluir los mensajes en el area del chat y configurar los colores de los mensajes propios y del sistema
        self.areaChat.config(state=tk.DISABLED)
        self.areaChat.yview(tk.END)

        self.areaChat.tag_config("propio", foreground="blue")
        self.areaChat.tag_config("notificacion", foreground="gray")
   
    def cerrarCliente(self):
        try:
            self.socketCliente.shutdown(socket.SHUT_RDWR)
            self.socketCliente.close()
        except:
            pass

        self.root.quit()

root = tk.Tk()
AplicacionCliente(root)
root.mainloop()