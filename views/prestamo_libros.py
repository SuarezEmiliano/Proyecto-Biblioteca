import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import Calendar
from entities.Libro import Libro
from entities.Prestamo import Prestamo
from entities.Usuario import Usuario
import re
from datetime import datetime

def abrir_ventana_prestamo_libros():
    ventana = tk.Toplevel()
    ventana.title("Préstamo de Libros")
    ventana.geometry("600x600+750+240")
    ventana.configure(bg="#2c3e50")

    # Obtener libros disponibles de la base de datos
    libros_disponibles = Libro.obtener_libros_disponibles()
    lista_libros = [(libro[0], libro[1]) for libro in libros_disponibles]

    usuarios_disponibles = Usuario.obtener_usuarios()
    lista_usuarios = [(usuario[0], usuario[1]) for usuario in usuarios_disponibles]

    # Crear un marco para el formulario
    frame = tk.Frame(ventana, bg="#34495e", padx=20, pady=20)
    frame.grid(pady=20, row=0, column=0, sticky="ew")
    ventana.grid_columnconfigure(0, weight=1)

    tk.Label(frame, text="Préstamo de Libros", font=("Helvetica", 18), bg="#34495e", fg="#ecf0f1").grid(
        row=0, column=0, columnspan=2, pady=10
    )

    # Combobox para seleccionar libro
    tk.Label(frame, text="Libro:", bg="#34495e", fg="#ecf0f1").grid(row=1, column=0, sticky="w")
    combobox_libros = ttk.Combobox(frame, values=[f"{libro[0]} - {libro[1]}" for libro in lista_libros], state="readonly", width="42")
    combobox_libros.grid(row=1, column=1, pady=5)
    label_error_libro = tk.Label(frame, text="", fg="red", bg="#34495e")
    label_error_libro.grid(row=2, column=1, sticky="w")
    
    # Combobox para seleccionar usuario
    tk.Label(frame, text="Usuario:", bg="#34495e", fg="#ecf0f1").grid(row=3, column=0, sticky="w")
    combobox_usuarios = ttk.Combobox(frame, values=[f"{usuario[0]} - {usuario[1]}" for usuario in lista_usuarios], state="readonly", width="42")
    combobox_usuarios.grid(row=3, column=1, pady=5)
    label_error_usuario = tk.Label(frame, text="", fg="red", bg="#34495e")
    label_error_usuario.grid(row=4, column=1, sticky="w")



    def mostrar_calendario_prestamo():
        cal_fecha_prestamo = None
        if cal_fecha_prestamo is not None:
            cal_fecha_prestamo.grid_forget()  # Oculta el calendario si ya estaba visible
        cal_fecha_prestamo = Calendar(frame, selectmode='day', date_pattern='yyyy-mm-dd')
        cal_fecha_prestamo.grid(row=5, column=1, pady=5)

        def seleccionar_fecha_prestamo(event):
            entry_fecha_prestamo.delete(0, tk.END)
            entry_fecha_prestamo.insert(0, cal_fecha_prestamo.get_date())
            cal_fecha_prestamo.grid_forget()  # Oculta el calendario después de seleccionar una fecha

        cal_fecha_prestamo.bind("<<CalendarSelected>>", seleccionar_fecha_prestamo)

    def mostrar_calendario_devolucion():
        cal_fecha_devolucion = None
        if cal_fecha_devolucion is not None:
            cal_fecha_devolucion.grid_forget()  # Oculta el calendario si ya estaba visible
        cal_fecha_devolucion = Calendar(frame, selectmode='day', date_pattern='yyyy-mm-dd')
        cal_fecha_devolucion.grid(row=7, column=1, pady=5)

        def seleccionar_fecha_devolucion(event):
            entry_fecha_devolucion.delete(0, tk.END)
            entry_fecha_devolucion.insert(0, cal_fecha_devolucion.get_date())
            cal_fecha_devolucion.grid_forget()  # Oculta el calendario después de seleccionar una fecha

        cal_fecha_devolucion.bind("<<CalendarSelected>>", seleccionar_fecha_devolucion)

    def mostrar_confirmacion():
        confirmacion = tk.Toplevel()
        confirmacion.title("Confirmación")
        confirmacion.geometry("400x200+750+240")
        confirmacion.configure(bg="#2c3e50")

        tk.Label(confirmacion, text="Préstamo registrado con éxito!", font=("Helvetica", 14), bg="#2c3e50", fg="#ecf0f1").pack(pady=20)

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

    # Campos para las fechas
    tk.Label(frame, text="Fecha de Préstamo:", bg="#34495e", fg="#ecf0f1").grid(row=5, column=0, sticky="w", padx=5)
    entry_fecha_prestamo = tk.Entry(frame, width=30, font=("Helvetica", 12))
    entry_fecha_prestamo.grid(row=5, column=1, pady=5)
    label_error_fecha_prestamo = tk.Label(frame, text="", fg="red", bg="#34495e")
    label_error_fecha_prestamo.grid(row=6, column=1, sticky="w")
    boton_calendario_prestamo = tk.Button(frame, text="📅", command=mostrar_calendario_prestamo, bg="#16a085", fg="white")
    boton_calendario_prestamo.grid(row=5, column=2, padx=5)

    # Modificado para evitar la superposición de los errores
    tk.Label(frame, text="Fecha de Devolución:", bg="#34495e", fg="#ecf0f1").grid(row=7, column=0, sticky="w", padx=5)
    entry_fecha_devolucion = tk.Entry(frame, width=30, font=("Helvetica", 12))
    entry_fecha_devolucion.grid(row=7, column=1, pady=5)
    label_error_fecha_devolucion = tk.Label(frame, text="", fg="red", bg="#34495e")
    label_error_fecha_devolucion.grid(row=8, column=1, sticky="w")
    boton_calendario_devolucion = tk.Button(frame, text="📅", command=mostrar_calendario_devolucion, bg="#16a085", fg="white")
    boton_calendario_devolucion.grid(row=7, column=2, padx=5)


    # Función para validar las fechas (formato YYYY-MM-DD)
    def validar_fecha(fecha):
        return bool(re.match(r"\d{4}-\d{2}-\d{2}", fecha))

    def registrar_prestamo():
        libro_seleccionado = combobox_libros.get()
        usuario_seleccionado = combobox_usuarios.get()
        fecha_prestamo = entry_fecha_prestamo.get()
        fecha_devolucion = entry_fecha_devolucion.get()

        # Limpiar los mensajes de error
        label_error_libro.config(text="")
        label_error_usuario.config(text="")
        label_error_fecha_prestamo.config(text="")
        label_error_fecha_devolucion.config(text="")

        campos_validos = True
        hoy = datetime.now().date()

        # Validación de libro y usuario
        if not libro_seleccionado:
            label_error_libro.config(text="Selecciona un libro válido.")
            campos_validos = False
        if not usuario_seleccionado:
            label_error_usuario.config(text="Selecciona un usuario válido.")
            campos_validos = False

        if not validar_fecha(fecha_prestamo):
            campos_validos = False
            label_error_fecha_prestamo.config(text="Formato de fecha incorrecto (YYYY-MM-DD).")
            
        if not validar_fecha(fecha_devolucion):
            label_error_fecha_devolucion.config(text="Formato de fecha incorrecto (YYYY-MM-DD).")
            campos_validos = False

        fecha_prestamo_dt = datetime.strptime(fecha_prestamo, "%Y-%m-%d").date()
        fecha_devolucion_dt = datetime.strptime(fecha_devolucion, "%Y-%m-%d").date()

        if fecha_prestamo_dt < hoy:
            label_error_fecha_prestamo.config(text="La fecha de préstamo no puede ser anterior a hoy.")
            campos_validos = False
        if fecha_devolucion_dt <= fecha_prestamo_dt:
            label_error_fecha_devolucion.config(text="La fecha de devolución debe ser posterior a la fecha de préstamo.")
            campos_validos = False

        if campos_validos:
            # Obtener código del libro seleccionado
            codigo_libro = libro_seleccionado.split(" - ")[0]


            # Obtener id del usuario seleccionado
            id_usuario = usuario_seleccionado.split(" - ")[0]


            # Obtener el tipo de usuario (estudiante o profesor)
            tipo_usuario = Usuario.obtener_tipo_usuario(id_usuario)


            # Verificar la cantidad de libros prestados
            libros_prestados = Prestamo.obtener_libros_prestados_por_usuario(id_usuario)


            if tipo_usuario == "Estudiante" and libros_prestados >= 3:
                label_error_usuario.config(text="Un estudiante no puede tener más de 3 libros prestados.")
                return
            elif tipo_usuario == "Profesor" and libros_prestados >= 5:
                label_error_usuario.config(text="Un profesor no puede tener más de 5 libros prestados.")
                return

            # Registrar el préstamo
            prestamo = Prestamo(id_usuario, codigo_libro, fecha_prestamo, fecha_devolucion)
            prestamo.guardar()

            # Restar 1 a la cantidad disponible del libro
            Libro.actualizar_cantidad_disponible(codigo_libro, -1)

            mostrar_confirmacion()

            # Limpiar los campos
            combobox_libros.set('')
            combobox_usuarios.set('')
            entry_fecha_prestamo.delete(0, tk.END)
            entry_fecha_devolucion.delete(0, tk.END)
            ventana.destroy()
                
    def consultar_prestamos():
        prestamos = Prestamo.obtener_prestamos_consulta()

        # Crear una nueva ventana para mostrar los libros
        ventana_prestamos = tk.Toplevel()
        ventana_prestamos.title("Consulta de prestamos")
        ventana_prestamos.geometry("1200x600+500+240")
        ventana_prestamos.configure(bg="#2c3e50")

        # Estilos del Treeview
        estilo = ttk.Style()
        estilo.configure("Treeview",
                         background="#34495e",
                         foreground="white",
                         fieldbackground="#008B8B",
                         font=("Helvetica", 10),
                         rowheight=25)

        estilo.configure("Treeview.Heading",
                         background="#2c3e50",
                         foreground="black",
                         font=("Helvetica", 12, "bold"),
                         anchor="center")

        estilo.map("Treeview",
                   background=[('selected', '#16a085')],
                   foreground=[('selected', 'white')])

        # Crear un frame para contener el Treeview y el botón de eliminar
        frame_contenedor = tk.Frame(ventana_prestamos, bg="#2c3e50")
        frame_contenedor.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Crear el Treeview para mostrar los libros
        tree = ttk.Treeview(frame_contenedor,
                            columns=("Id Prestamo","Usuario","Libro", "Fecha de prestamo", "Fecha de devolucion"),
                            show="headings")

        # Definir las columnas y encabezados
        tree.heading("Id Prestamo", text="Id Prestamo", anchor="center")
        tree.heading("Usuario", text="Usuario", anchor="center")
        tree.heading("Libro", text="Libro", anchor="center")
        tree.heading("Fecha de prestamo", text="Fecha de prestamo", anchor="center")
        tree.heading("Fecha de devolucion", text="Fecha de devolucion", anchor="center")

        # Definir la alineación de las columnas
        tree.column("Id Prestamo", width=120, anchor="center")
        tree.column("Usuario", width=120, anchor="center")
        tree.column("Libro", width=120, anchor="center")
        tree.column("Fecha de prestamo", width=250, anchor="center")
        tree.column("Fecha de devolucion", width=150, anchor="center")


        # Insertar los autores en el Treeview
        for prestamo in prestamos:
            id_usuario = prestamo[1]
            nombre_y_apellido = Usuario.obtener_nombre_apellido(id_usuario)
            nombre_usuario = nombre_y_apellido[0]
            apellido_usuario = nombre_y_apellido[1]

            isbn = prestamo[2]
            libro = Libro.obtener_por_isbn(isbn)
            nombre_libro = libro[0]

            tree.insert("", tk.END, values=(prestamo[0],nombre_usuario,nombre_libro, prestamo[2], prestamo[3]))

        # Función para eliminar el libro seleccionado
        def eliminar_prestamo_seleccionado():
            # Obtener el Id del prestamo seleccionado
            selected_item = tree.selection()
            if selected_item:
                id = tree.item(selected_item)["values"][0]  # Obtener el ISBN
                confirmacion = messagebox.askyesno("Confirmación",
                                                   f"¿Estás seguro de que deseas eliminar el préstamo con Id {id}?")
                if confirmacion:
                    Prestamo.eliminar_prestamo(id)
                    tree.delete(selected_item)
                    messagebox.showinfo("Éxito", "El préstamo ha sido eliminado correctamente.")
            else:
                messagebox.showwarning("Selección", "Por favor, selecciona un libro para eliminar.")

        # Crear el botón de eliminar debajo del Treeview
        boton_eliminar = tk.Button(ventana_prestamos, text="Eliminar Prestamo", command=eliminar_prestamo_seleccionado,
                                   width=15, height=2, bg="#d9534f", fg="white", font=("Helvetica", 12))
        boton_eliminar.pack(pady=10)

        # Agregar el Treeview al frame
        tree.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

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
        text="Registrar Préstamo",
        command=registrar_prestamo,
        bg="#008B8B",
        fg="white",
        font=("Helvetica", 12),
        width=15,
        height=2
    )
    boton_registrar.grid(row=0, column=1, padx=10)

    # Botón para consultar prestamos
    tk.Button(
        frame,
        text="Consultar Prestamos Existentes",
        command=consultar_prestamos,
        bg="#005f8b",
        fg="white",
        font=("Helvetica", 12),
        width=25,
        height=2
    ).grid(row=14, column=0, columnspan=2, pady=10)

    ventana.mainloop()
