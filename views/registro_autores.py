import tkinter as tk

def abrir_ventana_registro_autores():
    ventana = tk.Toplevel()
    ventana.title("Registro de Autores")
    tk.Label(ventana, text="Registro de Autores").pack()
    # Añade aquí los campos de entrada y botones para registrar autores
