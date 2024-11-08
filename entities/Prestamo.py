import sqlite3
from datetime import datetime


class Prestamo:
    def __init__(self, id_usuario, isbn, fecha_prestamo, fecha_devolucion):
        self.id_usuario = id_usuario
        self.isbn = isbn
        self.fecha_prestamo = fecha_prestamo
        self.fecha_devolucion = fecha_devolucion

    def guardar(self):
        conn = sqlite3.connect('biblioteca.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO prestamos (id_usuario, isbn, fecha_prestamo, fecha_devolucion_estimada) 
            VALUES (?, ?, ?, ?)
        ''', (self.id_usuario, self.isbn, self.fecha_prestamo, self.fecha_devolucion))
        conn.commit()
        conn.close()

    @staticmethod
    def obtener_prestamos():
        conn = sqlite3.connect('biblioteca.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id_usuario, isbn FROM prestamos')
        prestamos = cursor.fetchall()
        conn.close()
        return prestamos

    # Función para obtener prestamos vencidos
    @staticmethod
    def obtener_prestamos_vencidos():
        conn = sqlite3.connect('biblioteca.db')
        cursor = conn.cursor()
        fecha_actual = datetime.now().strftime('%Y-%m-%d')
        cursor.execute('''
            SELECT p.id_usuario, l.titulo, p.fecha_prestamo, p.fecha_devolucion_estimada 
            FROM prestamos p
            JOIN libros l ON p.isbn = l.isbn
            WHERE p.fecha_devolucion_estimada < ? AND p.fecha_devolucion_estimada IS NOT NULL
        ''', (fecha_actual,))
        prestamos = cursor.fetchall()
        conn.close()
        return prestamos

    # Función para obtener libros más prestados del último mes
    @staticmethod
    def obtener_libros_mas_prestados():
        conn = sqlite3.connect('biblioteca.db')
        cursor = conn.cursor()
        fecha_actual = datetime.now()
        fecha_inicio = (fecha_actual.replace(day=1)).strftime('%Y-%m-%d')  # Primer día del mes actual
        cursor.execute('''
            SELECT l.titulo, COUNT(p.isbn) AS cantidad_prestamos 
            FROM prestamos p
            JOIN libros l ON p.isbn = l.isbn
            WHERE p.fecha_prestamo >= ?
            GROUP BY p.isbn
            ORDER BY cantidad_prestamos DESC
        ''', (fecha_inicio,))
        libros = cursor.fetchall()
        conn.close()
        return libros

    # Función para obtener usuarios con más préstamos
    @staticmethod
    def obtener_usuarios_con_mas_prestamos():
        conn = sqlite3.connect('biblioteca.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT u.nombre, u.apellido, COUNT(p.id_usuario) AS cantidad_prestamos
            FROM prestamos p
            JOIN usuarios u ON p.id_usuario = u.id_usuario
            GROUP BY p.id_usuario
            ORDER BY cantidad_prestamos DESC
        ''')
        usuarios = cursor.fetchall()
        conn.close()
        return usuarios

    # Función para obtener préstamos pendientes
    @staticmethod
    def obtener_prestamos_pendientes():
        conn = sqlite3.connect('biblioteca.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT p.id_usuario, l.titulo, p.fecha_prestamo, p.fecha_devolucion_estimada 
            FROM prestamos p
            JOIN libros l ON p.isbn = l.isbn
            WHERE p.fecha_devolucion_real IS NULL
        ''')
        prestamos_pendientes = cursor.fetchall()
        conn.close()
        return prestamos_pendientes