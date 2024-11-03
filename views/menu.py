import tkinter as tk
from tkinter import font as tkFont
from .registro_autores import abrir_ventana_registro_autores
from .registro_libros import abrir_ventana_registro_libros
from .registro_usuarios import abrir_ventana_registro_usuarios
from .prestamo_libros import abrir_ventana_prestamo_libros
from .devolucion_libros import abrir_ventana_devolucion_libros
from .consulta_disponibilidad import abrir_ventana_consulta_disponibilidad
from .reportes import abrir_ventana_reportes

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
    ventana.title("Biblioteca - Menú Principal")
    ventana.geometry("400x500")
    ventana.configure(bg="#f0f0f0")  # Fondo claro
    ventana.resizable(False, False)  # No permitir redimensionar

    # Establecer una fuente personalizada
    fuente_titulo = tkFont.Font(family="Helvetica", size=16, weight="bold")
    fuente_boton = tkFont.Font(family="Helvetica", size=12)

    # Etiqueta de título
    label_titulo = tk.Label(ventana, text="Sistema de Biblioteca", font=fuente_titulo, bg="#f0f0f0")
    label_titulo.pack(pady=20)

    # Crear un marco para los botones
    frame_botones = tk.Frame(ventana, bg="#f0f0f0")
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
        bg="#f44336",
        fg="white",
        width=10,
        height=1,
        relief=tk.RAISED,
        command=ventana.destroy
    )
    boton_salir.pack(pady=20)

    ventana.mainloop()
