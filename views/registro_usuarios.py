import tkinter as tk

def abrir_ventana_registro_usuarios():
    ventana = tk.Toplevel()
    ventana.title("Registro de Usuarios")
    tk.Label(ventana, text="Registro de Usuarios").pack()
    # Añade aquí los campos de entrada y botones para registrar usuarios
