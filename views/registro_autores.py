import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from entities.Autor import Autor
import re

def abrir_ventana_registro_autores():
    ventana = tk.Toplevel()
    ventana.title("Registro de Autores")
    ventana.geometry("600x600+750+240")
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

    # Función para consultar los libros creados

    def consultar_autores():
        autores = Autor.obtener_autores_consulta()

        # Crear una nueva ventana para mostrar los libros
        ventana_autores = tk.Toplevel()
        ventana_autores.title("Consulta de autores")
        ventana_autores.geometry("1200x600+500+240")
        ventana_autores.configure(bg="#2c3e50")

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
        frame_contenedor = tk.Frame(ventana_autores, bg="#2c3e50")
        frame_contenedor.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Crear el Treeview para mostrar los libros
        tree = ttk.Treeview(frame_contenedor,
                            columns=("Id","Nombre", "Apellido", "Nacionalidad"),
                            show="headings")

        # Definir las columnas y encabezados
        tree.heading("Id", text="Id", anchor="center")
        tree.heading("Nombre", text="Nombre", anchor="center")
        tree.heading("Apellido", text="Apellido", anchor="center")
        tree.heading("Nacionalidad", text="Nacionalidad", anchor="center")

        # Definir la alineación de las columnas
        tree.column("Id", width=120, anchor="center")
        tree.column("Nombre", width=120, anchor="center")
        tree.column("Apellido", width=250, anchor="center")
        tree.column("Nacionalidad", width=150, anchor="center")


        # Insertar los autores en el Treeview
        for autor in autores:
            tree.insert("", tk.END, values=(autor[0],autor[1], autor[2], autor[3]))

        # Función para eliminar el autor seleccionado
        def eliminar_autor_seleccionado():
            # Obtener el id del autor seleccionado
            selected_item = tree.selection()
            if selected_item:
                id = tree.item(selected_item)["values"][0]
                confirmacion = messagebox.askyesno("Confirmación",
                                                   f"¿Estás seguro de que deseas eliminar el autor con el id: {id}?")
                if confirmacion:
                    Autor.eliminar_autor(id)
                    tree.delete(selected_item)
                    messagebox.showinfo("Éxito", "El autor ha sido eliminado correctamente.")
            else:
                messagebox.showwarning("Selección", "Por favor, selecciona un autor para eliminar.")

        # Crear el botón de eliminar debajo del Treeview
        boton_eliminar = tk.Button(ventana_autores, text="Eliminar Autor", command=eliminar_autor_seleccionado,
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
        text="Registrar Autor",
        command=registrar_autor,
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
        text="Consultar Autores Existentes",
        command=consultar_autores,
        bg="#005f8b",
        fg="white",
        font=("Helvetica", 12),
        width=25,
        height=2
    ).grid(row=14, column=0, columnspan=2, pady=10)

    ventana.mainloop()