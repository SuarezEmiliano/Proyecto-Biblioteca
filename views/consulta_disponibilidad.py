import tkinter as tk

def abrir_ventana_consulta_disponibilidad():
    ventana = tk.Toplevel()
    ventana.title("Consulta de Disponibilidad")
    tk.Label(ventana, text="Consulta de Disponibilidad de Libros").pack()
    # Añade aquí los campos de entrada y botones para consultar la disponibilidad de un libro
