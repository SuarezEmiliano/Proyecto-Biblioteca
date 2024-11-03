import tkinter as tk

def abrir_ventana_reportes():
    ventana = tk.Toplevel()
    ventana.title("Reportes")
    tk.Label(ventana, text="Generar Reportes").pack()
    # Añade aquí los campos de entrada y botones para generar reportes
