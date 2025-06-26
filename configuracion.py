from typing import Tuple
import tkinter as tk
import mysql.connector

def get_config_fondo() -> Tuple[str, str]:
    # Color de fondo y dimensiones de la ventana.
    return "#9E2A2F", "375x667"

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

def get_db_connection():
    """Devuelve una conexión a la base de datos MySQL para ser usada en otras páginas."""
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="JoSeSiTo%_10",  # Ajusta tu contraseña si es necesario
        database="db_vt0"
    )

class page():
    def __init__(self):
        self.root = tk.Tk()
        self.background = get_config_fondo()
        self.tittle = get_config_titulo()
        self.logo = get_config_logo()

    def render_header(self, nombre_usuario="nombre de usuario"):
        header_frame = tk.Frame(self.root, bg=self.background[0], bd=2, relief="ridge")
        header_frame.pack(fill='x', pady=(10, 0), padx=10)

        # Nombre de usuario alineado a la izquierda y centrado verticalmente
        perfil = tk.Label(header_frame, text=f'🔔 {nombre_usuario}', bg=self.background[0], fg="#FFF8E1", anchor='w', font=(self.tittle[3], 10, "bold"))
        perfil.pack(side="left", padx=5, pady=2, fill='y')

        btn_font = (self.tittle[3], 10, "bold")
        btn_style = {"bg": "#FFF8E1", "fg": "#9E2A2F", "font": btn_font, "bd": 1, "relief": "solid", "activebackground": "#F5E9C6", "activeforeground": "#9E2A2F"}

        btn_reportes = tk.Button(header_frame, text="Reportes", **btn_style)
        btn_reportes.pack(side="right", padx=5)

        btn_ayuda = tk.Button(header_frame, text="Ayuda", **btn_style)
        btn_ayuda.pack(side="right", padx=5)

        btn_acerca = tk.Button(header_frame, text="Acerca de", **btn_style)
        btn_acerca.pack(side="right", padx=5)
