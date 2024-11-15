import sqlite3

from database.database import ConexionDB


class Usuario:
    def __init__(self, nombre, apellido, tipo_usuario, direccion, telefono):
        # Eliminamos self.id ya que se generará automáticamente en la base de datos
        self.nombre = nombre
        self.apellido = apellido
        self.tipo_usuario = tipo_usuario
        self.direccion = direccion
        self.telefono = telefono

    def guardar(self):
        conn = ConexionDB().obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO usuarios (nombre, apellido, tipo_usuario, direccion, telefono) 
            VALUES (?, ?, ?, ?, ?)
        """, (self.nombre, self.apellido, self.tipo_usuario, self.direccion, self.telefono))
        conn.commit()

    @staticmethod
    def obtener_usuarios():
        conn = ConexionDB().obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT id_usuario, nombre FROM usuarios")
        usuarios = cursor.fetchall()
        return usuarios

    @staticmethod
    def obtener_usuarios_consulta():
        conn = ConexionDB().obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios")
        usuarios = cursor.fetchall()
        return usuarios


    @staticmethod
    def obtener_nombre_apellido(id_usuario):
        conn = ConexionDB().obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT nombre, apellido FROM usuarios WHERE id_usuario = ?", (id_usuario,))
        usuario = cursor.fetchone()  # Solo obtenemos un registro

        if usuario:
            return usuario
        else:
            return None

    @staticmethod
    def obtener_tipo_usuario(id_usuario):
        conn = ConexionDB().obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT tipo_usuario FROM usuarios WHERE id_usuario = ?", (id_usuario,))
        tipo_usuario = cursor.fetchone()
        return tipo_usuario[0] if tipo_usuario else None

    @staticmethod
    def obtener_id_usuario_por_nombre_apellido(nombre, apellido):
        conn = ConexionDB().obtener_conexion()
        cursor = conn.cursor()

        # Ejecutamos la consulta para obtener el id_usuario con la combinación de nombre y apellido
        cursor.execute("SELECT id_usuario FROM usuarios WHERE nombre = ? AND apellido = ?", (nombre, apellido))

        # Recuperamos un solo resultado
        usuario = cursor.fetchone()

        # Si encontramos un resultado, devolvemos el id_usuario
        if usuario:
            return usuario[0]
        else:
            return None

    @staticmethod
    def eliminar_usuario(id_usuario):
        conn = ConexionDB().obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id_usuario = ?", (id_usuario,))
        conn.commit()
