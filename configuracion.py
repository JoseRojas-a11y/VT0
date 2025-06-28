from typing import Tuple
import tkinter as tk
import mysql.connector

def get_config_fondo() -> Tuple[str, str]:
    # Color de fondo y dimensiones de la ventana.
    return "#9E2A2F", "400x710"

def get_config_titulo() -> Tuple[str, int, str, str]:
    # Texto del título, tamaño de fuente, color del texto, tipografía
    return "Bienvenido a VT0", 24, "#FFF8E1", "Helvetica"  # Texto crema

def get_config_logo() -> Tuple[str, str, str]:
    # Texto del logo, color de fondo, ruta de la imagen
    return "Universidad Nacional\nde\nIngenieria", "#9E2A2F", "logo_uni.png"

def get_config_entrada() -> Tuple[str, int, str, str]:
    # Texto de las etiquetas, tamaño de fuente, color y tipografía
    return "Código UNI:", 14, "#FFF8E1", "Helvetica"  # Texto crema

def get_config_boton() -> Tuple[str, str, str, int, int, int, str]:
    # Texto del botón, color de fondo, color del texto, tamaño, tamaño de fuente, alto, tipografía
    return "Iniciar sesión", "#FFF8E1", "#9E2A2F", 16, 20, 2, "Helvetica"  # Botón crema, texto vino

def render_header(root, nombre_usuario="nombre de usuario"):
    bg, _ = get_config_fondo()
    tittle = get_config_titulo()
    header_frame = tk.Frame(root, bg=bg, bd=2, relief="ridge")
    header_frame.pack(fill='x', pady=(10, 0), padx=10)

    perfil = tk.Label(header_frame, text=f'🔔 {nombre_usuario}', bg=bg, fg="#FFF8E1", anchor='w', font=(tittle[3], 10, "bold"))
    perfil.pack(side="left", padx=5, pady=2, fill='y')

    btn_font = (tittle[3], 10, "bold")
    btn_style = {"bg": "#FFF8E1", "fg": "#9E2A2F", "font": btn_font, "bd": 1, "relief": "solid", "activebackground": "#F5E9C6", "activeforeground": "#9E2A2F"}

    btn_reportes = tk.Button(header_frame, text="Reportes", command=lambda: mostrar_reportes(root), **btn_style)
    btn_reportes.pack(side="right", padx=5)

    btn_ayuda = tk.Button(header_frame, text="Ayuda", command=lambda: mostrar_ayuda(root), **btn_style)
    btn_ayuda.pack(side="right", padx=5)

    btn_acerca = tk.Button(header_frame, text="Acerca de", command=lambda: mostrar_acerca_de(root), **btn_style)
    btn_acerca.pack(side="right", padx=5)

def mostrar_acerca_de(root):
    ventana = tk.Toplevel(root)
    ventana.title("Acerca de")
    ventana.geometry("360x320")
    ventana.configure(bg="#FFF9C4")
    ventana.resizable(False, False)

    titulo = tk.Label(ventana, text="Sistema de Gestión - VT0", font=("Helvetica", 14, "bold"), bg="#FFF9C4", fg="#9E2A2F")
    titulo.pack(pady=(15, 5))

    version = tk.Label(ventana, text="Versión: 1.0", font=("Helvetica", 11), bg="#FFF9C4")
    version.pack()

    autores_label = tk.Label(ventana, text="Desarrollado por:", font=("Helvetica", 12, "bold"), bg="#FFF9C4", fg="#333")
    autores_label.pack(pady=(15, 5))

    integrantes = [
        "• Albornoz Azurza Gonzalo Alessandro ",
        "• Campos Castillo Andhle Leopoldo",
        "• Caycho Machaca Diego Alexander",
        "• Rojas Sanchez Jose Martin",
    ]
    for nombre in integrantes:
        tk.Label(ventana, text=nombre, font=("Helvetica", 11), bg="#FFF9C4").pack(anchor="w", padx=30)

    descripcion = "Aplicación creada como proyecto académico en la\nUniversidad Nacional de Ingeniería - UNI."
    tk.Label(ventana, text=descripcion, font=("Helvetica", 10), bg="#FFF9C4", fg="#555", justify="center").pack(pady=(20, 10))

    tk.Button(ventana, text="Cerrar", command=ventana.destroy, bg="#9E2A2F", fg="#FFF8E1", font=("Helvetica", 10, "bold")).pack(pady=5)
