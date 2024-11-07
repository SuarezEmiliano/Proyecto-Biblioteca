import tkinter as tk
from entities.Autor import Autor
import re

def abrir_ventana_registro_autores():
    ventana = tk.Toplevel()
    ventana.title("Registro de Autores")
    ventana.geometry("+750+300")
    ventana.configure(bg="#2c3e50")
    ventana.resizable(False, False)

    # Crear un marco para el formulario
    frame = tk.Frame(ventana, bg="#34495e", padx=20, pady=20)
    frame.pack(pady=20)

    tk.Label(frame, text="Registro de Autores", font=("Helvetica", 18), bg="#34495e", fg="#ecf0f1").grid(row=0, column=0, columnspan=2, pady=10)

    # Campos de entrada para el formulario
    tk.Label(frame, text="Nombre:", bg="#34495e", fg="#ecf0f1").grid(row=1, column=0, sticky="w")
    entry_nombre = tk.Entry(frame, width=30, font=("Helvetica", 12))
    entry_nombre.grid(row=1, column=1, pady=5)
    label_error_nombre = tk.Label(frame, text="Debe ser letras (1-20 caracteres)", fg="red", bg="#34495e")
    label_error_nombre.grid(row=2, column=1, sticky="w")
    label_error_nombre.grid_remove()

    tk.Label(frame, text="Apellido:", bg="#34495e", fg="#ecf0f1").grid(row=3, column=0, sticky="w")
    entry_apellido = tk.Entry(frame, width=30, font=("Helvetica", 12))
    entry_apellido.grid(row=3, column=1, pady=5)
    label_error_apellido = tk.Label(frame, text="Debe ser letras (1-20 caracteres)", fg="red", bg="#34495e")
    label_error_apellido.grid(row=4, column=1, sticky="w")
    label_error_apellido.grid_remove()

    tk.Label(frame, text="Nacionalidad:", bg="#34495e", fg="#ecf0f1").grid(row=5, column=0, sticky="w")
    entry_nacionalidad = tk.Entry(frame, width=30, font=("Helvetica", 12))
    entry_nacionalidad.grid(row=5, column=1, pady=5)
    label_error_nacionalidad = tk.Label(frame, text="Debe ser letras (1-20 caracteres)", fg="red", bg="#34495e")
    label_error_nacionalidad.grid(row=6, column=1, sticky="w")
    label_error_nacionalidad.grid_remove()

    def validar_campo(texto):
        return bool(re.fullmatch(r"[A-Za-záéíóúÁÉÍÓÚñÑ ]{1,20}", texto))

    def mostrar_confirmacion():
        confirmacion = tk.Toplevel()
        confirmacion.title("Confirmación")
        confirmacion.geometry("400x200+750+240")

        confirmacion.configure(bg="#2c3e50")

        tk.Label(confirmacion, text="Autor registrado con éxito!", font=("Helvetica", 14), bg="#2c3e50", fg="#ecf0f1").pack(pady=20)

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

    def registrar_autor():
        nombre = entry_nombre.get()
        apellido = entry_apellido.get()
        nacionalidad = entry_nacionalidad.get()

        campos_validos = True

        if not validar_campo(nombre):
            label_error_nombre.grid()
            campos_validos = False
        else:
            label_error_nombre.grid_remove()

        if not validar_campo(apellido):
            label_error_apellido.grid()
            campos_validos = False
        else:
            label_error_apellido.grid_remove()

        if not validar_campo(nacionalidad):
            label_error_nacionalidad.grid()
            campos_validos = False
        else:
            label_error_nacionalidad.grid_remove()

        if campos_validos:
            autor = Autor(nombre=nombre, apellido=apellido, nacionalidad=nacionalidad)
            autor.guardar()

            # Mostrar la ventana de confirmación personalizada
            mostrar_confirmacion()

            # Limpiar los campos
            entry_nombre.delete(0, tk.END)
            entry_apellido.delete(0, tk.END)
            entry_nacionalidad.delete(0, tk.END)

            # Ocultar los mensajes de error
            label_error_nombre.grid_remove()
            label_error_apellido.grid_remove()
            label_error_nacionalidad.grid_remove()

            # Cerrar la ventana de registro de autor
            ventana.destroy()

    # Botón para registrar el autor
    boton_registrar = tk.Button(
        ventana,
        text="Registrar Autor",
        command=registrar_autor,
        bg="#008B8B",
        fg="white",
        relief=tk.RAISED,
        width=25,
        height=2
    )
    boton_registrar.pack(pady=20)

    ventana.mainloop()