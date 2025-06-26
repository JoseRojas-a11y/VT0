from typing import Tuple
import tkinter as tk

def get_config_fondo() -> Tuple[str, str]:
    
    #Color de fondo y las dimensiones de la ventana.
    
    return "#9E2A2F", "375x667"

def get_config_titulo() -> Tuple[str, int, str, str]:
    
    #Texto del titulo, tamaño de fuente, color de fondo, color del texto y la tipografia
    
    return "Bienvenido a VT0", 24, "white", "Helvetica"

def get_config_logo() -> Tuple[str, str, str]:
    
    #Texto del logo, tamaño de fuente, color de fondo, color del texto y la tipografia
    
    return "Universidad Nacional\nde\nIngenieria", "#9E2A2F", "logo_uni.png"

def get_config_entrada() -> Tuple[str, int, str, str]:
    
    #Texto de las etiquetas, tamaño de fuente, color y la tipografia
    
    return "Código UNI:", 14, "white", "Helvetica"

def get_config_boton() -> Tuple[str, str, str, int, int, int, str]:
    
    #Texto del boton, color de fondo, color del texto, tamaño, tamaño de la fuente y la tipografia.
    
    return "Iniciar sesión", "#F5F5DC", "white", 16, 20, 2, "Helvetica"

class page():
    def __init__(self):
        self.root =tk.Tk()
        self.background = get_config_fondo()
        self.tittle = get_config_titulo()
        self.logo = get_config_logo()

    def render_header(self):
        header_frame = tk.Frame(self.root, bg=self.background[0])
        header_frame.pack(fill='x', pady=(10, 0), padx=10)

        btn_font = (self.tittle[3], 10)

        btn_reportes = tk.Button(header_frame, text="Reportes", bg="white", font=btn_font, bd=1, relief="solid")
        btn_reportes.pack(side="right", padx=5)

        btn_ayuda = tk.Button(header_frame, text="Ayuda", bg="white", font=btn_font, bd=1, relief="solid")
        btn_ayuda.pack(side="right", padx=5)

        btn_acerca = tk.Button(header_frame, text="Acerca de", bg="white", font=btn_font, bd=1, relief="solid")
        btn_acerca.pack(side="right", padx=5)

        perfil = tk.Label(header_frame, text='🔔 [Foto Perfil]', bg=self.background[0], anchor='ne')
        perfil.pack(side="right", padx=5)
