import sqlite3

from database.database import ConexionDB


class Autor:
    def __init__(self, nombre, apellido, nacionalidad):
        self.nombre = nombre
        self.apellido = apellido
        self.nacionalidad = nacionalidad

    def guardar(self):
        conn = ConexionDB().obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO autores (nombre, apellido, nacionalidad) VALUES (?, ?, ?)",
                       (self.nombre, self.apellido, self.nacionalidad))
        conn.commit()

    @staticmethod
    def obtener_autores():
        conn = ConexionDB().obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT id_autor, nombre FROM autores")
        autores = cursor.fetchall()
        return autores

    @staticmethod
    def obtener_autores_consulta():
        conn = ConexionDB().obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM autores")
        autores = cursor.fetchall()
        return autores

    @staticmethod
    def eliminar_autor(id_autor):
        conn = ConexionDB().obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM autores WHERE id_autor = ?", (id_autor,))
        conn.commit()
