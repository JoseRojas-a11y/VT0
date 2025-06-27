import tkinter as tk
from configuracion import page
from PIL import Image, ImageTk
from configuracion import get_db_connection
from configuracion import get_config_boton_volver
from Apps.NotasAlumnoPage import page_nota
from Apps.EventosAlumnoPage import page_eventos
from Apps.MaterialesAlumnoPage import page_material

class page_student(page):
    def __init__(self, nombre_usuario="Alumno", codigo_alumno=None):
        super().__init__()
        self.root.title("Panel Alumno")
        self.root.configure(bg=self.background[0])
        self.root.geometry(self.background[1])
        self.render_header(nombre_usuario)

        # Botón Cerrar sesión
        boton_volver_cfg = get_config_boton_volver()
        tk.Button(
            self.root, text="Cerrar sesión", command=self.cerrar_sesion,
            bg=boton_volver_cfg["bg"], fg=boton_volver_cfg["fg"],
            font=boton_volver_cfg["font"], relief=boton_volver_cfg["relief"]
        ).pack(anchor=boton_volver_cfg["anchor"], padx=boton_volver_cfg["padx"], pady=boton_volver_cfg["pady"])

        # Título personalizado
        self.label_saludo = tk.Label(
            self.root,
            text=f"¡Hola, {nombre_usuario}!",
            font=(self.tittle[3], self.tittle[1], "bold"),
            bg=self.background[0],
            fg=self.tittle[2]
        )
        self.label_saludo.pack(pady=(30, 10))

        # Imagen del logo
        img = Image.open(self.logo[2])
        img = img.resize((120, 120), Image.Resampling.LANCZOS)
        self.logo_img = ImageTk.PhotoImage(img)
        self.logo_label = tk.Label(self.root, image=self.logo_img, bg=self.logo[1])
        self.logo_label.pack(pady=10)

        # Mostrar información académica básica
        if codigo_alumno:
            try:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT nombre_completo FROM alumnos WHERE codigo=%s", (codigo_alumno,))
                row: tuple = cursor.fetchone() # type: ignore
                if row:
                    info = f"Nombre completo: {row[0]}\nCódigo: {codigo_alumno}"
                else:
                    info = f"Código: {codigo_alumno}"
                cursor.close()
                conn.close()
            except Exception as e:
                info = f"Error al obtener datos: {e}"
        else:
            info = "Bienvenido al sistema."
        self.label_info = tk.Label(self.root, text=info, font=(self.tittle[3], 12), bg=self.background[0], fg="#FFF8E1")
        self.label_info.pack(pady=10)

        # Botones para ver notas, eventos y materiales
        btn_style = {
            "width": 20, "height": 2, "bg": "#FFF8E1", "fg": "#9E2A2F", "bd": 2,
            "relief": "raised", "font": (self.tittle[3], 12, "bold"),
            "activebackground": "#F5E9C6", "activeforeground": "#9E2A2F", "cursor": "hand2",
            "highlightbackground": "#9E2A2F", "highlightcolor": "#9E2A2F"
        }
        tk.Button(self.root, text="Ver Notas", command=lambda: self.abrir_notas(nombre_usuario, codigo_alumno), **btn_style).pack(pady=7)
        tk.Button(self.root, text="Ver Eventos", command=lambda: self.abrir_eventos(nombre_usuario, codigo_alumno), **btn_style).pack(pady=7)
        tk.Button(self.root, text="Ver Materiales", command=lambda: self.abrir_materiales(nombre_usuario, codigo_alumno), **btn_style).pack(pady=7)

    def abrir_notas(self, nombre_usuario, codigo_alumno):
        self.root.destroy()
        page_nota(nombre_usuario=nombre_usuario, codigo_alumno=codigo_alumno)

    def abrir_eventos(self, nombre_usuario, codigo_alumno):
        self.root.destroy()
        page_eventos(nombre_usuario=nombre_usuario, codigo_alumno=codigo_alumno)

    def abrir_materiales(self, nombre_usuario, codigo_alumno):
        self.root.destroy()
        page_material(nombre_usuario=nombre_usuario, codigo_alumno=codigo_alumno)

    def cerrar_sesion(self):
        self.root.destroy()
        from Apps.LoginPage import LoginPage
        LoginPage()

if __name__ == "__main__":
    app = page_student(nombre_usuario="Alumno", codigo_alumno="A001")
    app.root.mainloop()
