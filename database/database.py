import sqlite3


class ConexionDB:
    _instancia = None

    def __new__(cls):
        # Si no hay una instancia creada, la creamos
        if cls._instancia is None:
            cls._instancia = super(ConexionDB, cls).__new__(cls)
            # Inicializamos la conexión a la base de datos
            cls._instancia.conn = sqlite3.connect('./biblioteca.db')
        return cls._instancia

    def obtener_conexion(self):
        return self._instancia.conn

    def cerrar_conexion(self):
        if self._instancia.conn:
            self._instancia.conn.close()
            self._instancia.conn = None
            self._instancia = None


# Creación de las tablas
def crear_tablas():
    # Usamos la instancia única de ConexionDB
    conexion_db = ConexionDB()
    conn = conexion_db.obtener_conexion()
    cursor = conn.cursor()

    # Tabla de autores
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS autores (
            id_autor INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            nacionalidad TEXT
        )
    ''')

    # Tabla de libros
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS libros (
            isbn TEXT PRIMARY KEY,
            titulo TEXT NOT NULL,
            genero TEXT,
            anio_publicacion INTEGER,
            id_autor INTEGER,
            cantidad_disponible INTEGER,
            cantidad_buen_estado INTEGER,
            dado_de_baja INTEGER,
            FOREIGN KEY(id_autor) REFERENCES autores(id_autor)
        )
    ''')

    # Tabla de usuarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            tipo_usuario TEXT NOT NULL, -- "estudiante" o "profesor"
            direccion TEXT,
            telefono TEXT
        )
    ''')

    # Tabla de préstamos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prestamos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_usuario INTEGER,
            isbn TEXT,
            fecha_prestamo TEXT,
            fecha_devolucion_estimada DATE,
            fecha_devolucion_real DATE,
            FOREIGN KEY(id_usuario) REFERENCES usuarios(id_usuario),
            FOREIGN KEY(isbn) REFERENCES libros(isbn)
        )
    ''')

    # Guardar cambios y cerrar conexión
    conn.commit()
    print("Tablas creadas correctamente.")


if __name__ == "__main__":
    crear_tablas()
