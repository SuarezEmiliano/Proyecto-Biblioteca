import sqlite3
from datetime import datetime

from database.database import ConexionDB


class Prestamo:
    def __init__(self, id_usuario, isbn, fecha_prestamo, fecha_devolucion):
        self.id_usuario = id_usuario
        self.isbn = isbn
        self.fecha_prestamo = fecha_prestamo
        self.fecha_devolucion = fecha_devolucion

    def guardar(self):
        conn = ConexionDB().obtener_conexion()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO prestamos (id_usuario, isbn, fecha_prestamo, fecha_devolucion_estimada) 
            VALUES (?, ?, ?, ?)
        ''', (self.id_usuario, self.isbn, self.fecha_prestamo, self.fecha_devolucion))
        conn.commit()

    @staticmethod
    def obtener_prestamos():
        conn = ConexionDB().obtener_conexion()
        cursor = conn.cursor()
        cursor.execute('SELECT id_usuario, isbn FROM prestamos')
        prestamos = cursor.fetchall()
        return prestamos

    @staticmethod
    def obtener_prestamos_consulta():
        conn = ConexionDB().obtener_conexion()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM prestamos WHERE fecha_devolucion_real IS NULL')
        prestamos = cursor.fetchall()
        return prestamos

    # Función para obtener prestamos vencidos
    @staticmethod
    def obtener_prestamos_vencidos():
        conn = ConexionDB().obtener_conexion()
        cursor = conn.cursor()

        # Obtener la fecha actual
        fecha_actual = datetime.now().strftime('%Y-%m-%d')

        # Consulta para obtener préstamos vencidos
        cursor.execute('''
            SELECT p.id_usuario, l.titulo, p.fecha_prestamo, p.fecha_devolucion_estimada, p.fecha_devolucion_real
            FROM prestamos p
            JOIN libros l ON p.isbn = l.isbn
            WHERE (p.fecha_devolucion_estimada < ? AND p.fecha_devolucion_real IS NULL AND l.dado_de_baja = 0) 
            OR (p.fecha_devolucion_real > p.fecha_devolucion_estimada)
        ''', (fecha_actual,))

        # Obtener los resultados
        prestamos = cursor.fetchall()

        # Retornar los préstamos vencidos
        return prestamos

    # Función para obtener libros más prestados del último mes
    @staticmethod
    def obtener_libros_mas_prestados():
        conn = ConexionDB().obtener_conexion()
        cursor = conn.cursor()
        fecha_actual = datetime.now()
        fecha_inicio = (fecha_actual.replace(day=1)).strftime('%Y-%m-%d')
        cursor.execute('''
            SELECT l.titulo, COUNT(p.isbn) AS cantidad_prestamos 
            FROM prestamos p
            JOIN libros l ON p.isbn = l.isbn
            WHERE p.fecha_prestamo >= ? AND dado_de_baja = 0
            GROUP BY p.isbn
            ORDER BY cantidad_prestamos DESC
        ''', (fecha_inicio,))
        libros = cursor.fetchall()
        return libros

    # Función para obtener usuarios con más préstamos
    @staticmethod
    def obtener_usuarios_con_mas_prestamos():
        conn = ConexionDB().obtener_conexion()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT u.nombre, u.apellido, COUNT(p.id) AS cantidad_prestamos
            FROM prestamos p
            JOIN usuarios u ON p.id = u.id_usuario
            GROUP BY p.id
            ORDER BY cantidad_prestamos DESC
        ''')
        usuarios = cursor.fetchall()

        return usuarios

    @staticmethod
    def obtener_libros_prestados_por_usuario(id_usuario):
        conn = ConexionDB().obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM prestamos WHERE id_usuario = ?", (id_usuario,))
        cantidad_prestados = cursor.fetchone()[0]
        return cantidad_prestados

    @staticmethod
    def registrar_devolucion(id_prestamo, fecha_devolucion):
        conn = ConexionDB().obtener_conexion()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE prestamos 
            SET fecha_devolucion_real = ? 
            WHERE id = ?
        ''', (fecha_devolucion, id_prestamo))
        conn.commit()

    @staticmethod
    def obtener_codigo_libro(id_prestamo):
        conn = ConexionDB().obtener_conexion()
        cursor = conn.cursor()
        cursor.execute('SELECT isbn FROM prestamos WHERE id = ?', (id_prestamo,))
        isbn = cursor.fetchone()[0]
        return isbn

    @staticmethod
    def eliminar_prestamo(id):
        conn = ConexionDB().obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM prestamos WHERE id = ?", (id,))
        conn.commit()
