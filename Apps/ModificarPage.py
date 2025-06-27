import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from configuracion import page, get_config_entrada, get_config_boton, get_db_connection

class ModificarPage(page):
    def __init__(self, tipo, codigo, nombre_usuario="Administrador"):
        super().__init__()
        self.tipo = tipo
        self.codigo = codigo
        self.root.title("Modificar Registro")
        self.root.configure(bg=self.background[0])
        self.root.geometry(self.background[1])
        self.render_header(nombre_usuario)

        tk.Button(
            self.root, text="Volver", bg="#B3C6E7", fg="#222",
            font=(self.tittle[3], 10, "bold"), relief="raised",
            command=self.volver_busqueda
        ).pack(anchor="nw", padx=15, pady=(5, 0))

        self.frame = tk.Frame(self.root, bg=self.background[0])
        self.frame.pack(pady=20)
        self.crear_formulario()

    def volver_busqueda(self):
        self.root.destroy()
        from Apps.SearchPage import SearchPage
        SearchPage(nombre_usuario="Administrador", tipo_inicial=self.tipo)

    def crear_formulario(self):
        entrada_cfg = get_config_entrada()
        boton_cfg = get_config_boton()
        conn = get_db_connection()
        cursor = conn.cursor()
        if self.tipo == "alumno":
            cursor.execute("SELECT a.codigo, a.nombre_completo, u.password FROM alumnos a JOIN usuarios u ON a.codigo=u.codigo_alumno WHERE a.codigo=%s", (self.codigo,))
            row: tuple = cursor.fetchone()  # type: ignore
            if not row:
                messagebox.showerror("Error", "Alumno no encontrado.")
                self.root.destroy()
                return
            tk.Label(self.frame, text="Nombre:", font=(entrada_cfg[3], entrada_cfg[1]), bg=self.background[0], fg=entrada_cfg[2]).grid(row=0, column=0, sticky="e", pady=5)
            entry_nombre = tk.Entry(self.frame, font=(entrada_cfg[3], 12))
            entry_nombre.insert(0, str(row[1]))  # type: ignore
            entry_nombre.grid(row=0, column=1, pady=5)
            tk.Label(self.frame, text="Contraseña:", font=(entrada_cfg[3], entrada_cfg[1]), bg=self.background[0], fg=entrada_cfg[2]).grid(row=1, column=0, sticky="e", pady=5)
            entry_pass = tk.Entry(self.frame, font=(entrada_cfg[3], 12))
            entry_pass.insert(0, str(row[2]))  # type: ignore
            entry_pass.grid(row=1, column=1, pady=5)
            tk.Button(self.frame, text="Guardar Cambios", bg=boton_cfg[1], fg=boton_cfg[2], font=(boton_cfg[6], 12, "bold"), command=lambda: self.guardar_alumno(entry_nombre, entry_pass)).grid(row=2, column=0, columnspan=2, pady=10)
            tk.Button(self.frame, text="Eliminar Alumno", bg="#E57373", fg="#fff", font=(boton_cfg[6], 12, "bold"), command=self.eliminar_alumno).grid(row=3, column=0, columnspan=2, pady=5)
        elif self.tipo == "curso":
            cursor.execute("SELECT codigo, nombre FROM cursos WHERE codigo=%s", (self.codigo,))
            row: tuple = cursor.fetchone()  # type: ignore
            if not row:
                messagebox.showerror("Error", "Curso no encontrado.")
                self.root.destroy()
                return
            tk.Label(self.frame, text="Código:", font=(entrada_cfg[3], entrada_cfg[1]), bg=self.background[0], fg=entrada_cfg[2]).grid(row=0, column=0, sticky="e", pady=5)
            entry_codigo = tk.Entry(self.frame, font=(entrada_cfg[3], 12))
            entry_codigo.insert(0, str(row[0]))  # type: ignore
            entry_codigo.grid(row=0, column=1, pady=5)
            tk.Label(self.frame, text="Nombre:", font=(entrada_cfg[3], entrada_cfg[1]), bg=self.background[0], fg=entrada_cfg[2]).grid(row=1, column=0, sticky="e", pady=5)
            entry_nombre = tk.Entry(self.frame, font=(entrada_cfg[3], 12))
            entry_nombre.insert(0, str(row[1]))  # type: ignore
            entry_nombre.grid(row=1, column=1, pady=5)
            tk.Button(self.frame, text="Guardar Cambios", bg=boton_cfg[1], fg=boton_cfg[2], font=(boton_cfg[6], 12, "bold"), command=lambda: self.guardar_curso(entry_codigo, entry_nombre)).grid(row=2, column=0, columnspan=2, pady=10)
            tk.Button(self.frame, text="Eliminar Curso", bg="#E57373", fg="#fff", font=(boton_cfg[6], 12, "bold"), command=self.eliminar_curso).grid(row=3, column=0, columnspan=2, pady=5)
        elif self.tipo == "notas":
            codigo_alumno, codigo_curso = self.codigo
            cursor.execute("SELECT parcial, pc1, pc2, pc3, pc4, final, prediccion FROM notas WHERE codigo_alumno=%s AND codigo_curso=%s", (codigo_alumno, codigo_curso))
            row: tuple = cursor.fetchone()  # type: ignore
            if not row:
                messagebox.showerror("Error", "Notas no encontradas.")
                self.root.destroy()
                return
            labels = ["Parcial", "PC1", "PC2", "PC3", "PC4", "Final", "Predicción"]
            entries = []
            for i, label in enumerate(labels):
                tk.Label(self.frame, text=label+":", font=(entrada_cfg[3], entrada_cfg[1]), bg=self.background[0], fg=entrada_cfg[2]).grid(row=i, column=0, sticky="e", pady=5)
                entry = tk.Entry(self.frame, font=(entrada_cfg[3], 12))
                entry.insert(0, str(row[i]))  # type: ignore
                entry.grid(row=i, column=1, pady=5)
                entries.append(entry)
                if label == "Predicción":
                    entry.config(state="readonly", disabledbackground="#EEE")
            tk.Button(self.frame, text="Guardar Cambios", bg=boton_cfg[1], fg=boton_cfg[2], font=(boton_cfg[6], 12, "bold"), command=lambda: self.guardar_notas(codigo_alumno, codigo_curso, entries)).grid(row=7, column=0, columnspan=2, pady=10)
            tk.Button(self.frame, text="Eliminar Notas", bg="#E57373", fg="#fff", font=(boton_cfg[6], 12, "bold"), command=lambda: self.eliminar_notas(codigo_alumno, codigo_curso)).grid(row=8, column=0, columnspan=2, pady=5)
        else:
            cursor.execute("SELECT id_material, nombre, enlace, codigo_curso FROM materiales WHERE id_material=%s", (self.codigo,))
            row: tuple = cursor.fetchone()  # type: ignore
            if not row:
                messagebox.showerror("Error", "Material no encontrado.")
                self.root.destroy()
                return
            tk.Label(self.frame, text="Nombre:", font=(entrada_cfg[3], entrada_cfg[1]), bg=self.background[0], fg=entrada_cfg[2]).grid(row=0, column=0, sticky="e", pady=5)
            entry_nombre = tk.Entry(self.frame, font=(entrada_cfg[3], 12))
            entry_nombre.insert(0, str(row[1]))  # type: ignore
            entry_nombre.grid(row=0, column=1, pady=5)
            tk.Label(self.frame, text="Enlace:", font=(entrada_cfg[3], entrada_cfg[1]), bg=self.background[0], fg=entrada_cfg[2]).grid(row=1, column=0, sticky="e", pady=5)
            entry_enlace = tk.Entry(self.frame, font=(entrada_cfg[3], 12))
            entry_enlace.insert(0, str(row[2]))  # type: ignore
            entry_enlace.grid(row=1, column=1, pady=5)
            tk.Label(self.frame, text="Código Curso:", font=(entrada_cfg[3], entrada_cfg[1]), bg=self.background[0], fg=entrada_cfg[2]).grid(row=2, column=0, sticky="e", pady=5)
            entry_codigo_curso = tk.Entry(self.frame, font=(entrada_cfg[3], 12))
            entry_codigo_curso.insert(0, str(row[3]))  # type: ignore
            entry_codigo_curso.grid(row=2, column=1, pady=5)
            tk.Button(self.frame, text="Guardar Cambios", bg=boton_cfg[1], fg=boton_cfg[2], font=(boton_cfg[6], 12, "bold"), command=lambda: self.guardar_material(entry_nombre, entry_enlace, entry_codigo_curso)).grid(row=3, column=0, columnspan=2, pady=10)
            tk.Button(self.frame, text="Eliminar Material", bg="#E57373", fg="#fff", font=(boton_cfg[6], 12, "bold"), command=self.eliminar_material).grid(row=4, column=0, columnspan=2, pady=5)
        cursor.close()
        conn.close()

    def guardar_alumno(self, entry_nombre, entry_pass):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE alumnos SET nombre_completo=%s WHERE codigo=%s", (entry_nombre.get().strip(), self.codigo))
        cursor.execute("UPDATE usuarios SET password=%s WHERE codigo_alumno=%s", (entry_pass.get().strip(), self.codigo))
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

    def guardar_curso(self, entry_codigo, entry_nombre):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE cursos SET codigo=%s, nombre=%s WHERE codigo=%s", (entry_codigo.get().strip(), entry_nombre.get().strip(), self.codigo))
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

    def guardar_notas(self, codigo_alumno, codigo_curso, entries):
        # Calcula la predicción como el promedio de las otras notas (sin predicción)
        try:
            notas = [float(entries[i].get()) for i in range(6)]
            prediccion = sum(notas) / len(notas)
        except Exception:
            messagebox.showerror("Error", "Verifica que todas las notas sean números válidos.")
            return
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE notas SET parcial=%s, pc1=%s, pc2=%s, pc3=%s, pc4=%s, final=%s, prediccion=%s
            WHERE codigo_alumno=%s AND codigo_curso=%s
        """, (*notas, prediccion, codigo_alumno, codigo_curso))
        conn.commit()
        cursor.close()
        conn.close()
        messagebox.showinfo("Éxito", "Notas actualizadas y predicción recalculada.")

    def eliminar_notas(self, codigo_alumno, codigo_curso):
        if messagebox.askyesno("Confirmar", "¿Seguro que desea eliminar estas notas? Esta acción no se puede deshacer."):
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM notas WHERE codigo_alumno=%s AND codigo_curso=%s", (codigo_alumno, codigo_curso))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Eliminado", "Notas eliminadas correctamente.")
            self.root.destroy()

    def guardar_material(self, entry_nombre, entry_enlace, entry_codigo_curso):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE materiales SET nombre=%s, enlace=%s, codigo_curso=%s WHERE id_material=%s", (entry_nombre.get().strip(), entry_enlace.get().strip(), entry_codigo_curso.get().strip(), self.codigo))
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
    app = ModificarPage("alumno", "A001")
    app.root.mainloop()
