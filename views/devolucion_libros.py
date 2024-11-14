import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from entities.Libro import Libro
from entities.Prestamo import Prestamo
from entities.Usuario import Usuario
import re
from datetime import datetime

def abrir_ventana_devolucion_libros():
    ventana = tk.Toplevel()
    ventana.title("Devolución de Libros")
    ventana.geometry("600x400+750+240")
    ventana.configure(bg="#2c3e50")

    # Obtener préstamos de libros para devolver
    prestamos_pendientes = Prestamo.obtener_prestamos_consulta()
    lista_prestamos = []

    for prestamo in prestamos_pendientes:
        id_usuario = prestamo[1]
        nombre_y_apellido = Usuario.obtener_nombre_apellido(id_usuario)
        nombre_usuario = nombre_y_apellido[0]
        apellido_usuario = nombre_y_apellido[1]
        nombre_completo_usuario = f"{nombre_usuario} {apellido_usuario}"

        isbn = prestamo[2]
        libro = Libro.obtener_por_isbn(isbn)
        nombre_libro = libro[1]

        # Concatenamos el nombre del usuario con el nombre del libro para cada préstamo
        lista_prestamos.append(f"{prestamo[0]} - {nombre_completo_usuario} - {nombre_libro}")

    # Crear un marco para el formulario
    frame = tk.Frame(ventana, bg="#34495e", padx=20, pady=20)
    frame.grid(pady=20, row=0, column=0, sticky="ew")
    ventana.grid_columnconfigure(0, weight=1)

    tk.Label(frame, text="Devolución de Libros", font=("Helvetica", 18), bg="#34495e", fg="#ecf0f1").grid(
        row=0, column=0, columnspan=2, pady=10
    )

    # Combobox para seleccionar préstamo
    tk.Label(frame, text="Préstamo:", bg="#34495e", fg="#ecf0f1").grid(row=1, column=0, sticky="w")
    combobox_prestamos = ttk.Combobox(frame, values=lista_prestamos, state="readonly", width="42")
    combobox_prestamos.grid(row=1, column=1, pady=5)
    label_error_prestamo = tk.Label(frame, text="", fg="red", bg="#34495e")
    label_error_prestamo.grid(row=2, column=1, sticky="w")

    # Campo estado
    tk.Label(frame, text="Estado:", bg="#34495e", fg="#ecf0f1").grid(row=5, column=0, sticky="w")
    combobox_estado = ttk.Combobox(frame, values=["Buen Estado", "Mal Estado"], state="readonly", width="42")
    combobox_estado.grid(row=5, column=1, pady=5)
    label_error_estado = tk.Label(frame, text="", fg="red", bg="#34495e")
    label_error_estado.grid(row=6, column=1, sticky="w")

    


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
        fecha_devolucion = datetime.now().date()
        estado_seleccionado = combobox_estado.get()

        # Limpiar mensajes de error
        label_error_prestamo.config(text="")
        label_error_estado.config(text="")

        campos_validos = True

        # Validación de campos
        if not prestamo_seleccionado:
            label_error_prestamo.config(text="Selecciona un préstamo válido.")
            campos_validos = False

        if not estado_seleccionado:
            label_error_estado.config(text="Selecciona el estado del libro.")
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

            if estado_seleccionado == "Mal Estado":
                Libro.actualizar_cantidad_buen_estado(codigo_libro, -1)

            mostrar_confirmacion()

            # Limpiar campos
            combobox_prestamos.set('')
            combobox_estado.set('')
            ventana.destroy()

    # Marco para los botones de "Cancelar" y "Registrar"
    frame_botones = tk.Frame(ventana, bg="#2c3e50")
    frame_botones.grid(pady=20)

    # Botón de cancelar a la izquierda
    boton_cancelar = tk.Button(
        frame_botones,
        text="Cancelar",
        command=ventana.destroy,
        bg="#d9534f",
        fg="white",
        font=("Helvetica", 12),
        width=15,
        height=2
    )
    boton_cancelar.grid(row=0, column=0, padx=10)

    # Botón de registrar a la derecha
    boton_registrar = tk.Button(
        frame_botones,
        text="Registrar Devolución",
        command=registrar_devolucion,
        bg="#008B8B",
        fg="white",
        font=("Helvetica", 12),
        width=15,
        height=2
    )
    boton_registrar.grid(row=0, column=1, padx=10)

    ventana.mainloop()
