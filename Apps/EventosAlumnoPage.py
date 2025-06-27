import tkinter as tk
from configuracion import page, get_db_connection, get_config_boton_volver
from PIL import Image, ImageTk
from Apps.StudentPage import page_student
from collections import defaultdict
import datetime

class page_eventos(page):
    def __init__(self, nombre_usuario="Alumno", codigo_alumno=None):
        super().__init__()
        self.root.title("Eventos del Alumno")
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
        tk.Label(self.root, text="Eventos", font=(self.tittle[3], self.tittle[1], "bold"), bg=self.background[0], fg=self.tittle[2]).pack(pady=(30, 10))

        # Logo
        img = Image.open(self.logo[2])
        img = img.resize((100, 100), Image.Resampling.LANCZOS)
        self.logo_img = ImageTk.PhotoImage(img)
        tk.Label(self.root, image=self.logo_img, bg=self.logo[1]).pack(pady=10)

        # Lista de eventos
        frame_eventos = tk.Frame(self.root, bg=self.background[0])
        frame_eventos.pack(pady=10, fill="both", expand=True)
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT fecha, tipo, hora, descripcion
                FROM eventos
                ORDER BY fecha, hora
            """)
            eventos = cursor.fetchall()
            cursor.close()
            conn.close()
            eventos_por_fecha = defaultdict(list)
            for fecha, tipo, hora, descripcion in eventos:
                eventos_por_fecha[fecha].append((tipo, hora, descripcion))
            row = 0
            for fecha in sorted(eventos_por_fecha):
                fecha_dt = datetime.datetime.strptime(str(fecha), "%Y-%m-%d")
                fecha_str = fecha_dt.strftime("%A %d de %B del %Y").capitalize()
                tk.Label(frame_eventos, text=fecha_str, font=(self.tittle[3], 12, "bold"), fg="orange", bg=self.background[0]).grid(row=row, column=0, columnspan=4, sticky="w", pady=(10,0))
                row += 1
                for tipo, hora, descripcion in eventos_por_fecha[fecha]:
                    tk.Label(frame_eventos, text=tipo, font=(self.tittle[3], 10, "bold"), bg=self.background[0], fg="#FFF8E1").grid(row=row, column=0, sticky="w")
                    tk.Label(frame_eventos, text=f"🕒 {hora}", fg="blue", bg=self.background[0], font=(self.tittle[3], 10)).grid(row=row, column=1, sticky="w")
                    tk.Label(frame_eventos, text=descripcion, fg="navy", bg=self.background[0], font=(self.tittle[3], 10)).grid(row=row, column=2, sticky="w")
                    row += 1
            if not eventos:
                tk.Label(frame_eventos, text="No hay eventos registrados.", font=(self.tittle[3], 12), bg=self.background[0], fg="#FFF8E1").grid(row=0, column=0)
        except Exception as e:
            tk.Label(frame_eventos, text=f"Error al obtener eventos: {e}", font=(self.tittle[3], 12), bg=self.background[0], fg="#FFF8E1").grid(row=0, column=0)

        self.root.mainloop()

    def volver_panel(self, nombre_usuario, codigo_alumno):
        self.root.destroy()
        page_student(nombre_usuario=nombre_usuario, codigo_alumno=codigo_alumno) 