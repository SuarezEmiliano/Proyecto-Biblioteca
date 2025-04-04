import tkinter as tk
from tkinter import font as tkfont

from views.registro_autores import abrir_ventana_registro_autores
from views.registro_libros import abrir_ventana_registro_libros
from views.registro_usuarios import abrir_ventana_registro_usuarios
from views.prestamo_libros import abrir_ventana_prestamo_libros
from views.devolucion_libros import abrir_ventana_devolucion_libros
from views.consulta_disponibilidad import abrir_ventana_consulta_disponibilidad
from views.reportes import abrir_ventana_reportes


def abrir_ventana():
    def manejar_opcion(opcion):
        if opcion == "Registro de Autores":
            abrir_ventana_registro_autores()
        elif opcion == "Registro de Libros":
            abrir_ventana_registro_libros()
        elif opcion == "Registro de Usuarios":
            abrir_ventana_registro_usuarios()
        elif opcion == "Préstamo de Libros":
            abrir_ventana_prestamo_libros()
        elif opcion == "Devolución de Libros":
            abrir_ventana_devolucion_libros()
        elif opcion == "Consulta de Disponibilidad":
            abrir_ventana_consulta_disponibilidad()
        elif opcion == "Reportes":
            abrir_ventana_reportes()

    # Crear la ventana del menú
    ventana = tk.Tk()
    ventana.title("ALEJANDRÍA - Menú Principal")
    ventana.geometry("600x600+750+240")
    ventana.configure(bg="#2c3e50")
    ventana.resizable(False, False)

    # Establecer una fuente personalizada
    fuente_titulo = tkfont.Font(family="Helvetica", size=16, weight="bold")
    fuente_boton = tkfont.Font(family="Helvetica", size=12)

    # Etiqueta de título
    label_titulo = tk.Label(ventana, text="ALEJANDRÍA - Menú Principal", font=fuente_titulo, bg="#2c3e50", fg="#ecf0f1")
    label_titulo.pack(pady=20)

    # Crear un marco para los botones
    frame_botones = tk.Frame(ventana, bg="#34495e")
    frame_botones.pack(pady=10)

    # Crear botones para cada opción con un diseño mejorado
    opciones = [
        "Registro de Autores",
        "Registro de Libros",
        "Registro de Usuarios",
        "Préstamo de Libros",
        "Devolución de Libros",
        "Consulta de Disponibilidad",
        "Reportes"
    ]

    for opcion in opciones:
        boton = tk.Button(
            frame_botones,
            text=opcion,
            font=fuente_boton,
            bg="#008B8B",
            fg="white",
            width=25,
            height=2,
            relief=tk.RAISED,
            command=lambda op=opcion: manejar_opcion(op)
        )
        boton.pack(pady=5)

    # Botón de salir
    boton_salir = tk.Button(
        ventana,
        text="Salir",
        font=fuente_boton,
        bg="#d9534f",
        fg="white",
        width=25,
        height=2,
        relief=tk.RAISED,
        command=ventana.destroy,
    )
    boton_salir.pack(pady=0)

    ventana.mainloop()
