import tkinter as tk
from tkinter import messagebox
from config import page, get_config_entrada, get_config_boton, get_db_connection

class ModificarPage(page):
    def __init__(self, tipo, codigo, nombre_usuario="Administrador"):
        super().__init__()
        self.tipo = tipo
        self.codigo = codigo
        self.root.title("Modificar Registro")
        self.root.configure(bg=self.background[0])
        self.root.geometry(self.background[1])
        self.render_header(nombre_usuario)

        # Botón Volver
        self.btn_volver = tk.Button(self.root, text="Volver", bg="#B3C6E7", fg="#222", font=(self.tittle[3], 10, "bold"), relief="raised", command=self.volver_busqueda)
        self.btn_volver.pack(anchor="nw", padx=15, pady=(5, 0))

        self.frame = tk.Frame(self.root, bg=self.background[0])
        self.frame.pack(pady=20)
        self.datos = {}
        self.crear_formulario()

    def volver_busqueda(self):
        self.root.destroy()
        from SearchPage import SearchPage
        SearchPage(nombre_usuario="Administrador", tipo_inicial=self.tipo)

    def crear_formulario(self):
        entrada_cfg = get_config_entrada()
        boton_cfg = get_config_boton()
        conn = get_db_connection()
        cursor = conn.cursor()
        if self.tipo == "alumno":
            cursor.execute("SELECT a.codigo, a.nombre_completo, u.password FROM alumnos a JOIN usuarios u ON a.codigo=u.codigo_alumno WHERE a.codigo=%s", (self.codigo,))
            row = cursor.fetchone()
            if not row:
                messagebox.showerror("Error", "Alumno no encontrado.")
                self.root.destroy()
                return
            self.datos = {"codigo": row[0], "nombre": row[1], "password": row[2]}
            # Nombre
            tk.Label(self.frame, text="Nombre:", font=(entrada_cfg[3], entrada_cfg[1]), bg=self.background[0], fg=entrada_cfg[2]).grid(row=0, column=0, sticky="e", pady=5)
            self.entry_nombre = tk.Entry(self.frame, font=(entrada_cfg[3], 12))
            self.entry_nombre.insert(0, self.datos["nombre"])
            self.entry_nombre.grid(row=0, column=1, pady=5)
            # Contraseña
            tk.Label(self.frame, text="Contraseña:", font=(entrada_cfg[3], entrada_cfg[1]), bg=self.background[0], fg=entrada_cfg[2]).grid(row=1, column=0, sticky="e", pady=5)
            self.entry_pass = tk.Entry(self.frame, font=(entrada_cfg[3], 12))
            self.entry_pass.insert(0, self.datos["password"])
            self.entry_pass.grid(row=1, column=1, pady=5)
            # Botón guardar
            tk.Button(self.frame, text="Guardar Cambios", bg=boton_cfg[1], fg=boton_cfg[2], font=(boton_cfg[6], 12, "bold"), command=self.guardar_alumno).grid(row=2, column=0, columnspan=2, pady=10)
            # Botón eliminar
            tk.Button(self.frame, text="Eliminar Alumno", bg="#E57373", fg="#fff", font=(boton_cfg[6], 12, "bold"), command=self.eliminar_alumno).grid(row=3, column=0, columnspan=2, pady=5)
        elif self.tipo == "curso":
            cursor.execute("SELECT codigo, nombre FROM cursos WHERE codigo=%s", (self.codigo,))
            row = cursor.fetchone()
            if not row:
                messagebox.showerror("Error", "Curso no encontrado.")
                self.root.destroy()
                return
            self.datos = {"codigo": row[0], "nombre": row[1]}
            tk.Label(self.frame, text="Código:", font=(entrada_cfg[3], entrada_cfg[1]), bg=self.background[0], fg=entrada_cfg[2]).grid(row=0, column=0, sticky="e", pady=5)
            self.entry_codigo = tk.Entry(self.frame, font=(entrada_cfg[3], 12))
            self.entry_codigo.insert(0, self.datos["codigo"])
            self.entry_codigo.grid(row=0, column=1, pady=5)
            tk.Label(self.frame, text="Nombre:", font=(entrada_cfg[3], entrada_cfg[1]), bg=self.background[0], fg=entrada_cfg[2]).grid(row=1, column=0, sticky="e", pady=5)
            self.entry_nombre = tk.Entry(self.frame, font=(entrada_cfg[3], 12))
            self.entry_nombre.insert(0, self.datos["nombre"])
            self.entry_nombre.grid(row=1, column=1, pady=5)
            tk.Button(self.frame, text="Guardar Cambios", bg=boton_cfg[1], fg=boton_cfg[2], font=(boton_cfg[6], 12, "bold"), command=self.guardar_curso).grid(row=2, column=0, columnspan=2, pady=10)
            tk.Button(self.frame, text="Eliminar Curso", bg="#E57373", fg="#fff", font=(boton_cfg[6], 12, "bold"), command=self.eliminar_curso).grid(row=3, column=0, columnspan=2, pady=5)
        else:
            cursor.execute("SELECT id_material, nombre, enlace, codigo_curso FROM materiales WHERE id_material=%s", (self.codigo,))
            row = cursor.fetchone()
            if not row:
                messagebox.showerror("Error", "Material no encontrado.")
                self.root.destroy()
                return
            self.datos = {"id_material": row[0], "nombre": row[1], "enlace": row[2], "codigo_curso": row[3]}
            tk.Label(self.frame, text="Nombre:", font=(entrada_cfg[3], entrada_cfg[1]), bg=self.background[0], fg=entrada_cfg[2]).grid(row=0, column=0, sticky="e", pady=5)
            self.entry_nombre = tk.Entry(self.frame, font=(entrada_cfg[3], 12))
            self.entry_nombre.insert(0, self.datos["nombre"])
            self.entry_nombre.grid(row=0, column=1, pady=5)
            tk.Label(self.frame, text="Enlace:", font=(entrada_cfg[3], entrada_cfg[1]), bg=self.background[0], fg=entrada_cfg[2]).grid(row=1, column=0, sticky="e", pady=5)
            self.entry_enlace = tk.Entry(self.frame, font=(entrada_cfg[3], 12))
            self.entry_enlace.insert(0, self.datos["enlace"])
            self.entry_enlace.grid(row=1, column=1, pady=5)
            tk.Label(self.frame, text="Código Curso:", font=(entrada_cfg[3], entrada_cfg[1]), bg=self.background[0], fg=entrada_cfg[2]).grid(row=2, column=0, sticky="e", pady=5)
            self.entry_codigo_curso = tk.Entry(self.frame, font=(entrada_cfg[3], 12))
            self.entry_codigo_curso.insert(0, self.datos["codigo_curso"])
            self.entry_codigo_curso.grid(row=2, column=1, pady=5)
            tk.Button(self.frame, text="Guardar Cambios", bg=boton_cfg[1], fg=boton_cfg[2], font=(boton_cfg[6], 12, "bold"), command=self.guardar_material).grid(row=3, column=0, columnspan=2, pady=10)
            tk.Button(self.frame, text="Eliminar Material", bg="#E57373", fg="#fff", font=(boton_cfg[6], 12, "bold"), command=self.eliminar_material).grid(row=4, column=0, columnspan=2, pady=5)
        cursor.close()
        conn.close()

    def guardar_alumno(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        nuevo_nombre = self.entry_nombre.get().strip()
        nueva_pass = self.entry_pass.get().strip()
        cursor.execute("UPDATE alumnos SET nombre_completo=%s WHERE codigo=%s", (nuevo_nombre, self.codigo))
        cursor.execute("UPDATE usuarios SET password=%s WHERE codigo_alumno=%s", (nueva_pass, self.codigo))
        conn.commit()
        cursor.close()
        conn.close()
        messagebox.showinfo("Éxito", "Datos de alumno actualizados.")

    def eliminar_alumno(self):
        if messagebox.askyesno("Confirmar", "¿Seguro que desea eliminar este alumno? Esta acción no se puede deshacer."):
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM usuarios WHERE codigo_alumno=%s", (self.codigo,))
            cursor.execute("DELETE FROM alumnos WHERE codigo=%s", (self.codigo,))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Eliminado", "Alumno eliminado correctamente.")
            self.root.destroy()

    def guardar_curso(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        nuevo_codigo = self.entry_codigo.get().strip()
        nuevo_nombre = self.entry_nombre.get().strip()
        cursor.execute("UPDATE cursos SET codigo=%s, nombre=%s WHERE codigo=%s", (nuevo_codigo, nuevo_nombre, self.codigo))
        conn.commit()
        cursor.close()
        conn.close()
        messagebox.showinfo("Éxito", "Datos de curso actualizados.")

    def eliminar_curso(self):
        if messagebox.askyesno("Confirmar", "¿Seguro que desea eliminar este curso? Esta acción no se puede deshacer."):
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM cursos WHERE codigo=%s", (self.codigo,))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Eliminado", "Curso eliminado correctamente.")
            self.root.destroy()

    def guardar_material(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        nuevo_nombre = self.entry_nombre.get().strip()
        nuevo_enlace = self.entry_enlace.get().strip()
        nuevo_codigo_curso = self.entry_codigo_curso.get().strip()
        cursor.execute("UPDATE materiales SET nombre=%s, enlace=%s, codigo_curso=%s WHERE id_material=%s", (nuevo_nombre, nuevo_enlace, nuevo_codigo_curso, self.codigo))
        conn.commit()
        cursor.close()
        conn.close()
        messagebox.showinfo("Éxito", "Datos de material actualizados.")

    def eliminar_material(self):
        if messagebox.askyesno("Confirmar", "¿Seguro que desea eliminar este material? Esta acción no se puede deshacer."):
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM materiales WHERE id_material=%s", (self.codigo,))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Eliminado", "Material eliminado correctamente.")
            self.root.destroy()

if __name__ == "__main__":
    # Ejemplo de uso: ModificarPage("alumno", "A001")
    app = ModificarPage("alumno", "A001")
    app.root.mainloop()