def mostrar_ayuda(root):
    ventana = tk.Toplevel(root)
    ventana.title("Ayuda")
    ventana.geometry("400x400")
    ventana.configure(bg="#FFF9C4")
    ventana.resizable(False, False)

    tk.Label(ventana, text="Centro de Ayuda", font=("Helvetica", 14, "bold"), bg="#FFF9C4", fg="#9E2A2F").pack(pady=15)

    preguntas = [
        ("¿Cómo consultar mis notas?", "Para ver tus notas, haz clic en la pestaña 'Notas'. Allí podrás ver tus calificaciones por curso."),
        ("¿Dónde encuentro los materiales de mis cursos?", "En la sección 'Material' puedes filtrar por curso y buscar materiales. Luego puedes abrirlos o copiar el enlace."),
        ("¿Qué tipo de eventos se mostrarán?", "Se muestran eventos como exámenes, talleres, conferencias o charlas, ordenados por fecha."),
        ("¿Qué hago si no veo un curso en mi lista?", "Revisa con el administrador si estás matriculado correctamente en ese curso."),
        ("¿Cómo cambiar mi contraseña?", "Por ahora, solo el administrador puede cambiar contraseñas desde su panel.")
    ]

    for texto_btn, respuesta in preguntas:
        tk.Button(
            ventana,
            text=texto_btn,
            bg="#FFF8E1",
            fg="#222",
            font=("Helvetica", 10, "bold"),
            wraplength=300,
            relief="raised",
            command=lambda r=respuesta, p=texto_btn: mostrar_respuesta(root, p, r)
        ).pack(fill="x", padx=20, pady=6)

    tk.Button(ventana, text="Cerrar", command=ventana.destroy, bg="#9E2A2F", fg="#FFF8E1", font=("Helvetica", 10, "bold")).pack(pady=10)

def mostrar_respuesta(root, pregunta, respuesta):
    subventana = tk.Toplevel(root)
    subventana.title(pregunta)
    subventana.geometry("400x200")
    subventana.configure(bg="#FFF9C4")
    subventana.resizable(False, False)

    tk.Label(subventana, text=pregunta, font=("Helvetica", 12, "bold"), bg="#FFF9C4", fg="#9E2A2F", wraplength=360).pack(pady=10)
    tk.Label(subventana, text=respuesta, font=("Helvetica", 10), bg="#FFF9C4", wraplength=360, justify="left").pack(padx=15)

    tk.Button(subventana, text="Cerrar", command=subventana.destroy, bg="#9E2A2F", fg="#FFF8E1", font=("Helvetica", 10, "bold")).pack(pady=10)

def get_config_boton_volver() -> dict:
    """Estilo estándar para botones de volver/cerrar sesión."""
    return {
        "bg": "#FFF8E1",
        "fg": "#222",
        "font": (get_config_titulo()[3], 10, "bold"),
        "relief": "raised",
        "padx": 15,
        "pady": (5, 0),
        "anchor": "nw"
    }

def mostrar_reportes(root):
    ventana = tk.Toplevel(root)
    ventana.title("Reportes del Sistema")
    ventana.geometry("400x420")
    ventana.configure(bg="#FFF9C4")
    ventana.resizable(False, False)

    tk.Label(ventana, text="Reportes Disponibles", font=("Helvetica", 14, "bold"), bg="#FFF9C4", fg="#9E2A2F").pack(pady=15)

    reportes = [
        ("Promedio por curso", "Aquí se mostrará el promedio general de cada curso."),
        ("Cantidad de alumnos por curso", "Se mostrará cuántos estudiantes están inscritos en cada curso."),
        ("Cantidad de materiales por curso", "Visualizarás cuántos materiales tiene cada curso registrado."),
        ("Próximos eventos por tipo", "Se listarán eventos académicos agrupados por tipo.")
    ]

    for texto_btn, descripcion in reportes:
        tk.Button(
            ventana,
            text=texto_btn,
            bg="#FFF8E1",
            fg="#222",
            font=("Helvetica", 10, "bold"),
            wraplength=300,
            relief="raised",
            command=lambda t=texto_btn, d=descripcion: mostrar_detalle_reporte(root, t, d)
        ).pack(fill="x", padx=20, pady=6)

    tk.Button(ventana, text="Cerrar", command=ventana.destroy, bg="#9E2A2F", fg="#FFF8E1", font=("Helvetica", 10, "bold")).pack(pady=10)

