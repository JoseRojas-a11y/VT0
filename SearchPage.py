import tkinter as tk
from tkinter import messagebox
from configuracion import page, get_config_entrada, get_config_boton, get_db_connection

class SearchPage(page):
    def __init__(self, nombre_usuario="Administrador", tipo_inicial="alumno"):
        super().__init__()
        self.root.title("Buscar Registros")
        self.root.configure(bg=self.background[0])
        self.root.geometry(self.background[1])
        self.render_header(nombre_usuario)

        self.tipo = tk.StringVar(value=tipo_inicial)
        self.resultados = []

        # Selector de tipo de entidad
        selector_frame = tk.Frame(self.root, bg=self.background[0])
        selector_frame.pack(pady=(20, 10))
        for tipo, texto in [("alumno", "Alumno"), ("curso", "Curso"), ("material", "Material")]:
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

        # Botón buscar
        boton_cfg = get_config_boton()
        self.btn_buscar = tk.Button(self.root, text="Buscar", bg="#B3C6E7", fg="#222", font=(boton_cfg[6], 14, "bold"), width=12, height=1, command=self.buscar)
        self.btn_buscar.pack(pady=10)

        # Resultados
        self.frame_resultados = tk.Frame(self.root, bg=self.background[0])
        self.frame_resultados.pack(pady=10, fill="both", expand=True)

    def buscar(self):
        for widget in self.frame_resultados.winfo_children():
            widget.destroy()
        tipo = self.tipo.get()
        codigo = self.entry_codigo.get().strip()
        nombre = self.entry_nombre.get().strip()
        conn = get_db_connection()
        cursor = conn.cursor()
        if tipo == "alumno":
            query = "SELECT a.codigo, a.nombre_completo FROM alumnos a WHERE (%s='' OR a.codigo=%s) AND (%s='' OR a.nombre_completo LIKE CONCAT('%',%s,'%'))"
            cursor.execute(query, (codigo, codigo, nombre, nombre))
        elif tipo == "curso":
            query = "SELECT codigo, nombre FROM cursos WHERE (%s='' OR codigo=%s) AND (%s='' OR nombre LIKE CONCAT('%',%s,'%'))"
            cursor.execute(query, (codigo, codigo, nombre, nombre))
        else:
            query = "SELECT id_material, nombre FROM materiales WHERE (%s='' OR id_material=%s) AND (%s='' OR nombre LIKE CONCAT('%',%s,'%'))"
            cursor.execute(query, (codigo, codigo, nombre, nombre))
        resultados = cursor.fetchall() or []
        for res in resultados:
            btn = tk.Button(self.frame_resultados, text=f"{res[0]}   |   {res[1]}", font=(self.tittle[3], 12), bg="#FFF8E1", fg="#9E2A2F", relief="ridge", width=32, command=lambda r=res: self.abrir_modificar(r[0]))
            btn.pack(pady=5)
        if not resultados:
            tk.Label(self.frame_resultados, text="No se encontraron resultados.", font=(self.tittle[3], 12), bg=self.background[0], fg="#FFF8E1").pack()
        cursor.close()
        conn.close()

    def abrir_modificar(self, codigo):
        tipo = self.tipo.get()
        self.root.destroy()
        from ModificarPage import ModificarPage
        ModificarPage(tipo, codigo)

if __name__ == "__main__":
    app = SearchPage()
    app.root.mainloop()
