import tkinter as tk
from tkinter import messagebox, ttk
from entities.Autor import Autor
from entities.Libro import Libro

def abrir_ventana_registro_libros():
    ventana = tk.Toplevel()
    ventana.title("Registro de Libros")
    ventana.geometry("400x400")

    # Obtener autores de la base de datos
    autores = Autor.obtener_autores()
    lista_autores = [(autor[0], autor[1]) for autor in autores]

    # Crear un marco para el formulario
    frame = tk.Frame(ventana, padx=20, pady=20)
    frame.pack(pady=20)

    tk.Label(frame, text="Registro de Libros", font=("Helvetica", 18)).grid(row=0, column=0, columnspan=2, pady=10)

    tk.Label(frame, text="ISBN:").grid(row=1, column=0, sticky="w")
    entry_isbn = tk.Entry(frame, width=30)
    entry_isbn.grid(row=1, column=1, pady=5)

    tk.Label(frame, text="Título:").grid(row=2, column=0, sticky="w")
    entry_titulo = tk.Entry(frame, width=30)
    entry_titulo.grid(row=2, column=1, pady=5)

    tk.Label(frame, text="Género:").grid(row=3, column=0, sticky="w")
    entry_genero = tk.Entry(frame, width=30)
    entry_genero.grid(row=3, column=1, pady=5)

    tk.Label(frame, text="Año de Publicación:").grid(row=4, column=0, sticky="w")
    entry_anio_publicacion = tk.Entry(frame, width=30)
    entry_anio_publicacion.grid(row=4, column=1, pady=5)

    tk.Label(frame, text="Autor:").grid(row=5, column=0, sticky="w")
    combobox_autores = ttk.Combobox(frame, values=[f"{autor[0]} - {autor[1]}" for autor in lista_autores], state="readonly")
    combobox_autores.grid(row=5, column=1, pady=5)

    tk.Label(frame, text="Cantidad Disponible:").grid(row=6, column=0, sticky="w")
    entry_cantidad_disponible = tk.Entry(frame, width=30)
    entry_cantidad_disponible.grid(row=6, column=1, pady=5)

    def registrar_libro():
        isbn = entry_isbn.get()
        titulo = entry_titulo.get()
        genero = entry_genero.get()
        anio_publicacion = entry_anio_publicacion.get()
        autor_seleccionado = combobox_autores.get()
        cantidad_disponible = entry_cantidad_disponible.get()

        if not isbn or not titulo or not genero or not anio_publicacion or not autor_seleccionado or not cantidad_disponible:
            messagebox.showwarning("Advertencia", "Por favor, completa todos los campos.")
            return

        # Obtener ID del autor seleccionado
        id_autor = autor_seleccionado.split(" - ")[0]

        # Aquí puedes crear la instancia del libro y guardar en la base de datos
        libro = Libro(isbn, titulo, genero, anio_publicacion, id_autor, cantidad_disponible)
        libro.guardar()

        messagebox.showinfo("Éxito", "Libro registrado con éxito!")

        # Limpiar los campos
        entry_isbn.delete(0, tk.END)
        entry_titulo.delete(0, tk.END)
        entry_genero.delete(0, tk.END)
        entry_anio_publicacion.delete(0, tk.END)
        entry_cantidad_disponible.delete(0, tk.END)
        combobox_autores.set('')

    boton_registrar = tk.Button(ventana, text="Registrar Libro", command=registrar_libro)
    boton_registrar.pack(pady=20)

    ventana.mainloop()