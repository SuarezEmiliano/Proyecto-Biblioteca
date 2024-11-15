import tkinter as tk
from tkinter import messagebox, ttk
from entities.Autor import Autor
from entities.Libro import Libro
from entities.Prestamo import Prestamo
from entities.Usuario import Usuario
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
from fpdf import FPDF
from datetime import datetime

def mostrar_grafico(libros):
    # Convertir los datos en un DataFrame
    df = pd.DataFrame(libros, columns=["Libro", "Cantidad de préstamos"])

    # Crear el gráfico de barras
    plt.figure(figsize=(10, 6))
    sns.barplot(x="Cantidad de préstamos", y="Libro", data=df, palette="Blues_d")

    # Configurar el gráfico
    plt.title("Libros más prestados el último mes")
    plt.xlabel("Cantidad de Préstamos")
    plt.ylabel("Libro")

    # Guardar el gráfico como imagen PNG
    grafico_filename = "grafico_libros_prestados.png"
    plt.savefig(grafico_filename)
    plt.close()

    # Crear el archivo PDF
    pdf = FPDF()
    pdf.add_page()

    # Encabezado
    pdf.set_font("Arial", style='B', size=14)
    pdf.cell(200, 10, txt="Biblioteca Alejandría", ln=True, align='C')
    pdf.ln(5)

    # Dibuja la línea debajo del encabezado
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(10)

    # Título del reporte
    pdf.set_font("Arial", style='B', size=16)
    pdf.cell(200, 10, txt="Reporte de Libros Más Prestados el Último Mes", ln=True, align='C')
    pdf.ln(10)

    # Subtítulo
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(200, 10, txt="Detalle", ln=True, align='L')
    pdf.ln(5)

    # Agregar el gráfico al PDF (como imagen)
    pdf.image(grafico_filename, x=10, y=pdf.get_y(), w=180)

    pdf.ln(100)

    # Encabezado de la tabla
    pdf.set_font("Arial", 'B', 12)
    pdf.set_fill_color(0, 139, 139)
    pdf.ln(10)
    pdf.cell(100, 10, "Título del Libro", 1, 0, 'C', fill=True)
    pdf.cell(50, 10, "Cantidad de Préstamos", 1, 1, 'C', fill=True)

    # Cuerpo de la tabla
    pdf.set_font("Arial", size=10)
    for libro in libros:
        pdf.cell(100, 10, libro[0], 1, 0, 'C')
        pdf.cell(50, 10, str(libro[1]), 1, 1, 'C')

    # Guardar el PDF final con gráfico y tabla
    pdf.output("reporte_libros_prestados_grafico.pdf")

    # Eliminar la imagen temporal
    import os
    os.remove(grafico_filename)

    mostrar_confirmacion()

