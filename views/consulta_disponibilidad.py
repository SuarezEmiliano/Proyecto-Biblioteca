import tkinter as tk
from tkinter import messagebox, ttk
from entities.Libro import Libro

def abrir_ventana_consulta_disponibilidad():
    ventana = tk.Toplevel()
    ventana.title("Préstamo de Libros")
    ventana.geometry("400x400")
    ventana.configure(bg="#2c3e50")

    # Obtener libros disponibles de la base de datos
    libros_disponibles = Libro.obtener_libros_disponibles()
    lista_libros = [(libro[0], libro[1]) for libro in libros_disponibles]

    # Crear un marco para el formulario
    frame = tk.Frame(ventana, bg="#34495e", padx=20, pady=20)
    frame.pack(pady=20)

    tk.Label(frame, text="Préstamo de Libros", font=("Helvetica", 18), bg="#34495e", fg="#ecf0f1").grid(
        row=0, column=0, columnspan=2, pady=10
    )

    # Combobox para seleccionar libro
    tk.Label(frame, text="Libro:", bg="#34495e", fg="#ecf0f1").grid(row=1, column=0, sticky="w")
    combobox_libros = ttk.Combobox(frame, values=[f"{libro[0]} - {libro[1]}" for libro in lista_libros],
                                   state="readonly")
    combobox_libros.grid(row=1, column=1, pady=5)

    def consultar_disponibilidad():
        libro_seleccionado = combobox_libros.get()

        if not libro_seleccionado:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un libro.")
            return

        # Obtener código del libro seleccionado
        isbn_libro = libro_seleccionado.split(" - ")[0]

        # Consultar la cantidad disponible del libro
        cantidad_disponible = Libro.obtener_cantidad_disponible(isbn_libro)

        if cantidad_disponible is not None:
            messagebox.showinfo("Disponibilidad", f"Cantidad disponible: {cantidad_disponible}")
        else:
            messagebox.showerror("Error", "El libro no está registrado o no se pudo obtener la cantidad disponible.")

    # Botón para consultar disponibilidad
    boton_consultar = tk.Button(
        ventana,
        text="Consultar disponibilidad",
        command=consultar_disponibilidad,
        bg="#008B8B",  # Color de fondo del botón
        fg="white",  # Color del texto del botón
        relief=tk.RAISED,
        width=25,  # Ancho del botón
        height=2  # Altura del botón
    )
    boton_consultar.pack(pady=20)

    # Estilo del botón
    estilo = ttk.Style()
    estilo.configure("TButton", padding=6, relief="flat", background="#4CAF50", foreground="white")
    estilo.map("TButton", background=[("active", "#45a049")])

    ventana.mainloop()
