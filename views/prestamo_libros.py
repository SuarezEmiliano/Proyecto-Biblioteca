import tkinter as tk
from tkinter import messagebox, ttk
from entities.Libro import Libro
from entities.Prestamo import Prestamo
from entities.Usuario import Usuario

def abrir_ventana_prestamo_libros():
    ventana = tk.Toplevel()
    ventana.title("Préstamo de Libros")
    ventana.geometry("400x400")

    # Obtener libros disponibles de la base de datos
    libros_disponibles = Libro.obtener_libros_disponibles()
    lista_libros = [(libro[0], libro[1]) for libro in libros_disponibles]

    usuarios_disponibles = Usuario.obtener_usuarios()
    lista_usuarios = [(usuario[0], usuario[1]) for usuario in usuarios_disponibles]

    # Crear un marco para el formulario
    frame = tk.Frame(ventana, padx=20, pady=20)
    frame.pack(pady=20)

    tk.Label(frame, text="Préstamo de Libros", font=("Helvetica", 18)).grid(row=0, column=0, columnspan=2, pady=10)

    # Combobox para seleccionar libro
    tk.Label(frame, text="Libro:").grid(row=1, column=0, sticky="w")
    combobox_libros = ttk.Combobox(frame, values=[f"{libro[0]} - {libro[1]}" for libro in lista_libros], state="readonly")
    combobox_libros.grid(row=1, column=1, pady=5)

    # Combobox para seleccionar usuario
    tk.Label(frame, text="Usuario:").grid(row=2, column=0, sticky="w")
    combobox_usuarios = ttk.Combobox(frame, values=[f"{usuario[0]} - {usuario[1]}" for usuario in lista_usuarios], state="readonly")
    combobox_usuarios.grid(row=2, column=1, pady=5)

    # Campos para fechas
    tk.Label(frame, text="Fecha de Préstamo:").grid(row=3, column=0, sticky="w")
    entry_fecha_prestamo = tk.Entry(frame, width=30)
    entry_fecha_prestamo.grid(row=3, column=1, pady=5)

    tk.Label(frame, text="Fecha de Devolución:").grid(row=4, column=0, sticky="w")
    entry_fecha_devolucion = tk.Entry(frame, width=30)
    entry_fecha_devolucion.grid(row=4, column=1, pady=5)

    def registrar_prestamo():
        libro_seleccionado = combobox_libros.get()
        usuario_seleccionado = combobox_usuarios.get()
        fecha_prestamo = entry_fecha_prestamo.get()
        fecha_devolucion = entry_fecha_devolucion.get()

        if not libro_seleccionado or not usuario_seleccionado or not fecha_prestamo or not fecha_devolucion:
            messagebox.showwarning("Advertencia", "Por favor, completa todos los campos.")
            return

        # Obtener código del libro seleccionado
        codigo_libro = libro_seleccionado.split(" - ")[0]

        # Obtener id del usuario seleccionado   
        id_usuario = usuario_seleccionado.split(" - ")[0]

        # Aquí puedes crear la instancia de préstamo y guardarla en la base de datos
        try:
            prestamo = Prestamo(id_usuario, codigo_libro, fecha_prestamo, fecha_devolucion)
            prestamo.guardar()  # Asegúrate de que esta función maneja excepciones

            messagebox.showinfo("Éxito", "Préstamo registrado con éxito!")
        except Exception as e:
            messagebox.showerror("Error", f"Hubo un problema al registrar el préstamo: {e}")

        # Limpiar los campos
        combobox_libros.set('')
        combobox_usuarios.set('')
        entry_fecha_prestamo.delete(0, tk.END)
        entry_fecha_devolucion.delete(0, tk.END)

    boton_registrar = tk.Button(ventana, text="Registrar Préstamo", command=registrar_prestamo)
    boton_registrar.pack(pady=20)

    ventana.mainloop()