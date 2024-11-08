import tkinter as tk
from tkinter import messagebox, ttk
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
    sns.barplot(x="Cantidad de préstamos", y="Libro", data=df, palette="Blues_d", hue="Libro")

    # Configurar el gráfico
    plt.title("Libros más prestados el último mes")
    plt.xlabel("Cantidad de Préstamos")
    plt.ylabel("Libro")

    # Guardar el gráfico como un archivo PDF
    with PdfPages('reporte_libros_prestados.pdf') as pdf:
        pdf.savefig()
        plt.close()

    mostrar_confirmacion()

def esta_vencido(fecha_devolucion_estimada, fecha_devolucion_real=None):
    # Convertir las fechas de string a objetos datetime
    fecha_devolucion_estimada = datetime.strptime(fecha_devolucion_estimada, "%Y-%m-%d")

    if fecha_devolucion_real:
        # Convertir la fecha real a datetime si se ha proporcionado
        fecha_devolucion_real = datetime.strptime(fecha_devolucion_real, "%Y-%m-%d")
        # El préstamo está vencido si la fecha de devolución real es posterior a la estimada
        return fecha_devolucion_real > fecha_devolucion_estimada
    else:
        # Si no se tiene fecha de devolución real, el préstamo está vencido si la estimada ha pasado
        return fecha_devolucion_estimada < datetime.now()

def generar_pdf_prestamos_vencidos(prestamos):
    # Crear el documento PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Título del reporte
    pdf.cell(200, 10, txt="Reporte de Préstamos Vencidos", ln=True, align='C')

    # Agregar los datos de los préstamos vencidos
    for prestamo in prestamos:
        usuario = prestamo[0]
        libro = prestamo[1]
        fecha_prestamo = prestamo[2]
        fecha_devolucion_estimada = prestamo[3]
        fecha_devolucion_real = prestamo[4]

        # Verificar si el préstamo está vencido
        if esta_vencido(fecha_devolucion_estimada, fecha_devolucion_real):
            pdf.ln(10)
            pdf.cell(200, 10, txt=f"Usuario: {usuario} | Libro: {libro} | Fecha préstamo: {fecha_prestamo} | Fecha devolución estimada: {fecha_devolucion_estimada} | Fecha devolución real: {fecha_devolucion_real or 'No registrada'}", ln=True)

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
                contenido = [
                    f"Usuario: {prestamo[0]} | Libro: {prestamo[1]} | Fecha préstamo: {prestamo[2]} | Fecha devolución: {prestamo[3]}"
                    for prestamo in prestamos
                ]
                # Mostrar los resultados en el Listbox
                for linea in contenido:
                    listbox_resultados.insert(tk.END, linea)
                # Mostrar el Listbox ahora que hay datos
                listbox_resultados.pack()
                # Generar el PDF para préstamos vencidos
                generar_pdf_prestamos_vencidos(prestamos)
            else:
                messagebox.showinfo("Préstamos Vencidos", "No hay prestamos vencidos.")

        elif reporte_seleccionado == "Libros más prestados el último mes":
            libros = Prestamo.obtener_libros_mas_prestados()
            if libros:
                contenido = [f"Libro: {libro[0]} | Cantidad de préstamos: {libro[1]}" for libro in libros]
                # Mostrar los resultados en el Listbox
                for linea in contenido:
                    listbox_resultados.insert(tk.END, linea)
                # Mostrar el Listbox ahora que hay datos
                listbox_resultados.pack()
                # Mostrar el gráfico de barras y guardarlo como PDF
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
                contenido = [
                    f"Usuario: {usuario[0]} {usuario[1]} | Cantidad de préstamos: {usuario[2]}"
                    for usuario in usuarios_con_prestamos
                ]
                # Mostrar los resultados en el Listbox
                for linea in contenido:
                    listbox_resultados.insert(tk.END, linea)
                # Mostrar el Listbox ahora que hay datos
                listbox_resultados.pack()

                # Generar el PDF para los usuarios con más préstamos
                generar_pdf_usuarios_mas_prestamos(usuarios_con_prestamos)
            else:
                messagebox.showinfo("Usuarios con más préstamos", "No hay usuarios con préstamos registrados.")

        else:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un reporte.")

    # Combobox para seleccionar el reporte
    tk.Label(frame, text="Seleccionar Reporte:", bg="#34495e", fg="#ecf0f1").grid(row=1, column=0, sticky="w")
    combobox_reportes = ttk.Combobox(frame, values=[
        "Prestamos vencidos",
        "Libros más prestados el último mes",
        "Usuarios con más préstamos de libros"
    ], state="readonly", width=40)
    combobox_reportes.grid(row=1, column=1, pady=5)

    # Botón para generar el reporte
    boton_generar_reporte = tk.Button(
        ventana,
        text="Generar Reporte",
        command=generar_reporte,
        bg="#008B8B",
        fg="white",
        relief=tk.RAISED,
        width=25,
        height=2
    )
    boton_generar_reporte.pack(pady=20)

    ventana.mainloop()
