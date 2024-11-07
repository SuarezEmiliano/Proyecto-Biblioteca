import tkinter as tk
from tkinter import ttk
from entities.Autor import Autor
from entities.Libro import Libro
import re

def abrir_ventana_registro_libros():
    ventana = tk.Toplevel()
    ventana.title("Registro de Libros")
    ventana.geometry("500x500+750+240")
    ventana.configure(bg="#2c3e50")
    ventana.resizable(False, False)
    # Obtener autores de la base de datos
    autores = Autor.obtener_autores()
    lista_autores = [(autor[0], autor[1]) for autor in autores]

    # Crear un marco para el formulario
    frame = tk.Frame(ventana, bg="#34495e", padx=20, pady=20)
    frame.pack(pady=20)

    tk.Label(frame, text="Registro de Libros", font=("Helvetica", 18), bg="#34495e", fg="#ecf0f1").grid(row=0, column=0, columnspan=2, pady=10)

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
    combobox_autores = ttk.Combobox(frame, values=[f"{autor[0]} - {autor[1]}" for autor in lista_autores], width=28, state="readonly", font=("Helvetica", 12))
    combobox_autores.grid(row=9, column=1, pady=5)
    label_error_autor = tk.Label(frame, text="Debe seleccionar un autor", fg="red", bg="#34495e")
    label_error_autor.grid(row=10, column=1, sticky="w")
    label_error_autor.grid_remove()

    tk.Label(frame, text="Cantidad Disponible:", bg="#34495e", fg="#ecf0f1").grid(row=11, column=0, sticky="w")
    entry_cantidad_disponible = tk.Entry(frame, width=30, font=("Helvetica", 12))
    entry_cantidad_disponible.grid(row=11, column=1, pady=5)
    label_error_cantidad = tk.Label(frame, text="Debe ser un número entero", fg="red", bg="#34495e")
    label_error_cantidad.grid(row=12, column=1, sticky="w")
    label_error_cantidad.grid_remove()

    def validar_isbn(isbn):
        return len(isbn) == 13 and isbn.isdigit()

    def validar_titulo_o_genero(texto):
        return bool(re.fullmatch(r"[A-Za-záéíóúÁÉÍÓÚñÑ ]{1,20}", texto))

    def validar_anio(anio):
        return len(anio) == 4 and anio.isdigit()

    def validar_cantidad(cantidad):
        return cantidad.isdigit()

    def mostrar_confirmacion():
        confirmacion = tk.Toplevel()
        confirmacion.title("Confirmación")
        confirmacion.geometry("400x200+750+240")
        confirmacion.configure(bg="#2c3e50")

        tk.Label(confirmacion, text="Libro registrado con éxito!", font=("Helvetica", 14), bg="#2c3e50", fg="#ecf0f1").pack(pady=20)

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

        if not validar_anio(anio_publicacion):
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
            libro = Libro(isbn, titulo, genero, anio_publicacion, id_autor, cantidad_disponible)
            libro.guardar()

            # Mostrar la ventana de confirmación personalizada
            mostrar_confirmacion()

            # Limpiar los campos
            entry_isbn.delete(0, tk.END)
            entry_titulo.delete(0, tk.END)
            entry_genero.delete(0, tk.END)
            entry_anio_publicacion.delete(0, tk.END)
            entry_cantidad_disponible.delete(0, tk.END)
            combobox_autores.set('')

            # Cerrar la ventana de registro de libro
            ventana.destroy()

    # Botón de registro
    boton_registrar = tk.Button(
        ventana,
        text="Registrar Libro",
        command=registrar_libro,
        bg="#008B8B",
        fg="white",
        relief=tk.RAISED,
        width=25,
        height=2
    )
    boton_registrar.pack(pady=20)

    ventana.mainloop()