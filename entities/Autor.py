import sqlite3


class Autor:
    def __init__(self, nombre, apellido, nacionalidad):
        self.nombre = nombre
        self.apellido = apellido
        self.nacionalidad = nacionalidad

    def guardar(self):
        conn = sqlite3.connect('biblioteca.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO autores (nombre, apellido, nacionalidad) VALUES (?, ?, ?)",
                       (self.nombre, self.apellido, self.nacionalidad))
        conn.commit()
        conn.close()

    @staticmethod
    def obtener_autores():
        conn = sqlite3.connect('biblioteca.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id_autor, nombre FROM autores")
        autores = cursor.fetchall()
        conn.close()
        return autores
