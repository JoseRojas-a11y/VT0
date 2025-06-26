import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from config import page, get_db_connection

class page_admin(page):
    def __init__(self, nombre_usuario="nombre de usuario"):
        super().__init__()
        if not hasattr(self, 'root'):
            self.root = tk.Tk()
        self.root.title("Panel Administrador")

        # Configuración de la ventana
        self.root.configure(bg=self.background[0])
        self.root.geometry(self.background[1])
        self.render_header(nombre_usuario)

        # Botón Volver
        self.btn_volver = tk.Button(self.root, text="Volver", bg="#B3C6E7", fg="#222", font=(self.tittle[3], 10, "bold"), relief="raised", command=self.volver_login)
        self.btn_volver.pack(anchor="nw", padx=15, pady=(5, 0))

        # Título "Hola, nombre!"
        self.label_saludo = tk.Label(
            self.root,
            text=f"¡Hola, {nombre_usuario}!",
            font=(self.tittle[3], self.tittle[1], "bold"),
            bg=self.background[0],
            fg=self.tittle[2]
        )
        self.label_saludo.pack(pady=(30, 10))

        # Imagen del logo redimensionada
        img = Image.open(self.logo[2])
        img = img.resize((120, 120), Image.Resampling.LANCZOS)
        self.logo_img = ImageTk.PhotoImage(img)
        self.logo_label = tk.Label(self.root, image=self.logo_img, bg=self.logo[1])
        self.logo_label.pack(pady=10)
        
        # Texto "Seleccione campo"
        self.label_seleccion = tk.Label(
            self.root,
            text="Seleccione campo con el\n que quiere interactuar",
            font=(self.tittle[3], 12),
            bg=self.background[0],
            fg="#FFF8E1"
        )
        self.label_seleccion.pack(pady=(20, 5))

        # Separador
        self.separador = tk.Frame(self.root, height=2, width=220, bg='#FFF8E1', bd=0, relief="ridge")
        self.separador.pack(pady=(0, 10))

        # Estilo de botones
        estilo_boton = {
            "width": 20,
            "height": 2,
            "bg": "#FFF8E1",
            "fg": "#9E2A2F",
            "bd": 2,
            "relief": "raised",
            "font": (self.tittle[3], 12, "bold"),
            "activebackground": "#F5E9C6",
            "activeforeground": "#9E2A2F",
            "cursor": "hand2",
            "highlightbackground": "#9E2A2F",
            "highlightcolor": "#9E2A2F"
        }

        self.btn_alumno = tk.Button(self.root, text="Alumno", command=lambda: self.abrir_busqueda('alumno', nombre_usuario), **estilo_boton)
        self.btn_alumno.pack(pady=7)

        self.btn_curso = tk.Button(self.root, text="Curso", command=lambda: self.abrir_busqueda('curso', nombre_usuario), **estilo_boton)
        self.btn_curso.pack(pady=7)

        self.btn_material = tk.Button(self.root, text="Material", command=lambda: self.abrir_busqueda('material', nombre_usuario), **estilo_boton)
        self.btn_material.pack(pady=7)

    def volver_login(self):
        self.root.destroy()
        from LoginPage import LoginPage
        LoginPage()

    def abrir_busqueda(self, tipo, nombre_usuario):
        self.root.destroy()
        from SearchPage import SearchPage
        SearchPage(nombre_usuario=nombre_usuario, tipo_inicial=tipo)

# Solo para pruebas locales
if __name__ == "__main__":
    app = page_admin(nombre_usuario="Administrador")
    app.root.mainloop()