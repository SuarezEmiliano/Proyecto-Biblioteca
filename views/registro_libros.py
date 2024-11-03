import tkinter as tk

def abrir_ventana_registro_libros():
    ventana = tk.Toplevel()
    ventana.title("Registro de Libros")
    tk.Label(ventana, text="Registro de Libros").pack()
