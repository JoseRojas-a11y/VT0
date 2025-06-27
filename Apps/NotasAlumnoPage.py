import tkinter as tk
from configuracion import page, get_db_connection, get_config_boton_volver
from PIL import Image, ImageTk
from Apps.StudentPage import page_student

class page_nota(page):
    def __init__(self, nombre_usuario="Alumno", codigo_alumno=None):
        super().__init__()
        self.root.title("Notas del Alumno")
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
        tk.Label(self.root, text="Notas", font=(self.tittle[3], self.tittle[1], "bold"), bg=self.background[0], fg=self.tittle[2]).pack(pady=(30, 10))

        # Logo
        img = Image.open(self.logo[2])
        img = img.resize((100, 100), Image.Resampling.LANCZOS)
        self.logo_img = ImageTk.PhotoImage(img)
        tk.Label(self.root, image=self.logo_img, bg=self.logo[1]).pack(pady=10)

        # Tabla de notas
        frame_tabla = tk.Frame(self.root, bg=self.background[0])
        frame_tabla.pack(pady=10)
        headers = ["Curso", "Parcial", "PC1", "PC2", "PC3", "PC4", "Final", "Predicción"]
        for j, h in enumerate(headers):
            tk.Label(frame_tabla, text=h, font=(self.tittle[3], 10, "bold"), bg=self.background[0], fg="#FFF8E1", padx=8, pady=4, borderwidth=1, relief="solid").grid(row=0, column=j, sticky="nsew")
        if codigo_alumno:
            try:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT c.nombre, n.parcial, n.pc1, n.pc2, n.pc3, n.pc4, n.final, n.prediccion
                    FROM notas n
                    JOIN cursos c ON n.codigo_curso = c.codigo
                    WHERE n.codigo_alumno = %s
                """, (codigo_alumno,))
                notas = cursor.fetchall()
                cursor.close()
                conn.close()
                for i, fila in enumerate(notas, start=1):
                    for j, dato in enumerate(fila):
                        tk.Label(frame_tabla, text=str(dato), font=(self.tittle[3], 10), bg=self.background[0], fg="#FFF8E1", padx=8, pady=4, borderwidth=1, relief="solid").grid(row=i, column=j, sticky="nsew")
                if not notas:
                    tk.Label(frame_tabla, text="No hay notas registradas.", font=(self.tittle[3], 12), bg=self.background[0], fg="#FFF8E1").grid(row=1, column=0, columnspan=len(headers))
            except Exception as e:
                tk.Label(frame_tabla, text=f"Error al obtener notas: {e}", font=(self.tittle[3], 12), bg=self.background[0], fg="#FFF8E1").grid(row=1, column=0, columnspan=len(headers))
        else:
            tk.Label(frame_tabla, text="No se proporcionó código de alumno.", font=(self.tittle[3], 12), bg=self.background[0], fg="#FFF8E1").grid(row=1, column=0, columnspan=len(headers))

        self.root.mainloop()

    def volver_panel(self, nombre_usuario, codigo_alumno):
        self.root.destroy()
        page_student(nombre_usuario=nombre_usuario, codigo_alumno=codigo_alumno) 