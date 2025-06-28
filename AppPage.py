import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import datetime
from configuracion import (
    get_db_connection, get_config_logo, get_config_entrada, get_config_boton,
    get_config_boton_volver, get_config_fondo, get_config_titulo, render_header, page
)

class AdminPage(page):
    def __init__(self, root, nombre_usuario, on_logout):
        self.root = root
        self.nombre_usuario = nombre_usuario
        self.on_logout = on_logout
        self.show_admin()

    def show_admin(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        bg, size = get_config_fondo()
        tittle = get_config_titulo()
        logo_cfg = get_config_logo()
        boton_volver_cfg = get_config_boton_volver()

        render_header(self.root, self.nombre_usuario)
        self.add_logout_button()

        label_titulo = tk.Label(
            self.root,
            text=f"¡Hola, {self.nombre_usuario}!",
            font=(tittle[3], tittle[1], "bold"),
            bg=bg, fg=tittle[2]
        )
        label_titulo.pack(pady=(30, 10))

        img = Image.open(logo_cfg[2]).resize((100, 125), Image.Resampling.LANCZOS)
        self.logo_img_admin = ImageTk.PhotoImage(img)
        logo_label = tk.Label(self.root, image=self.logo_img_admin, bg=logo_cfg[1])
        logo_label.pack(pady=10)

        label_campo = tk.Label(
            self.root,
            text="Seleccione campo con el\n que quiere interactuar",
            font=(tittle[3], 12),
            bg=bg, fg="#FFF8E1"
        )
        label_campo.pack(pady=(20, 5))

        tk.Frame(self.root, height=2, width=220, bg='#FFF8E1', bd=0, relief="ridge").pack(pady=(0, 10))

        estilo_boton = {
            "width": 20, "height": 2, "bg": "#FFF8E1", "fg": "#9E2A2F", "bd": 2,
            "relief": "raised", "font": (tittle[3], 12, "bold"),
            "activebackground": "#F5E9C6", "activeforeground": "#9E2A2F", "cursor": "hand2",
            "highlightbackground": "#9E2A2F", "highlightcolor": "#9E2A2F"
        }
        tk.Button(self.root, text="Alumno", command=lambda: self.show_search("alumno"), **estilo_boton).pack(pady=7)
        tk.Button(self.root, text="Curso", command=lambda: self.show_search("curso"), **estilo_boton).pack(pady=7)
        tk.Button(self.root, text="Material", command=lambda: self.show_search("material"), **estilo_boton).pack(pady=7)

    def show_search(self, tipo):
        for widget in self.root.winfo_children():
            widget.destroy()
        bg, size = get_config_fondo()
        tittle = get_config_titulo()
        render_header(self.root, self.nombre_usuario)
        self.add_logout_button()
        tk.Button(self.root, text="Volver", bg="#FFF8E1", fg="#222", font=(tittle[3], 10, "bold"), relief="raised", command=self.show_admin).pack(anchor="nw", padx=15, pady=(5, 0))
        tk.Label(self.root, text=f"Buscar {tipo.capitalize()}", font=(tittle[3], 16, "bold"), bg=bg, fg="#9E2A2F").pack(pady=(20, 10))
        entrada_cfg = get_config_entrada()
        frame_busqueda = tk.Frame(self.root, bg=bg)
        frame_busqueda.pack(pady=5)
        # Ajustar etiquetas y consulta para materiales
        label_codigo_text = "Código:"
        if tipo == "material":
            label_codigo_text = "Código de curso:"
        tk.Label(frame_busqueda, text=label_codigo_text, font=(entrada_cfg[3], entrada_cfg[1]), bg=bg, fg=entrada_cfg[2]).grid(row=0, column=0, padx=5, pady=5)
        entry_codigo = tk.Entry(frame_busqueda, font=(entrada_cfg[3], 12))
        entry_codigo.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(frame_busqueda, text="Nombre:", font=(entrada_cfg[3], entrada_cfg[1]), bg=bg, fg=entrada_cfg[2]).grid(row=1, column=0, padx=5, pady=5)
        entry_nombre = tk.Entry(frame_busqueda, font=(entrada_cfg[3], 12))
        entry_nombre.grid(row=1, column=1, padx=5, pady=5)
        boton_cfg = get_config_boton()
        btn_buscar = tk.Button(self.root, text="Buscar", bg="#FFF8E1", fg="#222", font=(boton_cfg[6], 14, "bold"), width=12, height=1)
        btn_buscar.pack(pady=10)
        frame_resultados = tk.Frame(self.root, bg=bg)
        frame_resultados.pack(pady=10, fill="both", expand=True)

        def buscar():
            for widget in frame_resultados.winfo_children():
                widget.destroy()
            codigo = entry_codigo.get().strip()
            nombre = entry_nombre.get().strip()
            conn = get_db_connection()
            cursor = conn.cursor()
            if tipo == "alumno":
                query = "SELECT a.codigo, a.nombre_completo FROM alumnos a WHERE (%s='' OR a.codigo=%s) AND (%s='' OR a.nombre_completo LIKE CONCAT('%',%s,'%'))"
                cursor.execute(query, (codigo, codigo, nombre, nombre))
            elif tipo == "curso":
                query = "SELECT codigo, nombre FROM cursos WHERE (%s='' OR codigo=%s) AND (%s='' OR nombre LIKE CONCAT('%',%s,'%'))"
                cursor.execute(query, (codigo, codigo, nombre, nombre))
            elif tipo == "material":
                query = "SELECT codigo_curso, nombre FROM materiales WHERE (%s='' OR codigo_curso=%s) AND (%s='' OR nombre LIKE CONCAT('%',%s,'%'))"
                cursor.execute(query, (codigo, codigo, nombre, nombre))
            resultados: tuple = cursor.fetchall() # type: ignore
            for res in resultados:
                btn = tk.Button(frame_resultados, text=f"{res[0]}   |   {res[1]}", font=(tittle[3], 12), bg="#FFF8E1", fg="#9E2A2F", relief="ridge", width=32, command=lambda r=res: self.show_modificar(tipo, r[0]))
                btn.pack(pady=5)
            if not resultados:
                tk.Label(frame_resultados, text="No se encontraron resultados.", font=(tittle[3], 12), bg=bg, fg="#9E2A2F").pack()
            cursor.close()
            conn.close()
        btn_buscar.config(command=buscar)
        buscar()  # Mostrar todos al inicio

    def show_modificar(self, tipo, codigo):
        # Limpiar la ventana
        for widget in self.root.winfo_children():
            widget.destroy()
        from configuracion import get_config_entrada, get_config_boton, get_db_connection, render_header, get_config_fondo
        bg, size = get_config_fondo()
        tittle = get_config_titulo()
        render_header(self.root, self.nombre_usuario)
        # Botón Volver
        tk.Button(
            self.root, text="Volver", bg="#FFF8E1", fg="#222",
            font=(tittle[3], 10, "bold"), relief="raised",
            command=lambda: self.show_search(tipo)
        ).pack(anchor="nw", padx=15, pady=(5, 0))
        frame = tk.Frame(self.root, bg=bg)
        frame.pack(pady=20)
        entrada_cfg = get_config_entrada()
        boton_cfg = get_config_boton()
        conn = get_db_connection()
        cursor = conn.cursor()
        if tipo == "alumno":
            cursor.execute("SELECT a.codigo, a.nombre_completo, u.password FROM alumnos a JOIN usuarios u ON a.codigo=u.codigo_alumno WHERE a.codigo=%s", (codigo,))
            row = cursor.fetchone()
            if not row:
                messagebox.showerror("Error", "Alumno no encontrado.")
                return
            tk.Label(frame, text="Nombre:", font=(entrada_cfg[3], entrada_cfg[1]), bg=bg, fg=entrada_cfg[2]).grid(row=0, column=0, sticky="e", pady=5)
            entry_nombre = tk.Entry(frame, font=(entrada_cfg[3], 12))
            entry_nombre.insert(0, str(row[1]))
            entry_nombre.grid(row=0, column=1, pady=5)
            tk.Label(frame, text="Contraseña:", font=(entrada_cfg[3], entrada_cfg[1]), bg=bg, fg=entrada_cfg[2]).grid(row=1, column=0, sticky="e", pady=5)
            entry_pass = tk.Entry(frame, font=(entrada_cfg[3], 12))
            entry_pass.insert(0, str(row[2]))
            entry_pass.grid(row=1, column=1, pady=5)
            tk.Button(frame, text="Guardar Cambios", bg=boton_cfg[1], fg=boton_cfg[2], font=(boton_cfg[6], 12, "bold"), command=lambda: self.guardar_alumno(codigo, entry_nombre, entry_pass)).grid(row=2, column=0, columnspan=2, pady=10)
            tk.Button(frame, text="Eliminar Alumno", bg="#E57373", fg="#fff", font=(boton_cfg[6], 12, "bold"), command=lambda: self.eliminar_alumno(codigo)).grid(row=3, column=0, columnspan=2, pady=5)
        elif tipo == "curso":
            cursor.execute("SELECT codigo, nombre FROM cursos WHERE codigo=%s", (codigo,))
            row = cursor.fetchone()
            if not row:
                messagebox.showerror("Error", "Curso no encontrado.")
                return
            tk.Label(frame, text="Código:", font=(entrada_cfg[3], entrada_cfg[1]), bg=bg, fg=entrada_cfg[2]).grid(row=0, column=0, sticky="e", pady=5)
            entry_codigo = tk.Entry(frame, font=(entrada_cfg[3], 12))
            entry_codigo.insert(0, str(row[0]))
            entry_codigo.grid(row=0, column=1, pady=5)
            tk.Label(frame, text="Nombre:", font=(entrada_cfg[3], entrada_cfg[1]), bg=bg, fg=entrada_cfg[2]).grid(row=1, column=0, sticky="e", pady=5)
            entry_nombre = tk.Entry(frame, font=(entrada_cfg[3], 12))
            entry_nombre.insert(0, str(row[1]))
            entry_nombre.grid(row=1, column=1, pady=5)
            tk.Button(frame, text="Guardar Cambios", bg=boton_cfg[1], fg=boton_cfg[2], font=(boton_cfg[6], 12, "bold"), command=lambda: self.guardar_curso(codigo, entry_codigo, entry_nombre)).grid(row=2, column=0, columnspan=2, pady=10)
            tk.Button(frame, text="Eliminar Curso", bg="#E57373", fg="#fff", font=(boton_cfg[6], 12, "bold"), command=lambda: self.eliminar_curso(codigo)).grid(row=3, column=0, columnspan=2, pady=5)
        elif tipo == "material":
            cursor.execute("SELECT id_material, nombre, enlace, codigo_curso FROM materiales WHERE id_material=%s", (codigo,))
            row = cursor.fetchone()
            if not row:
                messagebox.showerror("Error", "Material no encontrado.")
                return
            tk.Label(frame, text="Nombre:", font=(entrada_cfg[3], entrada_cfg[1]), bg=bg, fg=entrada_cfg[2]).grid(row=0, column=0, sticky="e", pady=5)
            entry_nombre = tk.Entry(frame, font=(entrada_cfg[3], 12))
            entry_nombre.insert(0, str(row[1]))
            entry_nombre.grid(row=0, column=1, pady=5)
            tk.Label(frame, text="Enlace:", font=(entrada_cfg[3], entrada_cfg[1]), bg=bg, fg=entrada_cfg[2]).grid(row=1, column=0, sticky="e", pady=5)
            entry_enlace = tk.Entry(frame, font=(entrada_cfg[3], 12))
            entry_enlace.insert(0, str(row[2]))
            entry_enlace.grid(row=1, column=1, pady=5)
            tk.Label(frame, text="Código Curso:", font=(entrada_cfg[3], entrada_cfg[1]), bg=bg, fg=entrada_cfg[2]).grid(row=2, column=0, sticky="e", pady=5)
            entry_codigo_curso = tk.Entry(frame, font=(entrada_cfg[3], 12))
            entry_codigo_curso.insert(0, str(row[3]))
            entry_codigo_curso.grid(row=2, column=1, pady=5)
            tk.Button(frame, text="Guardar Cambios", bg=boton_cfg[1], fg=boton_cfg[2], font=(boton_cfg[6], 12, "bold"), command=lambda: self.guardar_material(codigo, entry_nombre, entry_enlace, entry_codigo_curso)).grid(row=3, column=0, columnspan=2, pady=10)
            tk.Button(frame, text="Eliminar Material", bg="#E57373", fg="#fff", font=(boton_cfg[6], 12, "bold"), command=lambda: self.eliminar_material(codigo)).grid(row=4, column=0, columnspan=2, pady=5)
        cursor.close()
        conn.close()

    def guardar_alumno(self, codigo, entry_nombre, entry_pass):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE alumnos SET nombre_completo=%s WHERE codigo=%s", (entry_nombre.get().strip(), codigo))
        cursor.execute("UPDATE usuarios SET password=%s WHERE codigo_alumno=%s", (entry_pass.get().strip(), codigo))
        conn.commit()
        cursor.close()
        conn.close()
        messagebox.showinfo("Éxito", "Datos de alumno actualizados.")

    def eliminar_alumno(self, codigo):
        if messagebox.askyesno("Confirmar", "¿Seguro que desea eliminar este alumno? Esta acción no se puede deshacer."):
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM usuarios WHERE codigo_alumno=%s", (codigo,))
            cursor.execute("DELETE FROM alumnos WHERE codigo=%s", (codigo,))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Eliminado", "Alumno eliminado correctamente.")
            self.show_search("alumno")

    def guardar_curso(self, codigo, entry_codigo, entry_nombre):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE cursos SET codigo=%s, nombre=%s WHERE codigo=%s", (entry_codigo.get().strip(), entry_nombre.get().strip(), codigo))
        conn.commit()
        cursor.close()
        conn.close()
        messagebox.showinfo("Éxito", "Datos de curso actualizados.")

    def eliminar_curso(self, codigo):
        if messagebox.askyesno("Confirmar", "¿Seguro que desea eliminar este curso? Esta acción no se puede deshacer."):
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM cursos WHERE codigo=%s", (codigo,))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Eliminado", "Curso eliminado correctamente.")
            self.show_search("curso")

    def guardar_material(self, codigo, entry_nombre, entry_enlace, entry_codigo_curso):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE materiales SET nombre=%s, enlace=%s, codigo_curso=%s WHERE id_material=%s", (entry_nombre.get().strip(), entry_enlace.get().strip(), entry_codigo_curso.get().strip(), codigo))
        conn.commit()
        cursor.close()
        conn.close()
        messagebox.showinfo("Éxito", "Datos de material actualizados.")

    def eliminar_material(self, codigo):
        if messagebox.askyesno("Confirmar", "¿Seguro que desea eliminar este material? Esta acción no se puede deshacer."):
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM materiales WHERE id_material=%s", (codigo,))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Eliminado", "Material eliminado correctamente.")
            self.show_search("material")

    def add_logout_button(self):
        """
        Adds a styled 'Cerrar sesión' button at the top-left below the header.
        Should be called after render_header in each page.
        """
        boton_volver_cfg = get_config_boton_volver()
        btn = tk.Button(
            self.root,
            text="Cerrar sesión",
            command=self.on_logout,
            bg=boton_volver_cfg["bg"],
            fg=boton_volver_cfg["fg"],
            font=boton_volver_cfg["font"],
            relief=boton_volver_cfg["relief"]
        )
        btn.pack(anchor=boton_volver_cfg["anchor"], padx=boton_volver_cfg["padx"], pady=boton_volver_cfg["pady"])