def generar_pdf_prestamos_vencidos(prestamos):
    # Crear el documento PDF
    pdf = FPDF()
    pdf.add_page()

    # Establecer el estilo de fuente para el encabezado
    pdf.set_font("Arial", style='B', size=14)

    # Encabezado (puedes agregar un logo o un texto adicional aquí si es necesario)
    pdf.cell(200, 10, txt="Biblioteca Alejandría", ln=True, align='C')
    pdf.ln(5)

    # Dibuja la línea debajo del encabezado
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())

    pdf.ln(10)

    # Título del reporte (centrado, en negrita y más grande)
    pdf.set_font("Arial", style='B', size=16)
    pdf.cell(200, 10, txt="Reporte de Préstamos Vencidos", ln=True, align='C')
    pdf.ln(10)

    # Subtítulo (en negrita)
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(200, 10, txt="Detalle", ln=True, align='L')
    pdf.ln(5)

    # Crear los encabezados de la tabla con un formato profesional
    pdf.set_font("Arial", style='B', size=12)
    pdf.set_fill_color(0, 139, 139)

    # Definir el ancho de las celdas
    ancho_isbn = 50  # Ancho para la columna ISBN
    ancho_fecha_prestamo = 40  # Ancho para la columna de fecha préstamo
    ancho_fecha_devolucion_estimada = 50  # Ancho para la columna de fecha devolución estimada
    ancho_fecha_devolucion_real = 50  # Ancho para la columna de fecha devolución real

    # Calcular el centro de la página para la tabla
    pdf.set_x((210 - (ancho_isbn + ancho_fecha_prestamo + ancho_fecha_devolucion_estimada + ancho_fecha_devolucion_real)) / 2)

    # Encabezados de la tabla
    pdf.cell(ancho_isbn, 10, txt="Libro", border=1, align='C', fill=True)
    pdf.cell(ancho_fecha_prestamo, 10, txt="Préstamo", border=1, align='C', fill=True)
    pdf.cell(ancho_fecha_devolucion_estimada, 10, txt="Devolución Estimada", border=1, align='C', fill=True)
    pdf.cell(ancho_fecha_devolucion_real, 10, txt="Devolución Real", border=1, align='C', fill=True)
    pdf.ln()

    # Cambiar a una fuente normal para los datos
    pdf.set_font("Arial", size=10)

    # Agregar los datos de los préstamos en las filas de la tabla
    for prestamo in prestamos:
        isbn = str(prestamo[1])  # Convertir a cadena
        fecha_prestamo = str(prestamo[2])  # Convertir a cadena
        fecha_devolucion_estimada = str(prestamo[3])  # Convertir a cadena
        fecha_devolucion_real = str(prestamo[4]) if prestamo[4] is not None else "No entregado aún"  # Convertir a cadena

        # Establecer la posición X para el PDF
        pdf.set_x((210 - (
                    ancho_isbn + ancho_fecha_prestamo + ancho_fecha_devolucion_estimada + ancho_fecha_devolucion_real)) / 2)

        # Agregar las celdas al PDF
        pdf.cell(ancho_isbn, 10, txt=isbn, border=1, align='C')
        pdf.cell(ancho_fecha_prestamo, 10, txt=fecha_prestamo, border=1, align='C')
        pdf.cell(ancho_fecha_devolucion_estimada, 10, txt=fecha_devolucion_estimada, border=1, align='C')
        pdf.cell(ancho_fecha_devolucion_real, 10, txt=fecha_devolucion_real, border=1, align='C')
        pdf.ln()

    # Pie de página
    pdf.set_y(-30)
    pdf.set_font("Arial", style='I', size=8)

    # Agregar la fecha y hora al pie de página
    pdf.cell(0, 10, txt=f"Fecha de generación: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", ln=True, align='C')

    # Mensaje de derechos reservados
    pdf.cell(0, 10, txt="Reporte generado automáticamente. Todos los derechos reservados.", align='C')

    # Guardar el archivo PDF
    pdf.output("reporte_prestamos_vencidos.pdf")
    mostrar_confirmacion()

