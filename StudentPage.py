import tkinter as tk
from configuracion import page
from PIL import Image, ImageTk
from configuracion import get_db_connection
from configuracion import get_config_boton_volver

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

    def cerrar_sesion(self):
        self.root.destroy()
        from LoginPage import LoginPage
        LoginPage()

if __name__ == "__main__":
    app = page_student(nombre_usuario="Alumno", codigo_alumno="A001")
    app.root.mainloop()
