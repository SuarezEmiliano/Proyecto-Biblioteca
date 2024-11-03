import sqlite3

# Conexión a la base de datos (creará el archivo biblioteca.db si no existe)
def conectar_db():
    conn = sqlite3.connect('../biblioteca.db')
    return conn

# Creación de las tablas
def crear_tablas():
    conn = conectar_db()
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
            fecha_devolucion_estimada TEXT,
            fecha_devolucion_real TEXT,
            FOREIGN KEY(id_usuario) REFERENCES usuarios(id_usuario),
            FOREIGN KEY(isbn) REFERENCES libros(isbn)
        )
    ''')

    # Guardar cambios y cerrar conexión
    conn.commit()
    conn.close()
    print("Tablas creadas correctamente.")

if __name__ == "__main__":
    crear_tablas()