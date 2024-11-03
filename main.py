from entities.Autor import Autor
from entities.Libro import Libro
from entities.Usuario import Usuario
from entities.Prestamo import Prestamo
from datetime import datetime

from views.menu import abrir_ventana

def main():
    abrir_ventana()

    try:
        # Ejemplo de registro de libro
        libro = Libro("9781234567897", "Cien Años de Soledad", "Novela", 1967, 1, 3)
        libro.guardar()
        print("Libro guardado exitosamente.")
    except Exception as e:
        print(f"Error al guardar libro: {e}")

    try:
        # Ejemplo de registro de usuario
        usuario = Usuario("Juan", "Pérez", "estudiante", "Calle Falsa 123", "123456789")
        usuario.guardar()
        print("Usuario guardado exitosamente.")
    except Exception as e:
        print(f"Error al guardar usuario: {e}")

    try:
        # Ejemplo de préstamo de libro
        prestamo = Prestamo("Juan", "9781234567897", datetime.now().strftime("%Y-%m-%d"), "2024-12-01")
        prestamo.guardar()
        print("Préstamo guardado exitosamente.")
    except Exception as e:
        print(f"Error al guardar préstamo: {e}")

if __name__ == "__main__":
    main()
