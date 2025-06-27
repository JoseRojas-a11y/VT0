import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from configuracion import page, get_config_entrada, get_config_boton, get_db_connection

class SearchPage(page):
    def __init__(self, nombre_usuario="Administrador", tipo_inicial="alumno"):
        super().__init__()
        self.root.title("Buscar Registros")
        self.root.configure(bg=self.background[0])
        self.root.geometry(self.background[1])
        self.render_header(nombre_usuario)

        # Botón Volver a AdminPage
        tk.Button(
            self.root, text="Volver", bg="#E42110", fg="#222",
            font=(self.tittle[3], 10, "bold"), relief="raised",
            command=self.volver_admin
        ).pack(anchor="nw", padx=15, pady=(5, 0))

        self.tipo = tk.StringVar(value=tipo_inicial)
        self.resultados = []

        # Selector de tipo de entidad
        selector_frame = tk.Frame(self.root, bg=self.background[0])
        selector_frame.pack(pady=(20, 10))
        for tipo, texto in [("alumno", "Alumno"), ("curso", "Curso"), ("material", "Material"), ("notas", "Notas")]:
            tk.Radiobutton(selector_frame, text=texto, variable=self.tipo, value=tipo, bg=self.background[0], fg="#FFF8E1", selectcolor="#FFF8E1", font=(self.tittle[3], 12)).pack(side="left", padx=10)

        # Título de búsqueda
        self.label_titulo = tk.Label(self.root, text="Campos de Búsqueda", font=(self.tittle[3], 16, "bold"), bg=self.background[0], fg="#FFF8E1")
        self.label_titulo.pack(pady=(10, 5))

        # Entradas de búsqueda
        entrada_cfg = get_config_entrada()
        self.frame_busqueda = tk.Frame(self.root, bg=self.background[0])
        self.frame_busqueda.pack(pady=5)
        self.label_codigo = tk.Label(self.frame_busqueda, text="Código:", font=(entrada_cfg[3], entrada_cfg[1]), bg=self.background[0], fg=entrada_cfg[2])
        self.label_codigo.grid(row=0, column=0, padx=5, pady=5)
        self.entry_codigo = tk.Entry(self.frame_busqueda, font=(entrada_cfg[3], 12))
        self.entry_codigo.grid(row=0, column=1, padx=5, pady=5)
        self.label_nombre = tk.Label(self.frame_busqueda, text="Nombre:", font=(entrada_cfg[3], entrada_cfg[1]), bg=self.background[0], fg=entrada_cfg[2])
        self.label_nombre.grid(row=1, column=0, padx=5, pady=5)
        self.entry_nombre = tk.Entry(self.frame_busqueda, font=(entrada_cfg[3], 12))
        self.entry_nombre.grid(row=1, column=1, padx=5, pady=5)
        # Campos para búsqueda de notas
        self.label_curso = tk.Label(self.frame_busqueda, text="Código Curso:", font=(entrada_cfg[3], entrada_cfg[1]), bg=self.background[0], fg=entrada_cfg[2])
        self.entry_curso = tk.Entry(self.frame_busqueda, font=(entrada_cfg[3], 12))

        # Botón buscar
        boton_cfg = get_config_boton()
        self.btn_buscar = tk.Button(self.root, text="Buscar", bg="#B3C6E7", fg="#222", font=(boton_cfg[6], 14, "bold"), width=12, height=1, command=self.buscar)
        self.btn_buscar.pack(pady=10)

        # Resultados
        self.frame_resultados = tk.Frame(self.root, bg=self.background[0])
        self.frame_resultados.pack(pady=10, fill="both", expand=True)

        # Actualiza campos según tipo
        self.tipo.trace_add('write', self.actualizar_campos)
        self.actualizar_campos()

    def actualizar_campos(self, *args):
        # Oculta todos los campos
        self.label_nombre.grid_remove()
        self.entry_nombre.grid_remove()
        self.label_curso.grid_remove()
        self.entry_curso.grid_remove()
        if self.tipo.get() == "notas":
            self.label_codigo.config(text="Código Alumno:")
            self.label_curso.grid(row=1, column=0, padx=5, pady=5)
            self.entry_curso.grid(row=1, column=1, padx=5, pady=5)
        else:
            self.label_codigo.config(text="Código:")
            self.label_nombre.grid(row=1, column=0, padx=5, pady=5)
            self.entry_nombre.grid(row=1, column=1, padx=5, pady=5)

    def buscar(self):
        for widget in self.frame_resultados.winfo_children():
            widget.destroy()
        tipo = self.tipo.get()
        codigo = self.entry_codigo.get().strip()
        nombre = self.entry_nombre.get().strip()
        codigo_curso = self.entry_curso.get().strip()
        conn = get_db_connection()
        cursor = conn.cursor()  # type: ignore  # Forzamos que fetchone/fetchall devuelvan tuplas
        if tipo == "alumno":
            query = "SELECT a.codigo, a.nombre_completo FROM alumnos a WHERE (%s='' OR a.codigo=%s) AND (%s='' OR a.nombre_completo LIKE CONCAT('%',%s,'%'))"
            cursor.execute(query, (codigo, codigo, nombre, nombre))
        elif tipo == "curso":
            query = "SELECT codigo, nombre FROM cursos WHERE (%s='' OR codigo=%s) AND (%s='' OR nombre LIKE CONCAT('%',%s,'%'))"
            cursor.execute(query, (codigo, codigo, nombre, nombre))
        elif tipo == "material":
            query = "SELECT id_material, nombre FROM materiales WHERE (%s='' OR id_material=%s) AND (%s='' OR nombre LIKE CONCAT('%',%s,'%'))"
            cursor.execute(query, (codigo, codigo, nombre, nombre))
        else:  # notas
            query = "SELECT codigo_alumno, codigo_curso FROM notas WHERE (%s='' OR codigo_alumno=%s) AND (%s='' OR codigo_curso=%s)"
            cursor.execute(query, (codigo, codigo, codigo_curso, codigo_curso))
        resultados: tuple = cursor.fetchall() # type: ignore
        for res in resultados:
            if tipo == "notas":
                btn = tk.Button(self.frame_resultados, text=f"{res[0]}   |   {res[1]}", font=(self.tittle[3], 12), bg="#FFF8E1", fg="#9E2A2F", relief="ridge", width=32, command=lambda r=res: self.abrir_modificar_nota(r[0], r[1]))
            else:
                btn = tk.Button(self.frame_resultados, text=f"{res[0]}   |   {res[1]}", font=(self.tittle[3], 12), bg="#FFF8E1", fg="#9E2A2F", relief="ridge", width=32, command=lambda r=res: self.abrir_modificar(r[0]))
            btn.pack(pady=5)
        if not resultados:
            tk.Label(self.frame_resultados, text="No se encontraron resultados.", font=(self.tittle[3], 12), bg=self.background[0], fg="#FFF8E1").pack()
        cursor.close()
        conn.close()

    def abrir_modificar(self, codigo):
        tipo = self.tipo.get()
        self.root.destroy()
        from Apps.ModificarPage import ModificarPage
        ModificarPage(tipo, codigo)

    def abrir_modificar_nota(self, codigo_alumno, codigo_curso):
        self.root.destroy()
        from Apps.ModificarPage import ModificarPage
        ModificarPage("notas", (codigo_alumno, codigo_curso))

    def volver_admin(self):
        self.root.destroy()
        from Apps.AdminPage import page_admin
        page_admin(nombre_usuario="Administrador")

if __name__ == "__main__":
    app = SearchPage()
    app.root.mainloop()
