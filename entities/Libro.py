import sqlite3

from database.database import ConexionDB


class Libro:
    def __init__(self, isbn, titulo, genero, anio_publicacion, id_autor, cantidad_disponible, cantidad_buen_estado, dado_de_baja):
        self.isbn = isbn
        self.titulo = titulo
        self.genero = genero
        self.anio_publicacion = anio_publicacion
        self.id_autor = id_autor
        self.cantidad_disponible = cantidad_disponible
        self.cantidad_buen_estado = cantidad_buen_estado
        self.dado_de_baja = dado_de_baja

    def guardar(self):
        conn = ConexionDB().obtener_conexion()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO libros (isbn, titulo, genero, anio_publicacion, 
                id_autor, cantidad_disponible, cantidad_buen_estado, dado_de_baja) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (self.isbn, self.titulo, self.genero, self.anio_publicacion,
              self.id_autor, self.cantidad_disponible, self.cantidad_buen_estado, self.dado_de_baja))
        conn.commit()

    @staticmethod
    def obtener_libros_disponibles():
        conn = ConexionDB().obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT isbn, titulo FROM libros WHERE cantidad_disponible > 0 AND dado_de_baja = 0")
        libros = cursor.fetchall()
        return libros

    @staticmethod
    def obtener_libros_consulta():
        conn = ConexionDB().obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT *, titulo FROM libros WHERE dado_de_baja = 0")
        libros = cursor.fetchall()
        return libros

    @staticmethod
    def obtener_libros_historico():
        conn = ConexionDB().obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT *, titulo FROM libros WHERE dado_de_baja = 1")
        libros = cursor.fetchall()
        return libros

    @staticmethod
    def obtener_cantidad_disponible(isbn):
        conn = ConexionDB().obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT cantidad_disponible FROM libros WHERE isbn = ? AND dado_de_baja = 0", (isbn,))
        cantidad = cursor.fetchone()

        if cantidad:
            return cantidad[0]  # Devolvemos la cantidad disponible
        else:
            return None

    @staticmethod
    def obtener_por_isbn(isbn):
        conn = ConexionDB().obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM libros WHERE isbn = ? AND dado_de_baja = 0", (isbn,))
        libro = cursor.fetchone()
        return libro

    @staticmethod
    def actualizar_cantidad_disponible(isbn, cantidad):
        conn = ConexionDB().obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("UPDATE libros SET cantidad_disponible = cantidad_disponible + ? WHERE isbn = ? AND dado_de_baja = 0",
                       (cantidad, isbn))
        conn.commit()

    @staticmethod
    def actualizar_cantidad_buen_estado(isbn, cantidad):
        conn = ConexionDB().obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("UPDATE libros SET cantidad_buen_estado = cantidad_buen_estado + ? WHERE isbn = ? AND dado_de_baja = 0",
                       (cantidad, isbn))
        conn.commit()

    @staticmethod
    def eliminar_libro(isbn):
        conn = ConexionDB().obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM libros WHERE isbn = ?", (isbn,))
        conn.commit()

    @staticmethod
    def dar_de_baja(isbn):
        # Conectar a la base de datos y actualizar el estado "dado de baja"
        conn = ConexionDB().obtener_conexion()
        cursor = conn.cursor()
        cursor.execute('''
                UPDATE libros
                SET dado_de_baja = 1
                WHERE isbn = ?
            ''', (isbn,))
        conn.commit()

    @staticmethod
    def obtener_libros_disponibles_por_autor(id_autor):
        conn = ConexionDB().obtener_conexion()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT isbn, titulo, cantidad_disponible 
            FROM libros 
            WHERE cantidad_disponible > 0 AND id_autor = ?
        ''', (id_autor,))
        libros = cursor.fetchall()
        return libros
