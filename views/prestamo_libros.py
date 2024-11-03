import tkinter as tk

def abrir_ventana_prestamo_libros():
    ventana = tk.Toplevel()
    ventana.title("Préstamo de Libros")
    tk.Label(ventana, text="Préstamo de Libros").pack()
    # Añade aquí los campos de entrada y botones para registrar un préstamo
