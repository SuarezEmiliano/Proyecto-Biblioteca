import tkinter as tk
from tkinter import messagebox, ttk
from entities.Autor import Autor  # Asegúrate de que esta ruta sea correcta


def abrir_ventana_registro_autores():
    ventana = tk.Toplevel()
    ventana.title("Registro de Autores")
    ventana.geometry("400x400")
    ventana.configure(bg="#2c3e50")  # Color de fondo más elegante

    # Crear un marco para el formulario
    frame = tk.Frame(ventana, bg="#34495e", padx=20, pady=20)
    frame.pack(pady=20)

    tk.Label(frame, text="Registro de Autores", font=("Helvetica", 18), bg="#34495e", fg="#ecf0f1").grid(row=0,
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

    tk.Label(frame, text="Nacionalidad:", bg="#34495e", fg="#ecf0f1").grid(row=3, column=0, sticky="w")
    entry_nacionalidad = tk.Entry(frame, width=30, font=("Helvetica", 12))
    entry_nacionalidad.grid(row=3, column=1, pady=5)


    # Función para manejar el registro del usuario
    def registrar_autor():
        nombre = entry_nombre.get()
        apellido = entry_apellido.get()
        nacionalidad = entry_nacionalidad.get()


        # Validar los campos
        if not nombre or not apellido or not nacionalidad:
            messagebox.showwarning("Advertencia", "Por favor, completa todos los campos.")
            return

        # Crear una instancia del usuario
        nuevo_usuario = Autor(id=None, nombre=nombre, apellido=apellido, nacionalidad=nacionalidad)

        # Aquí puedes añadir la lógica para guardar el usuario en la base de datos
        # Por ejemplo: guardar_autor_en_db(nuevo_autor)

        # Mostrar un mensaje de éxito
        messagebox.showinfo("Éxito", "Usuario registrado correctamente.")

        # Limpiar los campos
        entry_nombre.delete(0, tk.END)
        entry_apellido.delete(0, tk.END)
        entry_nacionalidad.delete(0, tk.END)



    # Botón para registrar el usuario
    boton_registrar = tk.Button(
        ventana,
        text="Registrar Autor",
        command=registrar_autor,
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
