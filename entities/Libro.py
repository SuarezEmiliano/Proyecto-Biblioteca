import sqlite3

class Libro:
    def __init__(self, isbn, titulo, genero, anio_publicacion, id_autor, cantidad_disponible):
        self.isbn = isbn
        self.titulo = titulo
        self.genero = genero
        self.anio_publicacion = anio_publicacion
        self.id_autor = id_autor  # Asegúrate de usar id_autor
        self.cantidad_disponible = cantidad_disponible

    def guardar(self):
        conn = sqlite3.connect('biblioteca.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO libros (isbn, titulo, genero, anio_publicacion, id_autor, cantidad_disponible) 
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (self.isbn, self.titulo, self.genero, self.anio_publicacion, self.id_autor, self.cantidad_disponible))
        conn.commit()
        conn.close()


    @staticmethod
    def consultar_disponibilidad(codigo):
        conn = sqlite3.connect('biblioteca.db')
        cursor = conn.cursor()
        cursor.execute("SELECT cantidad_disponible FROM libros WHERE codigo = ?", (codigo,))
        cantidad = cursor.fetchone()
        conn.close()
        return cantidad[0] if cantidad else 0
