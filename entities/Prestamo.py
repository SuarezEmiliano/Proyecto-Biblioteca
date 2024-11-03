import sqlite3

class Prestamo:
    def __init__(self, id_usuario, isbn, fecha_prestamo, fecha_devolucion):
        self.id_usuario = id_usuario
        self.isbn = isbn
        self.fecha_prestamo = fecha_prestamo
        self.fecha_devolucion = fecha_devolucion

    def guardar(self):
        conn = sqlite3.connect('biblioteca.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO prestamos (id_usuario, isbn, fecha_prestamo, fecha_devolucion_estimada) 
            VALUES (?, ?, ?, ?)
        ''', (self.id_usuario, self.isbn, self.fecha_prestamo, self.fecha_devolucion))
        conn.commit()
        conn.close()
