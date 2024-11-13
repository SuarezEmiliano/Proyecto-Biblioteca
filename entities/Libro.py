import sqlite3


class Libro:
    def __init__(self, isbn, titulo, genero, anio_publicacion, id_autor, cantidad_disponible, cantidad_buen_estado):
        self.isbn = isbn
        self.titulo = titulo
        self.genero = genero
        self.anio_publicacion = anio_publicacion
        self.id_autor = id_autor
        self.cantidad_disponible = cantidad_disponible
        self.cantidad_buen_estado = cantidad_buen_estado

    def guardar(self):
        conn = sqlite3.connect('biblioteca.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO libros (isbn, titulo, genero, anio_publicacion, 
                id_autor, cantidad_disponible, cantidad_buen_estado) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (self.isbn, self.titulo, self.genero, self.anio_publicacion,
              self.id_autor, self.cantidad_disponible, self.cantidad_buen_estado))
        conn.commit()
        conn.close()

    @staticmethod
    def obtener_libros_disponibles():
        conn = sqlite3.connect('biblioteca.db')
        cursor = conn.cursor()
        cursor.execute("SELECT isbn, titulo FROM libros WHERE cantidad_disponible > 0")
        libros = cursor.fetchall()
        conn.close()
        return libros

    @staticmethod
    def obtener_libros():
        conn = sqlite3.connect('biblioteca.db')
        cursor = conn.cursor()
        cursor.execute("SELECT *, titulo FROM libros")
        libros = cursor.fetchall()
        conn.close()
        return libros

    @staticmethod
    def obtener_cantidad_disponible(isbn):
        conn = sqlite3.connect('biblioteca.db')
        cursor = conn.cursor()
        cursor.execute("SELECT cantidad_disponible FROM libros WHERE isbn = ?", (isbn,))
        cantidad = cursor.fetchone()
        conn.close()

        if cantidad:
            return cantidad[0]  # Devolvemos la cantidad disponible
        else:
            return None

    @staticmethod
    def actualizar_cantidad_disponible(isbn, cantidad):
        conn = sqlite3.connect('biblioteca.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE libros SET cantidad_disponible = cantidad_disponible + ? WHERE isbn = ?",
                       (cantidad, isbn))
        conn.commit()
        conn.close()

    @staticmethod
    def actualizar_cantidad_buen_estado(isbn, cantidad):
        conn = sqlite3.connect('biblioteca.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE libros SET cantidad_buen_estado = cantidad_buen_estado + ? WHERE isbn = ?",
                       (cantidad, isbn))
        conn.commit()
        conn.close()
