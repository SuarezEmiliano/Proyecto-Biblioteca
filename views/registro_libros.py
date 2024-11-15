import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from entities.Autor import Autor
from entities.Libro import Libro
import re
import datetime


def abrir_ventana_registro_libros():
    ventana = tk.Toplevel()
    ventana.title("Registro de Libros")
    ventana.geometry("600x600+750+240")
    ventana.configure(bg="#2c3e50")
    ventana.resizable(False, False)

    # Obtener autores de la base de datos
    autores = Autor.obtener_autores()
    lista_autores = [(autor[0], autor[1]) for autor in autores]

    # Crear un marco para el formulario
    frame = tk.Frame(ventana, bg="#34495e", padx=20, pady=20)
    frame.pack(pady=20)

    tk.Label(frame, text="Registro de Libros", font=("Helvetica", 18), bg="#34495e", fg="#ecf0f1").grid(row=0, column=0,
                                                                                                        columnspan=2,
                                                                                                        pady=10)

    # Campos de entrada para el formulario
    tk.Label(frame, text="ISBN:", bg="#34495e", fg="#ecf0f1").grid(row=1, column=0, sticky="w")
    entry_isbn = tk.Entry(frame, width=30, font=("Helvetica", 12))
    entry_isbn.grid(row=1, column=1, pady=5)
    label_error_isbn = tk.Label(frame, text="Debe ser 13 dígitos numéricos", fg="red", bg="#34495e")
    label_error_isbn.grid(row=2, column=1, sticky="w")
    label_error_isbn.grid_remove()

    tk.Label(frame, text="Título:", bg="#34495e", fg="#ecf0f1").grid(row=3, column=0, sticky="w")
    entry_titulo = tk.Entry(frame, width=30, font=("Helvetica", 12))
    entry_titulo.grid(row=3, column=1, pady=5)
    label_error_titulo = tk.Label(frame, text="Debe ser solo letras (1-20 caracteres)", fg="red", bg="#34495e")
    label_error_titulo.grid(row=4, column=1, sticky="w")
    label_error_titulo.grid_remove()

    tk.Label(frame, text="Género:", bg="#34495e", fg="#ecf0f1").grid(row=5, column=0, sticky="w")
    entry_genero = tk.Entry(frame, width=30, font=("Helvetica", 12))
    entry_genero.grid(row=5, column=1, pady=5)
    label_error_genero = tk.Label(frame, text="Debe ser solo letras (1-20 caracteres)", fg="red", bg="#34495e")
    label_error_genero.grid(row=6, column=1, sticky="w")
    label_error_genero.grid_remove()

    tk.Label(frame, text="Año de Publicación:", bg="#34495e", fg="#ecf0f1").grid(row=7, column=0, sticky="w")
    entry_anio_publicacion = tk.Entry(frame, width=30, font=("Helvetica", 12))
    entry_anio_publicacion.grid(row=7, column=1, pady=5)
    label_error_anio = tk.Label(frame, text="Debe ser un año de 4 dígitos", fg="red", bg="#34495e")
    label_error_anio.grid(row=8, column=1, sticky="w")
    label_error_anio.grid_remove()

    tk.Label(frame, text="Autor:", bg="#34495e", fg="#ecf0f1").grid(row=9, column=0, sticky="w")
    combobox_autores = ttk.Combobox(frame, values=[f"{autor[0]} - {autor[1]}" for autor in lista_autores], width=28,
                                    state="readonly", font=("Helvetica", 12))
    combobox_autores.grid(row=9, column=1, pady=5)
    label_error_autor = tk.Label(frame, text="Debe seleccionar un autor", fg="red", bg="#34495e")
    label_error_autor.grid(row=10, column=1, sticky="w")
    label_error_autor.grid_remove()

    tk.Label(frame, text="Cantidad Disponible:", bg="#34495e", fg="#ecf0f1").grid(row=11, column=0, sticky="w")
    entry_cantidad_disponible = tk.Entry(frame, width=30, font=("Helvetica", 12))
    entry_cantidad_disponible.grid(row=11, column=1, pady=5)
    label_error_cantidad = tk.Label(frame, text="Debe ser un número entero mayor o igual a 1", fg="red", bg="#34495e")
    label_error_cantidad.grid(row=12, column=1, sticky="w")
    label_error_cantidad.grid_remove()

    # Funciones de validación
    def validar_isbn(isbn):
        return len(isbn) == 13 and isbn.isdigit()

    def validar_titulo_o_genero(texto):
        return bool(re.fullmatch(r"[A-Za-záéíóúÁÉÍÓÚñÑ ]{1,30}", texto))

    def validar_anio(anio):
        """Valida que el año sea un número de cuatro dígitos y no sea mayor que el año actual."""
        anio_actual = datetime.datetime.now().year
        try:
            anio = int(anio)
            if len(str(anio)) != 4:
                return "Debe ser un año de 4 dígitos"
            elif anio > anio_actual:
                return "Debe ser un año menor o igual al actual"
            elif anio < 1000:
                return "Debe ser un año mayor a 1000"
            else:
                return True
        except ValueError:
            return "Debe ser un año de 4 dígitos"

    def validar_cantidad(cantidad):
        return cantidad.isdigit() and int(cantidad) >= 1

    def mostrar_confirmacion():
        confirmacion = tk.Toplevel()
        confirmacion.title("Confirmación")
        confirmacion.geometry("400x200+750+240")
        confirmacion.configure(bg="#2c3e50")

        tk.Label(confirmacion, text="Libro registrado con éxito!", font=("Helvetica", 14), bg="#2c3e50",
                 fg="#ecf0f1").pack(pady=20)

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

    def registrar_libro():
        isbn = entry_isbn.get()
        titulo = entry_titulo.get()
        genero = entry_genero.get()
        anio_publicacion = entry_anio_publicacion.get()
        autor_seleccionado = combobox_autores.get()
        cantidad_disponible = entry_cantidad_disponible.get()

        campos_validos = True

        if not validar_isbn(isbn):
            label_error_isbn.grid()
            campos_validos = False
        else:
            label_error_isbn.grid_remove()

        if not validar_titulo_o_genero(titulo):
            label_error_titulo.grid()
            campos_validos = False
        else:
            label_error_titulo.grid_remove()

        if not validar_titulo_o_genero(genero):
            label_error_genero.grid()
            campos_validos = False
        else:
            label_error_genero.grid_remove()

        resultado_anio = validar_anio(anio_publicacion)
        if resultado_anio is not True:
            label_error_anio.config(text=resultado_anio)
            label_error_anio.grid()
            campos_validos = False
        else:
            label_error_anio.grid_remove()

        if not autor_seleccionado:
            label_error_autor.grid()
            campos_validos = False
        else:
            label_error_autor.grid_remove()

        if not validar_cantidad(cantidad_disponible):
            label_error_cantidad.grid()
            campos_validos = False
        else:
            label_error_cantidad.grid_remove()

        if campos_validos:
            id_autor = autor_seleccionado.split(" - ")[0]
            libro = Libro(isbn, titulo, genero, anio_publicacion, id_autor, cantidad_disponible, cantidad_disponible)
            libro.guardar()
            mostrar_confirmacion()
            entry_isbn.delete(0, tk.END)
            entry_titulo.delete(0, tk.END)
            entry_genero.delete(0, tk.END)
            entry_anio_publicacion.delete(0, tk.END)
            entry_cantidad_disponible.delete(0, tk.END)
            combobox_autores.set('')

    # Función para consultar los libros creados
    def consultar_libros():
        libros = Libro.obtener_libros_consulta()

        # Crear una nueva ventana para mostrar los libros
        ventana_libros = tk.Toplevel()
        ventana_libros.title("Consulta de libros")
        ventana_libros.geometry("1200x600+500+240")
        ventana_libros.configure(bg="#2c3e50")

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
        frame_contenedor = tk.Frame(ventana_libros, bg="#2c3e50")
        frame_contenedor.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Crear el Treeview para mostrar los libros
        tree = ttk.Treeview(frame_contenedor,
                            columns=("ISBN", "Título", "Género", "Año", "Autor", "Cantidad Disponible"),
                            show="headings")

        # Definir las columnas y encabezados
        tree.heading("ISBN", text="ISBN", anchor="center")
        tree.heading("Título", text="Título", anchor="center")
        tree.heading("Género", text="Género", anchor="center")
        tree.heading("Año", text="Año", anchor="center")
        tree.heading("Autor", text="Autor", anchor="center")
        tree.heading("Cantidad Disponible", text="Cantidad Disponible", anchor="center")

        # Definir la alineación de las columnas
        tree.column("ISBN", width=120, anchor="center")
        tree.column("Título", width=250, anchor="center")
        tree.column("Género", width=150, anchor="center")
        tree.column("Año", width=100, anchor="center")
        tree.column("Autor", width=200, anchor="center")
        tree.column("Cantidad Disponible", width=150, anchor="center")

        # Insertar los libros en el Treeview
        for libro in libros:
            tree.insert("", tk.END, values=(libro[0], libro[1], libro[2], libro[3], libro[4], libro[5]))

        # Función para eliminar el libro seleccionado
        def eliminar_libro_seleccionado():
            # Obtener el ISBN del libro seleccionado
            selected_item = tree.selection()
            if selected_item:
                isbn = tree.item(selected_item)["values"][0]  # Obtener el ISBN
                confirmacion = messagebox.askyesno("Confirmación",
                                                   f"¿Estás seguro de que deseas eliminar el libro con ISBN {isbn}?")
                if confirmacion:
                    Libro.eliminar_libro(isbn)
                    tree.delete(selected_item)
                    messagebox.showinfo("Éxito", "El libro ha sido eliminado correctamente.")
            else:
                messagebox.showwarning("Selección", "Por favor, selecciona un libro para eliminar.")

        def baja_libros_danados():
            # Obtener el ISBN del libro seleccionado
            selected_item = tree.selection()
            if selected_item:
                isbn = tree.item(selected_item)["values"][0]  # Obtener el ISBN
                confirmacion = messagebox.askyesno("Confirmación",
                                                   f"¿Estás seguro de que deseas dar de baja el libro con ISBN {isbn}?")
                if confirmacion:
                    Libro.dar_de_baja(isbn)
                    tree.delete(selected_item)
                    messagebox.showinfo("Éxito", "El libro ha sido dado de baja correctamente.")
            else:
                messagebox.showwarning("Selección", "Por favor, selecciona un libro para dar de baja.")

        # Crear un Frame para centrar los botones
        frame_botones = tk.Frame(ventana_libros, bg="#2c3e50")
        frame_botones.pack(pady=10, anchor="center")

        # Crear el botón de eliminar debajo del Treeview
        boton_eliminar = tk.Button(frame_botones, text="Eliminar Libros", command=eliminar_libro_seleccionado,
                                   width=20, height=2, bg="#d9534f", fg="white", font=("Helvetica", 12))
        #boton_eliminar.pack(side="left", padx=5)

        boton_baja_danados = tk.Button(frame_botones, text="Dar de baja", command=baja_libros_danados,
                                       width=15, height=2, bg="#d9534f", fg="white", font=("Helvetica", 12))
        boton_baja_danados.pack(side="left", padx=5)

        # Agregar el Treeview al frame
        tree.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    def consultar_historico():
        libros = Libro.obtener_libros_historico()

        # Crear una nueva ventana para mostrar los libros
        ventana_libros = tk.Toplevel()
        ventana_libros.title("Consulta de libros")
        ventana_libros.geometry("1200x600+500+240")
        ventana_libros.configure(bg="#2c3e50")

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
        frame_contenedor = tk.Frame(ventana_libros, bg="#2c3e50")
        frame_contenedor.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Crear el Treeview para mostrar los libros
        tree = ttk.Treeview(frame_contenedor,
                            columns=("ISBN", "Título", "Género", "Año", "Autor", "Cantidad Disponible"),
                            show="headings")

        # Definir las columnas y encabezados
        tree.heading("ISBN", text="ISBN", anchor="center")
        tree.heading("Título", text="Título", anchor="center")
        tree.heading("Género", text="Género", anchor="center")
        tree.heading("Año", text="Año", anchor="center")
        tree.heading("Autor", text="Autor", anchor="center")
        tree.heading("Cantidad Disponible", text="Cantidad Disponible", anchor="center")

        # Definir la alineación de las columnas
        tree.column("ISBN", width=120, anchor="center")
        tree.column("Título", width=250, anchor="center")
        tree.column("Género", width=150, anchor="center")
        tree.column("Año", width=100, anchor="center")
        tree.column("Autor", width=200, anchor="center")
        tree.column("Cantidad Disponible", width=150, anchor="center")

        # Insertar los libros en el Treeview
        for libro in libros:
            tree.insert("", tk.END, values=(libro[0], libro[1], libro[2], libro[3], libro[4], libro[5]))

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
        text="Registrar Libro",
        command=registrar_libro,
        bg="#008B8B",
        fg="white",
        font=("Helvetica", 12),
        width=15,
        height=2
    )
    boton_registrar.grid(row=0, column=1, padx=10)

    # Botón para consultar libros
    tk.Button(
        frame,
        text="Consultar Libros Existentes",
        command=consultar_libros,
        bg="#005f8b",
        fg="white",
        font=("Helvetica", 12),
        width=25,
        height=2
    ).grid(row=14, column=0, columnspan=2, pady=10)

    # Botón para consultar historico
    tk.Button(
        frame,
        text="Consultar Historico",
        command=consultar_historico,
        bg="#005f8b",
        fg="white",
        font=("Helvetica", 12),
        width=25,
        height=2
    ).grid(row=15, column=0, columnspan=2, pady=10)

    ventana.mainloop()