def mostrar_detalle_reporte(root, titulo, contenido):
    import tkinter as tk
    from tkinter import messagebox
    subventana = tk.Toplevel(root)
    subventana.title(titulo)
    subventana.geometry("500x340")
    subventana.configure(bg="#FFF9C4")
    subventana.resizable(False, False)

    tk.Label(subventana, text=titulo, font=("Helvetica", 12, "bold"), bg="#FFF9C4", fg="#9E2A2F").pack(pady=10)

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        if titulo == "Promedio por curso":
            cursor.execute("""
                SELECT c.codigo, c.nombre, ROUND(AVG(n.final), 2) AS promedio_final
                FROM notas n
                JOIN cursos c ON n.codigo_curso = c.codigo
                GROUP BY c.codigo, c.nombre
                ORDER BY c.codigo
            """)
            resultados = cursor.fetchall()
            headers = ["Código", "Curso", "Promedio Final"]

        elif titulo == "Cantidad de alumnos por curso":
            cursor.execute("""
                SELECT c.codigo, c.nombre, COUNT(ac.codigo_alumno) AS total_alumnos
                FROM cursos c
                LEFT JOIN alumnos_cursos ac ON c.codigo = ac.codigo_curso
                GROUP BY c.codigo, c.nombre
                ORDER BY c.codigo
            """)
            resultados = cursor.fetchall()
            headers = ["Código", "Curso", "N° de Alumnos"]

        elif titulo == "Cantidad de materiales por curso":
            cursor.execute("""
                SELECT c.codigo, c.nombre, COUNT(m.id_material) AS total_materiales
                FROM cursos c
                LEFT JOIN materiales m ON c.codigo = m.codigo_curso
                GROUP BY c.codigo, c.nombre
                ORDER BY c.codigo
            """)
            resultados = cursor.fetchall()
            headers = ["Código", "Curso", "N° de Materiales"]

        elif titulo == "Próximos eventos por tipo":
            cursor.execute("""
                SELECT tipo, COUNT(*) AS cantidad
                FROM eventos
                WHERE fecha >= CURDATE()
                GROUP BY tipo
                ORDER BY cantidad DESC
            """)
            resultados = cursor.fetchall()
            headers = ["Tipo de Evento", "Cantidad"]

        else:
            resultados = []
            headers = []

        if resultados:
            frame = tk.Frame(subventana, bg="#FFF9C4")
            frame.pack(padx=10, pady=10, fill="both", expand=True)

            for j, h in enumerate(headers):
                tk.Label(frame, text=h, font=("Helvetica", 10, "bold"), bg="#FFF8E1", fg="#9E2A2F", borderwidth=1, relief="solid", padx=5, pady=4).grid(row=0, column=j)

            for i, fila in enumerate(resultados, start=1):
                for j, dato in enumerate(fila):
                    tk.Label(frame, text=str(dato), font=("Helvetica", 10), bg="#FFFDE7", borderwidth=1, relief="solid", padx=5, pady=2).grid(row=i, column=j)
        else:
            tk.Label(subventana, text="No se encontraron resultados.", font=("Helvetica", 10), bg="#FFF9C4", fg="#9E2A2F").pack(pady=10)

        cursor.close()
        conn.close()

    except Exception as e:
        tk.Label(subventana, text=f"Error al obtener datos:\n{e}", font=("Helvetica", 10), bg="#FFF9C4", fg="red").pack(pady=10)

    tk.Button(subventana, text="Cerrar", command=subventana.destroy, bg="#9E2A2F", fg="#FFF8E1", font=("Helvetica", 10, "bold")).pack(pady=10)

def get_db_connection():
    """Devuelve una conexión a la base de datos MySQL para ser usada en otras páginas."""
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="JoSeSiTo%_10",  # Ajusta tu contraseña si es necesario
        database="db_vt0",
        auth_plugin='mysql_native_password'  # <-- Solución para el error de autenticación
    )

class page():
    def __init__(self):
        self.root = tk.Tk()
        self.background = get_config_fondo()
        self.tittle = get_config_titulo()
        self.logo = get_config_logo()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

