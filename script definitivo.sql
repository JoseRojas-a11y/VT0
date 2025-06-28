CREATE DATABASE db_vt0;
USE db_vt0;

-- Tabla: alumnos (solo información académica, sin password)
CREATE TABLE alumnos (
    codigo VARCHAR(20) PRIMARY KEY,
    nombre_completo VARCHAR(100) NOT NULL
);

-- Tabla: cursos
CREATE TABLE cursos (
    codigo VARCHAR(15) PRIMARY KEY, -- Ejemplo: MAT101-A
    nombre VARCHAR(100) NOT NULL
);

-- Tabla intermedia: alumnos_cursos (relación muchos a muchos)
CREATE TABLE alumnos_cursos (
    codigo_alumno VARCHAR(20),
    codigo_curso VARCHAR(15),
    PRIMARY KEY (codigo_alumno, codigo_curso),
    FOREIGN KEY (codigo_alumno) REFERENCES alumnos(codigo),
    FOREIGN KEY (codigo_curso) REFERENCES cursos(codigo)
);

-- Tabla: eventos
CREATE TABLE eventos (
    id_evento INT AUTO_INCREMENT PRIMARY KEY,
    tipo VARCHAR(100) NOT NULL,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    descripcion TEXT
);


-- Tabla: notas
CREATE TABLE notas (
    codigo_alumno VARCHAR(20),
    codigo_curso VARCHAR(15),
    parcial FLOAT,
    pc1 FLOAT,
    pc2 FLOAT,
    pc3 FLOAT,
    pc4 FLOAT,
    final FLOAT,
    prediccion FLOAT,
    PRIMARY KEY (codigo_alumno, codigo_curso),
    FOREIGN KEY (codigo_alumno) REFERENCES alumnos(codigo),
    FOREIGN KEY (codigo_curso) REFERENCES cursos(codigo)
);

-- Tabla: materiales
CREATE TABLE materiales (
    id_material INT AUTO_INCREMENT PRIMARY KEY,
    codigo_curso VARCHAR(15),
    tipo ENUM('planchas', 'video', 'pdf') NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    enlace TEXT,
    FOREIGN KEY (codigo_curso) REFERENCES cursos(codigo)
);

-- Tabla: usuarios del sistema (alumnos y administradores)
CREATE TABLE usuarios (
    username VARCHAR(50) PRIMARY KEY,
    password VARCHAR(50) NOT NULL,
    rol ENUM('administrador', 'alumno') NOT NULL,
    codigo_alumno VARCHAR(20),
    FOREIGN KEY (codigo_alumno) REFERENCES alumnos(codigo),
    CHECK (
        (rol = 'alumno' AND codigo_alumno IS NOT NULL) OR
        (rol = 'administrador' AND codigo_alumno IS NULL)
    )
);

-- === ALUMNOS ===
INSERT INTO alumnos (codigo, nombre_completo) VALUES
('A001', 'Luis Torres'),
('A002', 'María Salas'),
('A003', 'Carlos García'),
('A004', 'Sofía Mendoza'),
('A005', 'Diego Fernández'),
('A006', 'Lucía Ramírez');

-- === USUARIOS (contraseñas en texto plano solo para pruebas)
INSERT INTO usuarios (username, password, rol, codigo_alumno) VALUES
('luis.t', 'alumno123', 'alumno', 'A001'),
('maria.s', 'alumno456', 'alumno', 'A002'),
('admin1',  'admin123',  'administrador', NULL),
('sofia.m', 'clave001', 'alumno', 'A004'),
('diego.f', 'clave002', 'alumno', 'A005'),
('lucia.r', 'clave003', 'alumno', 'A006'),
('admin2',  'admin123', 'administrador', NULL);

-- === CURSOS ===
INSERT INTO cursos (codigo, nombre) VALUES
('MAT101-A', 'Matemática Básica'),
('FIS102-B', 'Física General'),
('QUI103-C', 'Química I'),
('MAT102-B', 'Álgebra Lineal'),
('BIO201-C', 'Biología General'),
('INF150-A', 'Introducción a la Programación');

-- === ALUMNOS_CURSOS ===
INSERT INTO alumnos_cursos (codigo_alumno, codigo_curso) VALUES
('A001', 'MAT101-A'),
('A001', 'FIS102-B'),
('A002', 'MAT101-A'),
('A003', 'QUI103-C'),
('A004', 'MAT102-B'),
('A004', 'BIO201-C'),
('A005', 'INF150-A'),
('A006', 'MAT102-B'),
('A006', 'INF150-A');

-- === NOTAS ===
INSERT INTO notas (codigo_alumno, codigo_curso, parcial, pc1, pc2, pc3, pc4, final, prediccion) VALUES
('A001', 'MAT101-A', 14, 15, 16, 15, 13, 16, 15),
('A001', 'FIS102-B', 12, 13, 16, 15, 11, 14, 13),
('A002', 'MAT101-A', 17, 18, 16, 15, 16, 19, 18),
('A004', 'MAT102-B', 15, 14, 16, 15, 14, 17, 16),
('A004', 'BIO201-C', 13, 15, 12, 13, 14, 14, 14),
('A005', 'INF150-A', 17, 18, 16, 19, 20, 19, 18),
('A006', 'MAT102-B', 14, 13, 14, 14, 15, 15, 14),
('A006', 'INF150-A', 19, 18, 19, 20, 20, 20, 19);

-- === EVENTOS ===
INSERT INTO eventos (tipo, fecha, hora, descripcion) VALUES
('Taller', '2025-07-10', '09:00:00', 'Taller de laboratorio de física'),
('Conferencia', '2025-07-15', '14:00:00', 'Charla de orientación vocacional'),
('Examen Final', '2025-08-10', '10:00:00', 'Evaluación final de Álgebra Lineal'),
('Taller Virtual', '2025-08-15', '17:00:00', 'Sesión de repaso de programación'),
('Charla Científica', '2025-08-20', '11:30:00', 'Investigación en biotecnología');

-- === MATERIALES ===
INSERT INTO materiales (codigo_curso, tipo, nombre, enlace) VALUES
('MAT101-A', 'pdf', 'Guía de ejercicios', 'https://ejemplo.com/mat101/guia.pdf'),
('FIS102-B', 'video', 'Video clase 1', 'https://ejemplo.com/fis102/clase1.mp4'),
('QUI103-C', 'planchas', 'Planchas de laboratorio', 'https://ejemplo.com/qui103/planchas.zip'),
('MAT102-B', 'pdf', 'Resumen de Teoría de Matrices', 'https://ejemplo.com/mat102/matrices.pdf'),
('BIO201-C', 'video', 'Clase grabada sobre células', 'https://ejemplo.com/bio201/celulas.mp4'),
('INF150-A', 'planchas', 'Ejercicios resueltos de Python', 'https://ejemplo.com/inf150/python.zip');

