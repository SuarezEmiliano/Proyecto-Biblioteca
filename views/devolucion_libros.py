import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from entities.Libro import Libro
from entities.Prestamo import Prestamo
from entities.Usuario import Usuario
import re


def abrir_ventana_devolucion_libros():
    ventana = tk.Toplevel()
    ventana.title("Devolución de Libros")
    ventana.geometry("600x400+750+240")
    ventana.configure(bg="#2c3e50")

    # Obtener préstamos de libros para devolver
    prestamos_pendientes = Prestamo.obtener_prestamos_pendientes()
    lista_prestamos = [(prestamo[0], f"{prestamo[1]} - {prestamo[2]}") for prestamo in prestamos_pendientes]

    # Crear un marco para el formulario
    frame = tk.Frame(ventana, bg="#34495e", padx=20, pady=20)
    frame.grid(pady=20, row=0, column=0)

    tk.Label(frame, text="Devolución de Libros", font=("Helvetica", 18), bg="#34495e", fg="#ecf0f1").grid(
        row=0, column=0, columnspan=2, pady=10
    )

    # Combobox para seleccionar préstamo
    tk.Label(frame, text="Préstamo:", bg="#34495e", fg="#ecf0f1").grid(row=1, column=0, sticky="w")
    combobox_prestamos = ttk.Combobox(frame, values=[f"{prestamo[0]} - {prestamo[1]}" for prestamo in lista_prestamos],
                                      state="readonly", width="42")
    combobox_prestamos.grid(row=1, column=1, pady=5)
    label_error_prestamo = tk.Label(frame, text="", fg="red", bg="#34495e")
    label_error_prestamo.grid(row=2, column=1, sticky="w")

    # Campo para la fecha de devolución
    tk.Label(frame, text="Fecha de Devolución:", bg="#34495e", fg="#ecf0f1").grid(row=3, column=0, sticky="w", padx=5)
    entry_fecha_devolucion = tk.Entry(frame, width=30, font=("Helvetica", 12))
    entry_fecha_devolucion.grid(row=3, column=1, pady=5)
    label_error_fecha_devolucion = tk.Label(frame, text="", fg="red", bg="#34495e")
    label_error_fecha_devolucion.grid(row=4, column=1, sticky="w")

    def mostrar_calendario_devolucion():
        cal_fecha_devolucion = Calendar(frame, selectmode='day', date_pattern='yyyy-mm-dd')
        cal_fecha_devolucion.grid(row=5, column=1, pady=5)

        def seleccionar_fecha_devolucion(event):
            entry_fecha_devolucion.delete(0, tk.END)
            entry_fecha_devolucion.insert(0, cal_fecha_devolucion.get_date())
            cal_fecha_devolucion.grid_forget()

        cal_fecha_devolucion.bind("<<CalendarSelected>>", seleccionar_fecha_devolucion)

    boton_calendario_devolucion = tk.Button(frame, text="📅", command=mostrar_calendario_devolucion, bg="#16a085",
                                            fg="white")
    boton_calendario_devolucion.grid(row=3, column=2, padx=5)

    # Validación de la fecha
    def validar_fecha(fecha):
        return bool(re.match(r"\d{4}-\d{2}-\d{2}", fecha))

    # Mostrar ventana de confirmación
    def mostrar_confirmacion():
        confirmacion = tk.Toplevel()
        confirmacion.title("Confirmación")
        confirmacion.geometry("400x200+750+240")
        confirmacion.configure(bg="#2c3e50")

        tk.Label(confirmacion, text="Devolución registrada con éxito!", font=("Helvetica", 14), bg="#2c3e50",
                 fg="#ecf0f1").pack(pady=20)

        # Botón para cerrar la ventana de confirmación
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

    # Función para registrar la devolución
    def registrar_devolucion():
        prestamo_seleccionado = combobox_prestamos.get()
        fecha_devolucion = entry_fecha_devolucion.get()

        # Limpiar mensajes de error
        label_error_prestamo.config(text="")
        label_error_fecha_devolucion.config(text="")

        campos_validos = True

        # Validación de campos
        if not prestamo_seleccionado:
            label_error_prestamo.config(text="Selecciona un préstamo válido.")
            campos_validos = False
        if not fecha_devolucion:
            label_error_fecha_devolucion.config(text="Ingresa una fecha de devolución.")
            campos_validos = False
        if not validar_fecha(fecha_devolucion):
            label_error_fecha_devolucion.config(text="La fecha debe ser en formato YYYY-MM-DD.")
            campos_validos = False

        if campos_validos:
            # Obtener el id del préstamo seleccionado
            id_prestamo = prestamo_seleccionado.split(" - ")[0]

            # Obtener el código del libro del préstamo
            codigo_libro = Prestamo.obtener_codigo_libro(id_prestamo)

            # Actualizar la base de datos
            Prestamo.registrar_devolucion(id_prestamo, fecha_devolucion)

            # Aumentar 1 a la cantidad disponible del libro
            Libro.actualizar_cantidad_disponible(codigo_libro, 1)

            mostrar_confirmacion()

            # Limpiar campos
            combobox_prestamos.set('')
            entry_fecha_devolucion.delete(0, tk.END)
            ventana.destroy()

    # Botón para registrar devolución
    boton_registrar = tk.Button(
        ventana,
        text="Registrar Devolución",
        command=registrar_devolucion,
        bg="#008B8B",
        fg="white",
        relief=tk.RAISED,
        width=25,
        height=2
    )
    boton_registrar.grid(row=6, column=0, columnspan=3, pady=20)

    ventana.mainloop()
