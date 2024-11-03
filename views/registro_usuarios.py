import tkinter as tk
from tkinter import messagebox, ttk
from entities.Usuario import Usuario  # Asegúrate de que esta ruta sea correcta


def abrir_ventana_registro_usuarios():
    ventana = tk.Toplevel()
    ventana.title("Registro de Usuarios")
    ventana.geometry("400x400")
    ventana.configure(bg="#2c3e50")  # Color de fondo más elegante

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

    tk.Label(frame, text="Apellido:", bg="#34495e", fg="#ecf0f1").grid(row=2, column=0, sticky="w")
    entry_apellido = tk.Entry(frame, width=30, font=("Helvetica", 12))
    entry_apellido.grid(row=2, column=1, pady=5)

    tk.Label(frame, text="Dirección:", bg="#34495e", fg="#ecf0f1").grid(row=3, column=0, sticky="w")
    entry_direccion = tk.Entry(frame, width=30, font=("Helvetica", 12))
    entry_direccion.grid(row=3, column=1, pady=5)

    tk.Label(frame, text="Teléfono:", bg="#34495e", fg="#ecf0f1").grid(row=4, column=0, sticky="w")
    entry_telefono = tk.Entry(frame, width=30, font=("Helvetica", 12))
    entry_telefono.grid(row=4, column=1, pady=5)

    tk.Label(frame, text="Tipo de Usuario:", bg="#34495e", fg="#ecf0f1").grid(row=5, column=0, sticky="w")
    tipo_usuario = tk.StringVar(value="Estudiante")  # Valor por defecto
    rb_estudiante = tk.Radiobutton(frame, text="Estudiante", variable=tipo_usuario, value="Estudiante", bg="#34495e",
                                   fg="#008B8B", selectcolor="#ecf0f1")
    rb_profesor = tk.Radiobutton(frame, text="Profesor", variable=tipo_usuario, value="Profesor", bg="#34495e",
                                 fg="#008B8B", selectcolor="#ecf0f1")
    rb_estudiante.grid(row=5, column=1, sticky="w")
    rb_profesor.grid(row=6, column=1, sticky="w")

    # Función para manejar el registro del usuario
    def registrar_usuario():
        nombre = entry_nombre.get()
        apellido = entry_apellido.get()
        direccion = entry_direccion.get()
        telefono = entry_telefono.get()
        tipo = tipo_usuario.get()

        # Validar los campos
        if not nombre or not apellido or not direccion or not telefono:
            messagebox.showwarning("Advertencia", "Por favor, completa todos los campos.")
            return

        # Crear una instancia del usuario
        nuevo_usuario = Usuario(id=None, nombre=nombre, apellido=apellido, tipo_usuario=tipo, direccion=direccion,
                                telefono=telefono)

        # Aquí puedes añadir la lógica para guardar el usuario en la base de datos
        # Por ejemplo: guardar_usuario_en_db(nuevo_usuario)

        # Mostrar un mensaje de éxito
        messagebox.showinfo("Éxito", "Usuario registrado correctamente.")

        # Limpiar los campos
        entry_nombre.delete(0, tk.END)
        entry_apellido.delete(0, tk.END)
        entry_direccion.delete(0, tk.END)
        entry_telefono.delete(0, tk.END)
        tipo_usuario.set("Estudiante")  # Restablecer a valor por defecto

    # Botón para registrar el usuario
    boton_registrar = tk.Button(
        ventana,
        text="Registrar Autor",
        command=registrar_usuario,
        bg="#008B8B",  # Color de fondo del botón
        fg="white",    # Color del texto del botón
        relief=tk.RAISED,
        width=25,      # Ancho del botón, consistente con el estilo anterior
        height=2       # Altura del botón, consistente con el estilo anterior
    )
    boton_registrar.pack(pady=20)

    # Estilo del botón
    estilo = ttk.Style()
    estilo.configure("TButton", padding=6, relief="flat", background="#4CAF50", foreground="white")
    estilo.map("TButton", background=[("active", "#45a049")])

    ventana.mainloop()
