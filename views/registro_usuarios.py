import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import re
from entities.Usuario import Usuario

def abrir_ventana_registro_usuarios():
    ventana = tk.Toplevel()
    ventana.title("Registro de Usuarios")
    ventana.geometry("600x600+750+240")
    ventana.configure(bg="#2c3e50")
    ventana.resizable(False, False)

    # Crear un marco para el formulario
    frame = tk.Frame(ventana, bg="#34495e", padx=20, pady=20)
    frame.pack(pady=20)

    tk.Label(frame, text="Registro de Usuarios", font=("Helvetica", 18), bg="#34495e", fg="#ecf0f1").grid(row=0,
                                                                                                          column=0,
                                                                                                          columnspan=2,
                                                                                                          pady=10)

    # Campos de entrada para el formulario
    tk.Label(frame, text="Nombre:", bg="#34495e", fg="#ecf0f1").grid(row=1, column=0, sticky="w")
    entry_nombre = tk.Entry(frame, width=30, font=("Helvetica", 12))
    entry_nombre.grid(row=1, column=1, pady=5)
    label_error_nombre = tk.Label(frame, text="Debe ser solo letras (1-20 caracteres)", fg="red", bg="#34495e")
    label_error_nombre.grid(row=2, column=1, sticky="w")
    label_error_nombre.grid_remove()

    tk.Label(frame, text="Apellido:", bg="#34495e", fg="#ecf0f1").grid(row=3, column=0, sticky="w")
    entry_apellido = tk.Entry(frame, width=30, font=("Helvetica", 12))
    entry_apellido.grid(row=3, column=1, pady=5)
    label_error_apellido = tk.Label(frame, text="Debe ser solo letras (1-20 caracteres)", fg="red", bg="#34495e")
    label_error_apellido.grid(row=4, column=1, sticky="w")
    label_error_apellido.grid_remove()

    tk.Label(frame, text="Dirección:", bg="#34495e", fg="#ecf0f1").grid(row=5, column=0, sticky="w")
    entry_direccion = tk.Entry(frame, width=30, font=("Helvetica", 12))
    entry_direccion.grid(row=5, column=1, pady=5)
    label_error_direccion = tk.Label(frame, text="Debe ser alfanumérico (1-30 caracteres)", fg="red", bg="#34495e")
    label_error_direccion.grid(row=6, column=1, sticky="w")
    label_error_direccion.grid_remove()

    tk.Label(frame, text="Teléfono:", bg="#34495e", fg="#ecf0f1").grid(row=7, column=0, sticky="w")
    entry_telefono = tk.Entry(frame, width=30, font=("Helvetica", 12))
    entry_telefono.grid(row=7, column=1, pady=5)
    label_error_telefono = tk.Label(frame, text="Debe ser solo números", fg="red", bg="#34495e")
    label_error_telefono.grid(row=8, column=1, sticky="w")
    label_error_telefono.grid_remove()

    tk.Label(frame, text="Tipo de Usuario:", bg="#34495e", fg="#ecf0f1").grid(row=9, column=0, sticky="w")
    tipo_usuario = tk.StringVar(value="Estudiante")  # Valor por defecto
    rb_estudiante = tk.Radiobutton(frame, text="Estudiante", variable=tipo_usuario, value="Estudiante", bg="#34495e",
                                   fg="#008B8B", selectcolor="#ecf0f1")
    rb_profesor = tk.Radiobutton(frame, text="Profesor", variable=tipo_usuario, value="Profesor", bg="#34495e",
                                 fg="#008B8B", selectcolor="#ecf0f1")
    rb_estudiante.grid(row=9, column=1, sticky="w")
    rb_profesor.grid(row=10, column=1, sticky="w")

    # Función para manejar el registro del usuario
    def registrar_usuario():
        nombre = entry_nombre.get()
        apellido = entry_apellido.get()
        direccion = entry_direccion.get()
        telefono = entry_telefono.get()
        tipo = tipo_usuario.get()

        # Validar los campos
        campos_validos = True

        if not re.match("^[A-Za-záéíóúÁÉÍÓÚñÑ ]{1,20}$", nombre):
            label_error_nombre.grid()
            campos_validos = False
        else:
            label_error_nombre.grid_remove()

        if not re.match("^[A-Za-záéíóúÁÉÍÓÚñÑ ]{1,20}$", apellido):
            label_error_apellido.grid()
            campos_validos = False
        else:
            label_error_apellido.grid_remove()

        # Modificar validación de dirección para aceptar hasta 30 caracteres con letras, números y algunos caracteres especiales
        if not re.match("^[A-Za-z0-9áéíóúÁÉÍÓÚñÑ ,.-]{1,30}$", direccion):
            label_error_direccion.grid()
            campos_validos = False
        else:
            label_error_direccion.grid_remove()

        if not telefono.isdigit():
            label_error_telefono.grid()
            campos_validos = False
        else:
            label_error_telefono.grid_remove()

        if campos_validos:
            # Crear una instancia del usuario
            usuario = Usuario(nombre=nombre, apellido=apellido, tipo_usuario=tipo, direccion=direccion,
                              telefono=telefono)
            usuario.guardar()

            # Limpiar los campos antes de mostrar la ventana de confirmación
            entry_nombre.delete(0, tk.END)
            entry_apellido.delete(0, tk.END)
            entry_direccion.delete(0, tk.END)
            entry_telefono.delete(0, tk.END)
            tipo_usuario.set("Estudiante")  # Restablecer a valor por defecto

            # Mostrar la ventana de confirmación personalizada
            mostrar_confirmacion()

            # Cerrar la ventana de registro
            ventana.destroy()

    def mostrar_confirmacion():
        confirmacion = tk.Toplevel()
        confirmacion.title("Confirmación")
        confirmacion.geometry("400x200+750+240")
        confirmacion.configure(bg="#2c3e50")

        tk.Label(confirmacion, text="Usuario registrado con éxito!", font=("Helvetica", 14), bg="#2c3e50",
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

    # Función para consultar los libros creados

    def consultar_usuarios():
        usuarios = Usuario.obtener_usuarios_consulta()
        print(usuarios)

        # Crear una nueva ventana para mostrar los libros
        ventana_usuarios = tk.Toplevel()
        ventana_usuarios.title("Consulta de Usuarios")
        ventana_usuarios.geometry("1200x600+500+240")
        ventana_usuarios.configure(bg="#2c3e50")

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
        frame_contenedor = tk.Frame(ventana_usuarios, bg="#2c3e50")
        frame_contenedor.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Crear el Treeview para mostrar los libros
        tree = ttk.Treeview(frame_contenedor,
                            columns=("Id","Nombre", "Apellido", "Tipo","Direccion","Telefono"),
                            show="headings")

        # Definir las columnas y encabezados
        tree.heading("Id", text="Id", anchor="center")
        tree.heading("Nombre", text="Nombre", anchor="center")
        tree.heading("Apellido", text="Apellido", anchor="center")
        tree.heading("Tipo", text="Tipo", anchor="center")
        tree.heading("Direccion", text="Direccion", anchor="center")
        tree.heading("Telefono", text="Telefono", anchor="center")

        # Definir la alineación de las columnas
        tree.column("Id", width=120, anchor="center")
        tree.column("Nombre", width=120, anchor="center")
        tree.column("Apellido", width=250, anchor="center")
        tree.column("Tipo", width=150, anchor="center")
        tree.column("Direccion", width=150, anchor="center")
        tree.column("Telefono", width=150, anchor="center")


        # Insertar los autores en el Treeview
        for usuario in usuarios:
            tree.insert("", tk.END, values=(usuario[0],usuario[1], usuario[2], usuario[3], usuario[4], usuario[5]))

        # Función para eliminar el usuario seleccionado
        def eliminar_usuario_seleccionado():
            # Obtener el id del usuario seleccionado
            selected_item = tree.selection()
            if selected_item:
                id = tree.item(selected_item)["values"][0]
                confirmacion = messagebox.askyesno("Confirmación",
                                                   f"¿Estás seguro de que deseas eliminar al usuario con el id:{id}?")
                if confirmacion:
                    Usuario.eliminar_usuario(id)
                    tree.delete(selected_item)
                    messagebox.showinfo("Éxito", "El usuario ha sido eliminado correctamente.")
            else:
                messagebox.showwarning("Selección", "Por favor, selecciona un usuario para eliminar.")

        # Crear el botón de eliminar debajo del Treeview
        boton_eliminar = tk.Button(ventana_usuarios, text="Eliminar Usuario", command=eliminar_usuario_seleccionado,
                                   width=15, height=2, bg="#d9534f", fg="white", font=("Helvetica", 12))
        boton_eliminar.pack(pady=10)

        # Agregar el Treeview al frame
        tree.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    # Marco para los botones de "Cancelar" y "Registrar"
    frame_botones = tk.Frame(ventana, bg="#2c3e50")
    frame_botones.pack(pady=20)

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
        text="Registrar Usuario",
        command=registrar_usuario,
        bg="#008B8B",
        fg="white",
        font=("Helvetica", 12),
        width=15,
        height=2
    )
    boton_registrar.grid(row=0, column=1, padx=10)

    # Botón para consultar autores
    tk.Button(
        frame,
        text="Consultar Usuarios Existentes",
        command=consultar_usuarios,
        bg="#005f8b",
        fg="white",
        font=("Helvetica", 12),
        width=25,
        height=2
    ).grid(row=14, column=0, columnspan=2, pady=10)

    ventana.mainloop()