import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # <- Se importa PIL para redimensionar imagenes
import mysql.connector
from config import page

# Conexión a la base de datos
def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="db_vt0"
    )

class page_admin(page):

    def __init__(self):
        super().__init__()

        # Configurar la ventana principal
        self.root.configure(bg=self.background[0])
        self.root.geometry(self.background[1])

        # encabezado
        self.render_header()

        # Título "Hola, nombre!"
        self.label_saludo = tk.Label(self.root, text="¡Hola, nombre!", 
                                     font=(self.tittle[3], self.tittle[1]), 
                                     bg=self.background[0], fg=self.tittle[2])
        self.label_saludo.pack(pady=(30, 10))

        # Imagen del logo redimensionada
        img = Image.open(self.logo[2])
        img = img.resize((120, 120), Image.LANCZOS)  # type: ignore
        self.logo_img = ImageTk.PhotoImage(img)
        self.logo_label = tk.Label(self.root, image=self.logo_img, bg=self.logo[1])
        self.logo_label.pack(pady=10)


        # Texto "Seleccione campo"
        self.label_seleccion = tk.Label(self.root, text="Seleccione campo con el\n que quiere interactuar", 
                                        font=(self.tittle[3], 10), 
                                        bg=self.background[0])
        self.label_seleccion.pack(pady=(20, 5))

        # Separador
        self.separador = tk.Frame(self.root, height=1, width=200, bg='gray')
        self.separador.pack(pady=(0, 10))

        # Botones
        estilo_boton = {
            "width": 20,
            "height": 1,
            "bg": self.background[0],
            "bd": 1,
            "relief": "solid",
            "font": (self.tittle[3], 12)
        }

        self.btn_alumno = tk.Button(self.root, text="Alumno", **estilo_boton)
        self.btn_alumno.pack(pady=5)

        self.btn_curso = tk.Button(self.root, text="Curso", **estilo_boton)
        self.btn_curso.pack(pady=5)

        self.btn_material = tk.Button(self.root, text="Material", **estilo_boton)
        self.btn_material.pack(pady=5)


# Solo para pruebas locales
if __name__ == "__main__":
    app = page_admin()
    app.root.mainloop()