def generar_pdf_usuarios_mas_prestamos(usuarios):
    # Creamos una lista con los usuarios y sus respectivas cantidades de préstamos
    usuarios_con_prestamos = []

    for usuario in usuarios:
        nombre_usuario = usuario[0]
        apellido_usuario = usuario[1]

        # Obtener el ID del usuario por su nombre y apellido
        id_usuario = Usuario.obtener_id_usuario_por_nombre_apellido(nombre_usuario, apellido_usuario)

        # Obtener la cantidad de préstamos del usuario
        cantidad_prestamos = Prestamo.obtener_libros_prestados_por_usuario(id_usuario)

        # Añadir el usuario y su cantidad de préstamos a la lista
        usuarios_con_prestamos.append((nombre_usuario, apellido_usuario, cantidad_prestamos))

    # Ordenar la lista de usuarios por la cantidad de préstamos en orden descendente
    usuarios_con_prestamos.sort(key=lambda x: x[2], reverse=True)

    # Crear el documento PDF
    pdf = FPDF()
    pdf.add_page()

    # Establecer el estilo de fuente para el encabezado
    pdf.set_font("Arial", style='B', size=14)

    # Encabezado (puedes agregar un logo o un texto adicional aquí si es necesario)
    pdf.cell(200, 10, txt="Biblioteca Alejandría", ln=True, align='C')
    pdf.ln(5)

    # Dibuja la línea debajo del encabezado
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())

    pdf.ln(10)

    # Título del reporte (centrado, en negrita y más grande)
    pdf.set_font("Arial", style='B', size=16)
    pdf.cell(200, 10, txt="Reporte de Usuarios con Más Préstamos", ln=True, align='C')
    pdf.ln(10)

    # Subtítulo (en negrita)
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(200, 10, txt="Detalle", ln=True, align='L')
    pdf.ln(5)

    # Crear los encabezados de la tabla con un formato profesional
    pdf.set_font("Arial", style='B', size=12)
    pdf.set_fill_color(0, 139, 139)

    # Definir el ancho de las celdas
    ancho_usuario = 80  # Ancho para la columna de usuario
    ancho_prestamos = 50  # Ancho para la columna de cantidad de préstamos

    # Calcular el centro de la página para la tabla
    pdf.set_x((210 - (ancho_usuario + ancho_prestamos)) / 2)

    # Encabezados de la tabla
    pdf.cell(ancho_usuario, 10, txt="Usuario", border=1, align='C', fill=True)
    pdf.cell(ancho_prestamos, 10, txt="Cantidad de Préstamos", border=1, align='C', fill=True)
    pdf.ln()

    # Cambiar a una fuente normal para los datos
    pdf.set_font("Arial", size=10)

    # Agregar los datos de los usuarios en las filas de la tabla
    for usuario in usuarios_con_prestamos:
        # usuario[0] -> nombre_usuario, usuario[1] -> apellido_usuario, usuario[2] -> cantidad_prestamos
        nombre_usuario = usuario[0]
        apellido_usuario = usuario[1]
        cantidad_prestamos = usuario[2]

        # Escribir los datos del usuario en la tabla
        pdf.set_x((210 - (ancho_usuario + ancho_prestamos)) / 2)
        pdf.cell(ancho_usuario, 10, txt=f"{nombre_usuario} {apellido_usuario}", border=1, align='C')
        pdf.cell(ancho_prestamos, 10, txt=str(cantidad_prestamos), border=1, align='C')
        pdf.ln()

    # Pie de página
    pdf.set_y(-30)
    pdf.set_font("Arial", style='I', size=8)

    # Agregar la fecha y hora al pie de página
    pdf.cell(0, 10, txt=f"Fecha de generación: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", ln=True, align='C')

    # Mensaje de derechos reservados
    pdf.cell(0, 10, txt="Reporte generado automáticamente. Todos los derechos reservados.", align='C')

    # Guardar el archivo PDF
    pdf.output("reporte_usuarios_mas_prestamos.pdf")
    mostrar_confirmacion()

