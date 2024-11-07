import tkinter as tk
from tkinter import messagebox, ttk
from entities.Prestamo import Prestamo
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

def generar_pdf_prestamos_vencidos(prestamos):
    # Crear el documento PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Título del reporte
    pdf.cell(200, 10, txt="Reporte de Préstamos Vencidos", ln=True, align='C')

    # Agregar los datos de los préstamos vencidos
    for prestamo in prestamos:
        pdf.ln(10)
        pdf.cell(200, 10, txt=f"Usuario: {prestamo[0]} | Libro: {prestamo[1]} | Fecha préstamo: {prestamo[2]} | Fecha devolución: {prestamo[3]}", ln=True)

    # Guardar el archivo PDF
    pdf.output("reporte_prestamos_vencidos.pdf")
    mostrar_confirmacion()
    
def generar_pdf_usuarios_mas_prestamos(usuarios):
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

    # Calcular el centro de la página para la tabla
    ancho_tabla = 140
    pdf.set_x((210 - ancho_tabla) / 2)

    # Encabezados de la tabla
    pdf.cell(70, 10, txt="Usuario", border=1, align='C', fill=True)
    pdf.cell(70, 10, txt="Cantidad de Préstamos", border=1, align='C', fill=True)
    pdf.ln()

    # Cambiar a una fuente normal para los datos
    pdf.set_font("Arial", size=10)

    # Agregar los datos de los usuarios en las filas de la tabla
    for usuario in usuarios:
        pdf.set_x((210 - ancho_tabla) / 2) 

        pdf.cell(70, 10, txt=f"{usuario[0]} {usuario[1]}", border=1, align='C')
        pdf.cell(70, 10, txt=str(usuario[2]), border=1, align='C')
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
    ventana.geometry("500x500+750+240")
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
                    for prestamo in prestamos]
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
            usuarios = Prestamo.obtener_usuarios_con_mas_prestamos()
            if usuarios:
                contenido = [f"Usuario: {usuario[0]} {usuario[1]} | Cantidad de préstamos: {usuario[2]}" for usuario in
                             usuarios]
                # Mostrar los resultados en el Listbox
                for linea in contenido:
                    listbox_resultados.insert(tk.END, linea)
                # Mostrar el Listbox ahora que hay datos
                listbox_resultados.pack()
                # Generar el PDF para usuarios con más préstamos
                generar_pdf_usuarios_mas_prestamos(usuarios)
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
