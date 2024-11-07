-- Borrar filas tablas
DELETE FROM autores;
DELETE FROM libros;
DELETE FROM prestamos;
DELETE FROM usuarios;

-- Reiniciar seq
UPDATE sqlite_sequence SET seq = 0;
