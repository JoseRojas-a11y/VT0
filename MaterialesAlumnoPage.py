import tkinter as tk
from configuracion import page, get_db_connection, get_config_boton_volver
from PIL import Image, ImageTk
from StudentPage import page_student

class page_material(page):
    def __init__(self, nombre_usuario="Alumno", codigo_alumno=None):
        super().__init__()
        self.root.title("Materiales del Alumno")
        self.root.configure(bg=self.background[0])
        self.root.geometry(self.background[1])
        self.render_header(nombre_usuario)

        # Botón Volver
        boton_volver_cfg = get_config_boton_volver()
        tk.Button(
            self.root, text="Volver", command=lambda: self.volver_panel(nombre_usuario, codigo_alumno),
            bg=boton_volver_cfg["bg"], fg=boton_volver_cfg["fg"],
            font=boton_volver_cfg["font"], relief=boton_volver_cfg["relief"]
        ).pack(anchor=boton_volver_cfg["anchor"], padx=boton_volver_cfg["padx"], pady=boton_volver_cfg["pady"])

        # Título
        tk.Label(self.root, text="Materiales", font=(self.tittle[3], self.tittle[1], "bold"), bg=self.background[0], fg=self.tittle[2]).pack(pady=(30, 10))

        # Logo
        img = Image.open(self.logo[2])
        img = img.resize((100, 100), Image.Resampling.LANCZOS)
        self.logo_img = ImageTk.PhotoImage(img)
        tk.Label(self.root, image=self.logo_img, bg=self.logo[1]).pack(pady=10)

        # Tabla de materiales
        frame_tabla = tk.Frame(self.root, bg=self.background[0])
        frame_tabla.pack(pady=10)
        headers = ["Tipo", "Nombre", "Enlace"]
        for j, h in enumerate(headers):
            tk.Label(frame_tabla, text=h, font=(self.tittle[3], 10, "bold"), bg=self.background[0], fg="#FFF8E1", padx=8, pady=4, borderwidth=1, relief="solid").grid(row=0, column=j, sticky="nsew")
        if codigo_alumno:
            try:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT m.tipo, m.nombre, m.enlace
                    FROM alumnos_cursos ac
                    JOIN materiales m ON ac.codigo_curso = m.codigo_curso
                    WHERE ac.codigo_alumno = %s
                """, (codigo_alumno,))
                materiales = cursor.fetchall()
                cursor.close()
                conn.close()
                for i, fila in enumerate(materiales, start=1):
                    for j, dato in enumerate(fila):
                        if j == 2:
                            # Enlace como link (si es posible)
                            enlace = str(dato)
                            link = tk.Label(frame_tabla, text=enlace, font=(self.tittle[3], 10, "underline"), fg="blue", bg=self.background[0], cursor="hand2", padx=8, pady=4, borderwidth=1, relief="solid")
                            link.grid(row=i, column=j, sticky="nsew")
                            link.bind("<Button-1>", lambda e, url=enlace: self.abrir_enlace(url))
                        else:
                            tk.Label(frame_tabla, text=str(dato), font=(self.tittle[3], 10), bg=self.background[0], fg="#FFF8E1", padx=8, pady=4, borderwidth=1, relief="solid").grid(row=i, column=j, sticky="nsew")
                if not materiales:
                    tk.Label(frame_tabla, text="No hay materiales registrados.", font=(self.tittle[3], 12), bg=self.background[0], fg="#FFF8E1").grid(row=1, column=0, columnspan=len(headers))
            except Exception as e:
                tk.Label(frame_tabla, text=f"Error al obtener materiales: {e}", font=(self.tittle[3], 12), bg=self.background[0], fg="#FFF8E1").grid(row=1, column=0, columnspan=len(headers))
        else:
            tk.Label(frame_tabla, text="No se proporcionó código de alumno.", font=(self.tittle[3], 12), bg=self.background[0], fg="#FFF8E1").grid(row=1, column=0, columnspan=len(headers))

        self.root.mainloop()

    def abrir_enlace(self, url):
        import webbrowser
        webbrowser.open(url)

    def volver_panel(self, nombre_usuario, codigo_alumno):
        self.root.destroy()
        page_student(nombre_usuario=nombre_usuario, codigo_alumno=codigo_alumno) 