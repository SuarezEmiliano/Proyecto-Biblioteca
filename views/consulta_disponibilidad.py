import tkinter as tk
from tkinter import messagebox, ttk
from entities.Libro import Libro

def abrir_ventana_consulta_disponibilidad():
    ventana = tk.Toplevel()
    ventana.title("Consulta de Disponibilidad")
    ventana.geometry("+750+300")
    ventana.configure(bg="#2c3e50")
    ventana.resizable(False, False)

    # Obtener libros disponibles de la base de datos
    libros_disponibles = Libro.obtener_libros_disponibles()
    lista_libros = [(libro[0], libro[1]) for libro in libros_disponibles]

    # Crear un marco para el formulario
    frame = tk.Frame(ventana, bg="#34495e", padx=20, pady=20)
    frame.pack(pady=20)

    tk.Label(frame, text="Consulta de Disponibilidad", font=("Helvetica", 18), bg="#34495e", fg="#ecf0f1").grid(
        row=0, column=0, columnspan=2, pady=10
    )

    # Combobox para seleccionar libro
    tk.Label(frame, text="Libro:", bg="#34495e", fg="#ecf0f1").grid(row=1, column=0, sticky="w")
    combobox_libros = ttk.Combobox(
        frame,
        values=[f"{libro[0]} - {libro[1]}" for libro in lista_libros],
        state="readonly",
        width=40
    )
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
            mostrar_disponibilidad(cantidad_disponible)
        else:
            messagebox.showerror("Error", "El libro no está registrado o no se pudo obtener la cantidad disponible.")

    # Botón para consultar disponibilidad
    boton_consultar = tk.Button(
        ventana,
        text="Consultar disponibilidad",
        command=consultar_disponibilidad,
        bg="#008B8B",
        fg="white",
        relief=tk.RAISED,
        width=25,
        height=2
    )
    boton_consultar.pack(pady=20)

    def mostrar_disponibilidad(cantidad_disponible):
        confirmacion = tk.Toplevel()
        confirmacion.title(f"Disponibilidad")
        confirmacion.geometry("500x250+750+240")
        confirmacion.configure(bg="#2c3e50")

        tk.Label(confirmacion, text="Disponibilidad del libro", font=("Helvetica", 14), bg="#2c3e50", fg="#ecf0f1").pack(pady=(10, 5))
        tk.Label(confirmacion, text=f"'{combobox_libros.get()}'", font=("Helvetica", 14), bg="#2c3e50", fg="#ecf0f1").pack(pady=(10, 5))
        tk.Label(confirmacion, text=f"Cantidad disponible: {cantidad_disponible}", font=("Helvetica", 14), bg="#2c3e50", fg="#ecf0f1").pack()

        # Botón para cerrar la ventana
        tk.Button(
            confirmacion,
            text="Cerrar",
            command=confirmacion.destroy,
            bg="#008B8B",
            fg="white",
            font=("Helvetica", 12),
            width=12,
            height=2
        ).pack(pady=8)

    # Estilo del botón
    estilo = ttk.Style()
    estilo.configure("TButton", padding=6, relief="flat", background="#4CAF50", foreground="white")
    estilo.map("TButton", background=[("active", "#45a049")])

    ventana.mainloop()