class StudentPage(page):
    def __init__(self, root, nombre_usuario, codigo_alumno, on_logout):
        self.root = root
        self.nombre_usuario = nombre_usuario
        self.codigo_alumno = codigo_alumno
        self.on_logout = on_logout
        self.show_student()

    def add_navbar(self):
        bg, _ = get_config_fondo()
        tittle = get_config_titulo()
        nav_frame = tk.Frame(self.root, bg=bg)
        nav_frame.pack(side="bottom", fill="x", pady=10)
        btn_nav_style = {"width": 10, "height": 2, "bg": "#FFF8E1", "fg": "#222", "font": (tittle[3], 10, "bold"), "relief": "raised"}
        tk.Button(nav_frame, text="Inicio", command=self.show_student, **btn_nav_style).pack(side="left", padx=5)
        tk.Button(nav_frame, text="Notas", command=self.show_notas, **btn_nav_style).pack(side="left", padx=5)
        tk.Button(nav_frame, text="Eventos", command=self.show_eventos, **btn_nav_style).pack(side="left", padx=5)
        tk.Button(nav_frame, text="Material", command=self.show_materiales, **btn_nav_style).pack(side="left", padx=5)

    def show_student(self):
        self.clear_window()
        bg, size = get_config_fondo()
        tittle = get_config_titulo()
        logo_cfg = get_config_logo()
        render_header(self.root, self.nombre_usuario)
        self.add_logout_button()
        # Frame centrado
        content = tk.Frame(self.root, bg=bg)
        content.pack(expand=True)
        # Bienvenida
        label_saludo = tk.Label(
            content,
            text=f"¡Hola, {self.nombre_usuario}!",
            font=(tittle[3], tittle[1], "bold"),
            bg=bg,
            fg=tittle[2]
        )
        label_saludo.pack(pady=(10, 10))
        # Logo central
        img = Image.open(logo_cfg[2])
        img = img.resize((180, 180), Image.Resampling.LANCZOS)
        self.logo_img_student = ImageTk.PhotoImage(img)
        logo_label = tk.Label(content, image=self.logo_img_student, bg=bg)
        logo_label.pack(pady=10)
        # Noticias
        noticias_frame = tk.Frame(content, bg=bg)
        noticias_frame.pack(pady=10)
        examen_info = "Sin exámenes próximos"
        evento_info = "Sin eventos próximos"
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT tipo, descripcion, fecha, hora
                FROM eventos
                WHERE tipo LIKE '%examen%'
                  AND fecha >= CURDATE()
                ORDER BY fecha, hora
                LIMIT 1
            """)
            examen = cursor.fetchone()
            if examen:
                examen_info = f"{examen[1]}\n{examen[2]} {examen[3]}"
            cursor.execute("""
                SELECT tipo, descripcion, fecha, hora
                FROM eventos
                WHERE fecha >= CURDATE()
                ORDER BY fecha, hora
                LIMIT 1
            """)
            evento = cursor.fetchone()
            if evento:
                evento_info = f"{evento[1]}\n{evento[2]} {evento[3]}"
            cursor.close()
            conn.close()
        except Exception as e:
            examen_info = f"Error: {e}"
            evento_info = f"Error: {e}"
        noticia_style = {"bg": "#FFF9C4", "bd": 2, "relief": "groove", "padx": 16, "pady": 12}
        left_news = tk.Frame(noticias_frame, **noticia_style)
        left_news.pack(fill="x", padx=10, pady=(0, 8))
        tk.Label(left_news, text="Nota reciente", font=(tittle[3], 12, "bold"), bg="#FFF9C4").pack(anchor="w")
        tk.Label(left_news, text=examen_info, font=(tittle[3], 12), bg="#FFF9C4").pack(anchor="w", pady=(4,0))
        right_news = tk.Frame(noticias_frame, **noticia_style)
        right_news.pack(fill="x", padx=10)
        tk.Label(right_news, text="Próximo evento", font=(tittle[3], 12, "bold"), bg="#FFF9C4").pack(anchor="w")
        tk.Label(right_news, text=evento_info, font=(tittle[3], 12), bg="#FFF9C4").pack(anchor="w", pady=(4,0))
        tk.Frame(self.root, height=2, width=220, bg='#FFF8E1', bd=0, relief="ridge").pack(pady=(10, 10))
        
        self.add_navbar()

    def show_notas(self):
        self.clear_window()
        bg, size = get_config_fondo()
        tittle = get_config_titulo()
        logo_cfg = get_config_logo()
        render_header(self.root, self.nombre_usuario)
        self.add_logout_button()
        content = tk.Frame(self.root, bg=bg)
        content.pack(expand=True)
        tk.Label(content, text="Notas", font=(tittle[3], tittle[1], "bold"), bg=bg, fg=tittle[2]).pack(pady=(30, 10))
        img = Image.open(logo_cfg[2])
        img = img.resize((100, 125), Image.Resampling.LANCZOS)
        self.logo_img_notas = ImageTk.PhotoImage(img)
        tk.Label(content, image=self.logo_img_notas, bg=logo_cfg[1]).pack(pady=10)
        frame_tabla = tk.Frame(content, bg=bg)
        frame_tabla.pack(pady=10)
        headers = ["Curso", "Parcial", "PC1", "PC2", "PC3", "PC4", "Final", "Predicción"]
        for j, h in enumerate(headers):
            tk.Label(frame_tabla, text=h, font=(tittle[3], 10, "bold"), bg=bg, fg="#FFF8E1", padx=8, pady=4, borderwidth=1, relief="solid").grid(row=0, column=j, sticky="nsew")
        if self.codigo_alumno:
            try:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT c.nombre, n.parcial, n.pc1, n.pc2, n.pc3, n.pc4, n.final, n.prediccion
                    FROM notas n
                    JOIN cursos c ON n.codigo_curso = c.codigo
                    WHERE n.codigo_alumno = %s
                """, (self.codigo_alumno,))
                notas: tuple = cursor.fetchall() # type: ignore
                cursor.close()
                conn.close()
                for i, fila in enumerate(notas, start=1):
                    for j, dato in enumerate(fila):
                        tk.Label(frame_tabla, text=str(dato), font=(tittle[3], 10), bg=bg, fg="#FFF8E1", padx=8, pady=4, borderwidth=1, relief="solid").grid(row=i, column=j, sticky="nsew")
                if not notas:
                    tk.Label(frame_tabla, text="No hay notas registradas.", font=(tittle[3], 12), bg=bg, fg="#FFF8E1").grid(row=1, column=0, columnspan=len(headers))
            except Exception as e:
                tk.Label(frame_tabla, text=f"Error al obtener notas: {e}", font=(tittle[3], 12), bg=bg, fg="#FFF8E1").grid(row=1, column=0, columnspan=len(headers))
        else:
            tk.Label(frame_tabla, text="No se proporcionó código de alumno.", font=(tittle[3], 12), bg=bg, fg="#FFF8E1").grid(row=1, column=0, columnspan=len(headers))
        self.add_navbar()

    def show_eventos(self):
        self.clear_window()
        bg, size = get_config_fondo()
        tittle = get_config_titulo()
        logo_cfg = get_config_logo()
        render_header(self.root, self.nombre_usuario)
        self.add_logout_button()

        content = tk.Frame(self.root, bg=bg)
        content.pack(expand=True, fill="both")

        tk.Label(content, text="Eventos", font=(tittle[3], tittle[1], "bold"), bg=bg, fg=tittle[2]).pack(pady=(30, 10))

        img = Image.open(logo_cfg[2])
        img = img.resize((100, 125), Image.Resampling.LANCZOS)
        self.logo_img_eventos = ImageTk.PhotoImage(img)
        tk.Label(content, image=self.logo_img_eventos, bg=logo_cfg[1]).pack(pady=10)

        # Frame centrado para eventos y scrollbar
        eventos_container = tk.Frame(content, bg=bg)
        eventos_container.pack(pady=10)

        # Obtener el ancho de la ventana y calcular el ancho del canvas
        self.root.update_idletasks()
        window_width = self.root.winfo_width()
        canvas_width = int(window_width * 0.65) if window_width > 0 else 500

        # Centrar el canvas y la scrollbar
        inner_container = tk.Frame(eventos_container, bg=bg)
        inner_container.pack(anchor="center")

        scroll_canvas = tk.Canvas(inner_container, bg=bg, highlightthickness=0, width=canvas_width, height=340)
        scroll_canvas.pack(side="left", fill="y", expand=False)

        scrollbar = tk.Scrollbar(inner_container, orient="vertical", command=scroll_canvas.yview)
        scrollbar.pack(side="left", fill="y")

        scroll_canvas.configure(yscrollcommand=scrollbar.set)

        frame_eventos = tk.Frame(scroll_canvas, bg=bg)
        scroll_canvas.create_window((0, 0), window=frame_eventos, anchor="nw")

        def on_frame_configure(event):
            scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all"))
        frame_eventos.bind("<Configure>", on_frame_configure)

        # Centrar el contenedor de eventos
        eventos_container.pack(anchor="center")

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT fecha, tipo, hora, descripcion
                FROM eventos
                ORDER BY fecha, hora
            """)
            eventos: tuple = cursor.fetchall()  # type: ignore
            cursor.close()
            conn.close()

            if eventos:
                for i, (fecha, tipo, hora, descripcion) in enumerate(eventos):
                    card = tk.Frame(frame_eventos, bg="#FFF9C4", bd=2, relief="groove", padx=2, pady=10)
                    card.pack(fill="x", pady=6)

                    # Fecha y hora en la parte superior
                    top = tk.Frame(card, bg="#FFF9C4")
                    top.pack(anchor="w", fill="x")
                    fecha_dt = datetime.datetime.strptime(str(fecha), "%Y-%m-%d")
                    fecha_str = fecha_dt.strftime("%d/%m/%Y")
                    tk.Label(top, text=f"📅 {fecha_str}", font=(tittle[3], 11, "bold"), bg="#FFF9C4", fg="#9E2A2F").pack(side="left")
                    tk.Label(top, text=f"🕒 {hora}", font=(tittle[3], 11), bg="#FFF9C4", fg="#1976D2").pack(side="left", padx=(18, 0))

                    # Tipo y descripción debajo
                    tk.Label(card, text=tipo, font=(tittle[3], 11, "bold"), bg="#FFF9C4", fg="#333").pack(anchor="w", pady=(6, 0))
                    tk.Label(card, text=descripcion, font=(tittle[3], 10), bg="#FFF9C4", fg="#222").pack(anchor="w", pady=(2, 0))
            else:
                tk.Label(frame_eventos, text="No hay eventos registrados.", font=(tittle[3], 12), bg=bg, fg="#FFF8E1").pack()
        except Exception as e:
            tk.Label(frame_eventos, text=f"Error al obtener eventos: {e}", font=(tittle[3], 12), bg=bg, fg="#FFF8E1").pack()

        self.add_navbar()

    def show_materiales(self):
        self.clear_window()
        bg, size = get_config_fondo()
        tittle = get_config_titulo()
        logo_cfg = get_config_logo()
        render_header(self.root, self.nombre_usuario)
        self.add_logout_button()
        content = tk.Frame(self.root, bg=bg)
        content.pack(expand=True)
        tk.Label(content, text="Materiales", font=(tittle[3], tittle[1], "bold"), bg=bg, fg=tittle[2]).pack(pady=(30, 10))
        img = Image.open(logo_cfg[2])
        img = img.resize((100, 125), Image.Resampling.LANCZOS)
        self.logo_img_materiales = ImageTk.PhotoImage(img)
        tk.Label(content, image=self.logo_img_materiales, bg=logo_cfg[1]).pack(pady=10)
        # Filtros
        filtro = tk.Frame(content, bg="#FFF9C4", bd=2, relief="ridge", pady=6, padx=6)
        filtro.pack(fill="x", padx=10)
        tk.Label(filtro, text="Curso:", bg="#FFF9C4", font=(tittle[3], 10, "bold"), fg="#9E2A2F").pack(side="left")
        curso_var = tk.StringVar(value="Todos")
        om = tk.OptionMenu(filtro, curso_var, "Todos")
        om.config(bg="white", fg="#222", activebackground="#FFF8E1", activeforeground="#9E2A2F")
        om.pack(side="left", padx=5)
        tk.Label(filtro, text="Buscar:", bg="#FFF9C4", font=(tittle[3], 10, "bold"), fg="#9E2A2F").pack(side="left", padx=(20,0))
        buscar_var = tk.StringVar()
        tk.Entry(filtro, textvariable=buscar_var, width=28, bg="#FFFDE7", fg="#222").pack(side="left", padx=5)
        # Lista
        lista_frm = tk.Frame(content, bg="#FFFDE7", bd=2, relief="groove")
        lista_frm.pack(fill="both", expand=True, padx=10, pady=6)
        scroll = tk.Scrollbar(lista_frm)
        scroll.pack(side="right", fill="y")
        listbox = tk.Listbox(lista_frm, yscrollcommand=scroll.set, font=(tittle[3], 10), bg="#FFF9C4", fg="#222", selectbackground="#B3C6E7", selectforeground="#222")
        listbox.pack(fill="both", expand=True)
        scroll.config(command=listbox.yview)
        # Botones
        btn_frm = tk.Frame(content, bg="#FFF9C4", pady=6)
        btn_frm.pack(fill="x", padx=10)
        tk.Button(btn_frm, text="Abrir 📂", bg="#9E2A2F", fg="white", activebackground="#B3C6E7", activeforeground="#9E2A2F", command=lambda: abrir()).pack(side="left", padx=6)
        tk.Button(btn_frm, text="Copiar 🔗", bg="#1976D2", fg="white", activebackground="#B3C6E7", activeforeground="#1976D2", command=lambda: copiar()).pack(side="left", padx=6)
        tk.Button(btn_frm, text="Actualizar", bg="#FFF8E1", fg="#9E2A2F", activebackground="#B3C6E7", activeforeground="#9E2A2F", command=lambda: refrescar()).pack(side="right", padx=6)
        # Cargar cursos
        conn = get_db_connection()
        cur  = conn.cursor()
        cur.execute("""
            SELECT c.codigo, c.nombre
            FROM alumnos_cursos ac
            JOIN cursos c ON ac.codigo_curso = c.codigo
            WHERE ac.codigo_alumno = %s
        """, (self.codigo_alumno,))
        for cod, nom in tuple(cur.fetchall()): # type: ignore
            etiqueta = f"{cod} - {nom}"
            om["menu"].add_command(
                label=etiqueta,
                command=tk._setit(curso_var, etiqueta, lambda *_: refrescar())
            )
        conn.close()
        enlaces = []
        palette = {"pdf": "#ffe6e6", "video": "#e8ffe8", "planchas": "#fffad6"}
        def refrescar(*_):
            listbox.delete(0, tk.END)
            enlaces.clear()
            sql = """SELECT m.tipo, m.nombre, m.enlace
                     FROM alumnos_cursos ac
                     JOIN materiales m ON ac.codigo_curso = m.codigo_curso
                     WHERE ac.codigo_alumno = %s"""
            params = [self.codigo_alumno]
            if curso_var.get() != "Todos":
                params.append(curso_var.get().split(" - ")[0])
                sql += " AND ac.codigo_curso = %s"
            if buscar_var.get():
                params.append(f"%{buscar_var.get()}%")
                sql += " AND m.nombre LIKE %s"
            conn = get_db_connection()
            cur  = conn.cursor()
            cur.execute(sql, tuple(params))
            for tipo, nombre, url in tuple(cur.fetchall()): # type: ignore
                listbox.insert(tk.END, f"{tipo:<10}| {nombre}")
                listbox.itemconfig(tk.END, bg=palette.get(tipo, "#FFF9C4"))
                enlaces.append(url)
            conn.close()
        def seleccion():
            if not listbox.curselection():
                messagebox.showwarning("Aviso", "Selecciona un material")
                return None
            return enlaces[listbox.curselection()[0]]
        def abrir():
            url = seleccion()
            if not url: return
            try:
                import sys
                if sys.platform.startswith("win"):
                    import os
                    os.startfile(url)
                elif sys.platform == "darwin":
                    import subprocess
                    subprocess.Popen(["open", url])
                else:
                    import subprocess
                    subprocess.Popen(["xdg-open", url])
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo abrir: {e}")
        def copiar():
            url = seleccion()
            if not url: return
            self.root.clipboard_clear()
            self.root.clipboard_append(url)
            messagebox.showinfo("Copiado", "Enlace copiado al portapapeles")
        buscar_var.trace("w", refrescar)
        curso_var.trace("w", refrescar)
        refrescar()
        self.add_navbar()

    def add_logout_button(self):
        """
        Adds a styled 'Cerrar sesión' button at the top-left below the header.
        Should be called after render_header in each page.
        """
        boton_volver_cfg = get_config_boton_volver()
        btn = tk.Button(
            self.root,
            text="Cerrar sesión",
            command=self.on_logout,
            bg=boton_volver_cfg["bg"],
            fg=boton_volver_cfg["fg"],
            font=boton_volver_cfg["font"],
            relief=boton_volver_cfg["relief"]
        )
        btn.pack(anchor=boton_volver_cfg["anchor"], padx=boton_volver_cfg["padx"], pady=boton_volver_cfg["pady"])

class AppPage(page):
    def __init__(self):
        super().__init__()
        self.root.title("Sistema de Gestión")
        self.root.geometry(get_config_fondo()[1])
        self.root.configure(bg=get_config_fondo()[0])
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.show_login()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_login(self):
        self.clear_window()
        bg, size = get_config_fondo()
        entrada_cfg = get_config_entrada()
        boton_cfg = get_config_boton()
        logo_cfg = get_config_logo()
        tittle = get_config_titulo()
        espacio = tk.Label(self.root, text=" ",bg=bg, height=4) 
        espacio.pack()

        label_saludo = tk.Label(
            self.root,
            text=f"¡Bienvenido a VT0!",
            font=(tittle[3], tittle[1], "bold"),
            bg=bg,
            fg=tittle[2]
        )
        label_saludo.pack()
        img = Image.open(logo_cfg[2])
        img = img.resize((200, 252), Image.Resampling.LANCZOS)
        self.logo_img = ImageTk.PhotoImage(img)
        logo_label = tk.Label(self.root, image=self.logo_img, bg=bg)
        logo_label.pack(pady=(30, 10))

        label_user = tk.Label(self.root, text="Usuario:", font=(entrada_cfg[3], entrada_cfg[1]), bg=bg, fg=entrada_cfg[2])
        label_user.pack(pady=(10, 5))
        self.entry_user = tk.Entry(self.root, font=(entrada_cfg[3], 12))
        self.entry_user.pack(pady=5)

        label_pass = tk.Label(self.root, text="Contraseña:", font=(entrada_cfg[3], entrada_cfg[1]), bg=bg, fg=entrada_cfg[2])
        label_pass.pack(pady=(20, 5))
        self.entry_pass = tk.Entry(self.root, show="*", font=(entrada_cfg[3], 12))
        self.entry_pass.pack(pady=5)

        btn_login = tk.Button(
            self.root,
            text=boton_cfg[0],
            bg=boton_cfg[1],
            fg=boton_cfg[2],
            font=(boton_cfg[6], boton_cfg[3], "bold"),
            width=boton_cfg[4],
            height=boton_cfg[5],
            relief="raised",
            command=self.login
        )
        btn_login.pack(pady=30)

    def login(self):
        username = self.entry_user.get().strip()
        password = self.entry_pass.get().strip()
        if not username or not password:
            messagebox.showwarning("Campos vacíos", "Por favor, ingrese usuario y contraseña.")
            return
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE username=%s AND password=%s", (username, password))
            user: tuple = cursor.fetchone() # type: ignore
            cursor.close()
            conn.close()
            if user:
                rol = user[2]
                codigo_alumno = user[3] if rol == 'alumno' else None
                if rol == 'administrador':
                    self.clear_window()
                    AdminPage(self.root, username, self.show_login)
                else:
                    self.clear_window()
                    StudentPage(self.root, username, codigo_alumno, self.show_login)
            else:
                messagebox.showerror("Error de acceso", "Usuario o contraseña incorrectos.")
        except Exception as e:
            messagebox.showerror("Error de conexión", f"No se pudo conectar a la base de datos.\n{e}")

    def on_closing(self):
        if messagebox.askokcancel("Salir", "¿Quieres salir del programa?"):
            self.root.destroy()

if __name__ == "__main__":
    app = AppPage()
    app.root.mainloop()
