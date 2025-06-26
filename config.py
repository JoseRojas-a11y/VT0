from typing import Tuple

def get_config_fondo() -> Tuple[str, str]:
    
    #Color de fondo y las dimensiones de la ventana.
    
    return "#9E2A2F", "375x667"

def get_config_titulo() -> Tuple[str, int, str, str, str]:
    
    #Texto del titulo, tamaño de fuente, color de fondo, color del texto y la tipografia
    
    return "Bienvenido a VT0", 24, "white", "#9E2A2F", "Helvetica"

def get_config_logo() -> Tuple[str, int, str, str, str]:
    
    #Texto del logo, tamaño de fuente, color de fondo, color del texto y la tipografia
    
    return "Universidad Nacional\nde\nIngenieria", 18, "white", "#9E2A2F", "Helvetica"

def get_config_entrada() -> Tuple[str, int, str, str]:
    
    #Texto de las etiquetas, tamaño de fuente, color y la tipografia
    
    return "Código UNI:", 14, "white", "Helvetica"

def get_config_boton() -> Tuple[str, str, str, int, int, int, str]:
    
    #Texto del boton, color de fondo, color del texto, tamaño, tamaño de la fuente y la tipografia.
    
    return "Iniciar sesión", "#F5F5DC", "black", 16, 20, 2, "Helvetica"

class page():
    def __init__(self):
        self.background = get_config_fondo()
        self.tittle = get_config_titulo()
        self.logo = get_config_logo()