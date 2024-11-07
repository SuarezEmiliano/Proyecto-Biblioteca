import sqlite3

class Usuario:
    def __init__(self, nombre, apellido, tipo_usuario, direccion, telefono):
        # Eliminamos self.id ya que se generará automáticamente en la base de datos
        self.nombre = nombre
        self.apellido = apellido
        self.tipo_usuario = tipo_usuario
        self.direccion = direccion
        self.telefono = telefono

    def guardar(self):
        conn = sqlite3.connect('biblioteca.db')
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO usuarios (nombre, apellido, tipo_usuario, direccion, telefono) 
            VALUES (?, ?, ?, ?, ?)
        """, (self.nombre, self.apellido, self.tipo_usuario, self.direccion, self.telefono))
        conn.commit()
        conn.close()

    def obtener_usuarios():
        conn = sqlite3.connect('biblioteca.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id_usuario, nombre FROM usuarios")
        usuarios = cursor.fetchall()
        conn.close()
        return usuarios

    def obtener_nombre_apellido(id_usuario):
        conn = sqlite3.connect('biblioteca.db')
        cursor = conn.cursor()
        cursor.execute("SELECT nombre, apellido FROM usuarios WHERE id_usuario = ?", (id_usuario,))
        usuario = cursor.fetchone()  # Solo obtenemos un registro
        conn.close()

        if usuario:
            return usuario
        else:
            return None