def generar_pdf_autores_libros_disponibilidad(autores_libros):
    """Genera un reporte en PDF con la lista de autores, libros y su disponibilidad."""
    # Crear el documento PDF
    pdf = FPDF()
    pdf.add_page()

    # Establecer el estilo de fuente para el encabezado
    pdf.set_font("Arial", style='B', size=14)

    # Encabezado (puedes agregar un logo o un texto adicional aquí si es necesario)
    pdf.cell(200, 10, txt="Biblioteca Alejandría", ln=True, align='C')
    pdf.ln(5)

    # Dibuja la línea debajo del encabezado
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())

    pdf.ln(10)

    # Título del reporte (centrado, en negrita y más grande)
    pdf.set_font("Arial", style='B', size=16)
    pdf.cell(200, 10, txt="Reporte de Autores, Libros y Disponibilidad", ln=True, align='C')
    pdf.ln(10)

    # Subtítulo (en negrita)
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(200, 10, txt="Detalle", ln=True, align='L')
    pdf.ln(5)

    # Crear los encabezados de la tabla con un formato profesional
    pdf.set_font("Arial", style='B', size=12)
    pdf.set_fill_color(0, 139, 139)

    # Definir el ancho de las celdas
    ancho_autor = 60
    ancho_libro = 80 
    ancho_disponibilidad = 50

    # Calcular el centro de la página para la tabla
    pdf.set_x((210 - (ancho_autor + ancho_libro + ancho_disponibilidad)) / 2)

    # Encabezados de la tabla
    pdf.cell(ancho_autor, 10, txt="Autor", border=1, align='C', fill=True)
    pdf.cell(ancho_libro, 10, txt="Libro", border=1, align='C', fill=True)
    pdf.cell(ancho_disponibilidad, 10, txt="Disponibilidad", border=1, align='C', fill=True)
    pdf.ln()

    # Cambiar a una fuente normal para los datos
    pdf.set_font("Arial", size=10)

    # Agregar los datos de los autores, libros y su disponibilidad en las filas de la tabla
    for item in autores_libros:
        pdf.cell(ancho_autor, 10, txt=item['autor'], border=1, align='C')
        pdf.cell(ancho_libro, 10, txt=item['libro'], border=1, align='C')
        pdf.cell(ancho_disponibilidad, 10, txt=item['disponibilidad'], border=1, align='C')
        pdf.ln()

    # Agregar pie de página
    pdf.set_y(-30)
    pdf.set_font("Arial", style='I', size=8)
    pdf.cell(0, 10, txt=f"Fecha de generación: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", ln=True, align='C')
    pdf.cell(0, 10, txt="Reporte generado automáticamente. Todos los derechos reservados.", align='C')

    # Guardar el archivo PDF
    nombre_archivo = f"reporte_autores_libros_disponibilidad.pdf"
    pdf.output(nombre_archivo)
    
    # Mostrar confirmación
    mostrar_confirmacion()

def obtener_autores_y_libros_disponibles():
    # Obtener todos los autores
    autores = Autor.obtener_autores()
    
    # Crear una lista para almacenar los resultados
    autores_y_libros_disponibles = []

    # Para cada autor, obtener los libros disponibles para ese autor
    for autor in autores:
        id_autor, nombre_autor = autor
        
        # Obtener los libros disponibles para este autor
        libros = Libro.obtener_libros_disponibles_por_autor(id_autor)
        
        # Si el autor tiene libros disponibles
        if libros:
            for libro in libros:
                isbn, titulo, cantidad_disponible = libro
                
                # Almacenar el resultado en la lista con las claves correctas
                autores_y_libros_disponibles.append({
                    "autor": nombre_autor,
                    "libro": titulo,  # Nombre del libro
                    "disponibilidad": str(cantidad_disponible)  # Disponibilidad del libro
                })
    return autores_y_libros_disponibles

def mostrar_confirmacion():
    confirmacion = tk.Toplevel()
    confirmacion.title("Confirmación")
    confirmacion.geometry("400x200+750+240")
    confirmacion.configure(bg="#2c3e50")

    tk.Label(confirmacion, text="Reporte Generado con éxito!", font=("Helvetica", 14), bg="#2c3e50", fg="#ecf0f1").pack(pady=20)
    tk.Label(confirmacion, text="El reporte ha sido guardado como PDF.", font=("Helvetica", 12), bg="#2c3e50", fg="#ecf0f1").pack(pady=20)

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

