import tkinter as tk
from tkinter import ttk

from entities.Libro import Libro


def abrir_ventana_devolucion_libros():
    ventana = tk.Toplevel()
    ventana.title("Devolución de Libros")
    ventana.geometry("600x400+750+240")
    ventana.configure(bg="#2c3e50")

    # Obtener libros disponibles de la base de datos
    libros_disponibles = Libro.obtener_libros_disponibles()
    lista_libros = [(libro[0], libro[1]) for libro in libros_disponibles]

    # Crear un marco para el formulario
    frame = tk.Frame(ventana, bg="#34495e", padx=20, pady=20)
    frame.grid(pady=20, row=0, column=0)

    tk.Label(frame, text="Devolución de Libros", font=("Helvetica", 18), bg="#34495e", fg="#ecf0f1").grid(
        row=0, column=0, columnspan=2, pady=10
    )

    # Combobox para seleccionar libro
    tk.Label(frame, text="Libro:", bg="#34495e", fg="#ecf0f1").grid(row=1, column=0, sticky="w")
    combobox_libros = ttk.Combobox(frame, values=[f"{libro[0]} - {libro[1]}" for libro in lista_libros],
                                   state="readonly", width="42")
    combobox_libros.grid(row=1, column=1, pady=5)
    label_error_libro = tk.Label(frame, text="", fg="red", bg="#34495e")
    label_error_libro.grid(row=2, column=1, sticky="w")



    ventana.mainloop()
