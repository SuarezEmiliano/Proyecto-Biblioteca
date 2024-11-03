import tkinter as tk

def abrir_ventana_devolucion_libros():
    ventana = tk.Toplevel()
    ventana.title("Devolución de Libros")
    tk.Label(ventana, text="Devolución de Libros").pack()
    # Añade aquí los campos de entrada y botones para registrar la devolución de un libro