def abrir_ventana_reportes():
    ventana = tk.Toplevel()
    ventana.title("Reportes")
    ventana.geometry("600x600+750+240")
    ventana.configure(bg="#2c3e50")

    # Crear un marco para el formulario
    frame = tk.Frame(ventana, bg="#34495e", padx=20, pady=20)
    frame.pack(pady=20)

    tk.Label(frame, text="Generar Reportes", font=("Helvetica", 18), bg="#34495e", fg="#ecf0f1").grid(
        row=0, column=0, columnspan=2, pady=10
    )

    # Listbox para mostrar los resultados (inicialmente oculto)
    listbox_resultados = tk.Listbox(ventana, width=80, height=15, font=("Helvetica", 10))
    listbox_resultados.pack(pady=20)
    listbox_resultados.pack_forget()

    # Función para mostrar los reportes
    def generar_reporte():
        reporte_seleccionado = combobox_reportes.get()

        # Limpiar el Listbox antes de agregar nuevos datos
        listbox_resultados.delete(0, tk.END)

        if reporte_seleccionado == "Prestamos vencidos":
            prestamos = Prestamo.obtener_prestamos_vencidos()
            if prestamos:
                generar_pdf_prestamos_vencidos(prestamos)
            else:
                messagebox.showinfo("Préstamos Vencidos", "No hay prestamos vencidos.")

        elif reporte_seleccionado == "Libros más prestados el último mes":
            libros = Prestamo.obtener_libros_mas_prestados()
            if libros:
                mostrar_grafico(libros)
            else:
                messagebox.showinfo("Libros más prestados", "No hay datos de libros prestados el último mes.")

        elif reporte_seleccionado == "Usuarios con más préstamos de libros":
            usuarios = Usuario.obtener_usuarios()
            usuarios_con_prestamos = []
            for usuario in usuarios:
                id_usuario = usuario[0]
                nombre_y_apellido = Usuario.obtener_nombre_apellido(id_usuario)
                nombre_usuario = nombre_y_apellido[0]
                apellido_usuario = nombre_y_apellido[1]

                # Obtener la cantidad de préstamos del usuario
                cantidad_prestamos = Prestamo.obtener_libros_prestados_por_usuario(id_usuario)

                # Añadir el usuario y su cantidad de préstamos a la lista
                usuarios_con_prestamos.append((nombre_usuario, apellido_usuario, cantidad_prestamos))
            usuarios_con_prestamos.sort(key=lambda x: x[2], reverse=True)
            if usuarios_con_prestamos:
                # Generar el PDF para los usuarios con más préstamos
                generar_pdf_usuarios_mas_prestamos(usuarios_con_prestamos)
            else:
                messagebox.showinfo("Usuarios con más préstamos", "No hay usuarios con préstamos registrados.")

        elif reporte_seleccionado == "Autores y Libros Disponibles":
            # Aquí asumimos que se obtiene una lista de autores, libros y su disponibilidad.
            autores_libros = obtener_autores_y_libros_disponibles()
            if autores_libros:
                # Llamamos a la función para generar el PDF con los autores, libros y disponibilidad
                generar_pdf_autores_libros_disponibilidad(autores_libros)
            else:
                messagebox.showinfo("Autores y Libros Disponibles", "No hay libros disponibles en este momento.")

        else:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un reporte.")

    # Combobox para seleccionar el reporte
    tk.Label(frame, text="Seleccionar Reporte:", bg="#34495e", fg="#ecf0f1").grid(row=1, column=0, sticky="w")
    combobox_reportes = ttk.Combobox(frame, values=[
        "Prestamos vencidos",
        "Libros más prestados el último mes",
        "Usuarios con más préstamos de libros",
        "Autores y Libros Disponibles"
    ], state="readonly", width=40)
    combobox_reportes.grid(row=1, column=1, pady=5)

    # Marco para los botones de "Cancelar" y "Registrar"
    frame_botones = tk.Frame(ventana, bg="#2c3e50")
    frame_botones.pack(pady=20)

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

    boton_generar_reporte = tk.Button(
        frame_botones,
        text="Generar reporte",
        command=generar_reporte,
        bg="#008B8B",
        fg="white",
        font=("Helvetica", 12),
        width=15,
        height=2
    )
    boton_generar_reporte.grid(row=0, column=1, padx=10)

    ventana.mainloop()
