import tkinter as tk
from tkinter import messagebox, ttk
from entities.Prestamo import Prestamo
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generar_pdf(titulo, contenido, archivo):
    # Crear el documento PDF
    c = canvas.Canvas(archivo, pagesize=letter)
    c.setFont("Helvetica", 12)
    c.drawString(100, 750, titulo)

    # Escribir el contenido
    y_position = 730
    for linea in contenido:
        c.drawString(100, y_position, linea)
        y_position -= 20  # Ajustar la posición para cada línea

    # Guardar el archivo PDF
    c.save()

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
                contenido = [f"Usuario: {prestamo[0]} | Libro: {prestamo[1]} | Fecha préstamo: {prestamo[2]} | Fecha devolución: {prestamo[3]}" for prestamo in prestamos]
                # Mostrar los resultados en el Listbox
                for linea in contenido:
                    listbox_resultados.insert(tk.END, linea)
                # Mostrar el Listbox ahora que hay datos
                listbox_resultados.pack()
                # Generar el PDF
                generar_pdf("Prestamos Vencidos", contenido, "prestamos_vencidos.pdf")
                messagebox.showinfo("Reporte Generado", "El reporte de préstamos vencidos ha sido generado como PDF.")
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
                # Generar el PDF
                generar_pdf("Libros más prestados", contenido, "libros_mas_prestados.pdf")
                messagebox.showinfo("Reporte Generado", "El reporte de libros más prestados ha sido generado como PDF.")
            else:
                messagebox.showinfo("Libros más prestados", "No hay datos de libros prestados el último mes.")

        elif reporte_seleccionado == "Usuarios con más préstamos de libros":
            usuarios = Prestamo.obtener_usuarios_con_mas_prestamos()
            if usuarios:
                contenido = [f"Usuario: {usuario[0]} {usuario[1]} | Cantidad de préstamos: {usuario[2]}" for usuario in usuarios]
                # Mostrar los resultados en el Listbox
                for linea in contenido:
                    listbox_resultados.insert(tk.END, linea)
                # Mostrar el Listbox ahora que hay datos
                listbox_resultados.pack()
                # Generar el PDF
                generar_pdf("Usuarios con más préstamos", contenido, "usuarios_mas_prestamos.pdf")
                messagebox.showinfo("Reporte Generado", "El reporte de usuarios con más préstamos ha sido generado como PDF.")
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
