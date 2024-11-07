import tkinter as tk
from tkinter import messagebox, ttk
from entities.Prestamo import Prestamo
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages  # Importa PdfPages
from fpdf import FPDF  # Importa la librería FPDF


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
        pdf.savefig()  # Guarda la figura actual en el archivo PDF
        plt.close()  # Cierra la figura para liberar memoria

    messagebox.showinfo("Reporte Generado", "El gráfico ha sido guardado como un archivo PDF.")


def generar_pdf_prestamos_vencidos(prestamos):
    # Crear el documento PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Título del reporte
    pdf.cell(200, 10, txt="Reporte de Préstamos Vencidos", ln=True, align='C')

    # Agregar los datos de los préstamos vencidos
    for prestamo in prestamos:
        pdf.ln(10)  # Salto de línea
        pdf.cell(200, 10, txt=f"Usuario: {prestamo[0]} | Libro: {prestamo[1]} | Fecha préstamo: {prestamo[2]} | Fecha devolución: {prestamo[3]}", ln=True)

    # Guardar el archivo PDF
    pdf.output("reporte_prestamos_vencidos.pdf")
    messagebox.showinfo("Reporte Generado", "El reporte de préstamos vencidos ha sido guardado como PDF.")


def generar_pdf_usuarios_mas_prestamos(usuarios):
    # Crear el documento PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Título del reporte
    pdf.cell(200, 10, txt="Reporte de Usuarios con Más Préstamos", ln=True, align='C')

    # Agregar los datos de los usuarios
    for usuario in usuarios:
        pdf.ln(10)  # Salto de línea
        pdf.cell(200, 10, txt=f"Usuario: {usuario[0]} {usuario[1]} | Cantidad de préstamos: {usuario[2]}", ln=True)

    # Guardar el archivo PDF
    pdf.output("reporte_usuarios_mas_prestamos.pdf")
    messagebox.showinfo("Reporte Generado", "El reporte de usuarios con más préstamos ha sido guardado como PDF.")


def abrir_ventana_reportes():
    ventana = tk.Toplevel()
    ventana.title("Reportes")
    ventana.geometry("600x600")
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
    listbox_resultados.pack_forget()  # Ocultar el Listbox al principio

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
                messagebox.showinfo("Prestamos Vencidos", "No hay prestamos vencidos.")

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
    ], state="readonly")
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
