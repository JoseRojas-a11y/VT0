import tkinter as tk
from tkinter import messagebox
import mysql.connector

# Conexión a la base de datos
def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="JoSeSiTo%_10",  # Ajusta tu contraseña si es necesario
        database="db_vt0"
    )

# Ventana para modificar notas (solo administrador)
def ventana_admin():
    admin_win = tk.Toplevel()
    admin_win.title("Modificar Notas")

    tk.Label(admin_win, text="Código del Alumno:").grid(row=0, column=0)
    tk.Label(admin_win, text="Código del Curso:").grid(row=1, column=0)

    entry_alumno = tk.Entry(admin_win)
    entry_curso = tk.Entry(admin_win)
    entry_alumno.grid(row=0, column=1)
    entry_curso.grid(row=1, column=1)

    def cargar_notas():
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT parcial, pc1, pc2, pc3, pc4, final, prediccion
            FROM notas
            WHERE codigo_alumno = %s AND codigo_curso = %s
        """, (entry_alumno.get(), entry_curso.get()))
        resultado = cursor.fetchone()
        conn.close()

        if resultado:
            for i, valor in enumerate(resultado):
                entradas[i].delete(0, tk.END)
                entradas[i].insert(0, str(valor))
        else:
            messagebox.showerror("Error", "Notas no encontradas")

    def guardar():
        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE notas SET parcial=%s, pc1=%s, pc2=%s, pc3=%s, pc4=%s, final=%s, prediccion=%s
                WHERE codigo_alumno = %s AND codigo_curso = %s
            """, tuple(e.get() for e in entradas) + (entry_alumno.get(), entry_curso.get()))
            conn.commit()
            messagebox.showinfo("Éxito", "Notas actualizadas correctamente")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()

    tk.Button(admin_win, text="Cargar Notas", command=cargar_notas).grid(row=2, columnspan=2, pady=5)

    campos = ["Parcial", "PC1", "PC2", "PC3", "PC4", "Final", "Prediccion"]
    entradas = []
    for i, campo in enumerate(campos):
        tk.Label(admin_win, text=campo + ":").grid(row=3 + i, column=0)
        e = tk.Entry(admin_win)
        e.grid(row=3 + i, column=1)
        entradas.append(e)

    tk.Button(admin_win, text="Guardar Cambios", command=guardar).grid(row=10, columnspan=2, pady=10)

# Ventana para que un alumno vea sus notas, cursos, eventos y materiales
def ventana_alumno(usuario):
    alumno_win = tk.Toplevel()
    alumno_win.title("Panel del Alumno")

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT codigo_alumno FROM usuarios WHERE username = %s", (usuario,))
    codigo_alumno_row: tuple = cursor.fetchone() # type: ignore
    if not codigo_alumno_row:
        messagebox.showerror("Error", "No se encontró el alumno para este usuario")
        conn.close()
        return
    codigo_alumno = codigo_alumno_row[0] # type: str
    conn.close()

    def mostrar_notas():
        notas_win = tk.Toplevel(alumno_win)
        notas_win.title("Notas")
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.nombre, n.parcial, n.pc1, n.pc2, n.pc3, n.pc4, n.final, n.prediccion
            FROM notas n
            JOIN cursos c ON n.codigo_curso = c.codigo
            WHERE n.codigo_alumno = %s
        """, (codigo_alumno,))
        notas = cursor.fetchall()
        conn.close()
        headers = ["Curso", "Parcial", "PC1", "PC2", "PC3", "PC4", "Final", "Prediccion"]
        for j, h in enumerate(headers):
            tk.Label(notas_win, text=h, font=("Arial", 10, "bold"), padx=10).grid(row=0, column=j, sticky="w")
        for i, fila in enumerate(notas, start=1):
            for j, dato in enumerate(fila):
                tk.Label(notas_win, text=str(dato), padx=10).grid(row=i, column=j, sticky="w")

    def mostrar_eventos():
        eventos_win = tk.Toplevel(alumno_win)
        eventos_win.title("Eventos")
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT fecha, tipo, hora, descripcion
            FROM eventos
            ORDER BY fecha, hora
        """)
        eventos = cursor.fetchall()
        conn.close()

        from collections import defaultdict
        import datetime
        eventos_por_fecha = defaultdict(list)
        for fecha, tipo, hora, descripcion in eventos:
            eventos_por_fecha[fecha].append((tipo, hora, descripcion))

        row = 0
        for fecha in sorted(eventos_por_fecha):
            fecha_dt = datetime.datetime.strptime(str(fecha), "%Y-%m-%d")
            fecha_str = fecha_dt.strftime("%A %d de %B del %Y").capitalize()
            tk.Label(eventos_win, text=fecha_str, font=("Arial", 12, "bold"), fg="orange").grid(row=row, column=0, columnspan=4, sticky="w", pady=(10,0))
            row += 1
            for tipo, hora, descripcion in eventos_por_fecha[fecha]:
                tk.Label(eventos_win, text=tipo, font=("Arial", 10, "bold")).grid(row=row, column=0, sticky="w")
                tk.Label(eventos_win, text=f"🕒 {hora}", fg="blue").grid(row=row, column=1, sticky="w")
                tk.Label(eventos_win, text=descripcion, fg="navy").grid(row=row, column=2, sticky="w")
                row += 1

    def mostrar_materiales():
        materiales_win = tk.Toplevel(alumno_win)
        materiales_win.title("Materiales")
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT m.tipo, m.nombre, m.enlace
            FROM alumnos_cursos ac
            JOIN materiales m ON ac.codigo_curso = m.codigo_curso
            WHERE ac.codigo_alumno = %s
        """, (codigo_alumno,))
        materiales = cursor.fetchall()
        conn.close()
        headers = ["Tipo", "Nombre", "Enlace"]
        for j, h in enumerate(headers):
            tk.Label(materiales_win, text=h, font=("Arial", 10, "bold")).grid(row=0, column=j)
        for i, fila in enumerate(materiales, start=1):
            for j, dato in enumerate(fila):
                tk.Label(materiales_win, text=str(dato)).grid(row=i, column=j)

    tk.Label(alumno_win, text="¿Qué deseas ver?", font=("Arial", 14, "bold")).pack(pady=10)
    tk.Button(alumno_win, text="Ver Notas", width=20, command=mostrar_notas).pack(pady=5)
    tk.Button(alumno_win, text="Ver Eventos", width=20, command=mostrar_eventos).pack(pady=5)
    tk.Button(alumno_win, text="Ver Materiales", width=20, command=mostrar_materiales).pack(pady=5)

# Verificar login
def verificar_login():
    usuario = entry_usuario.get()
    clave = entry_password.get()

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT password, rol FROM usuarios WHERE username = %s", (usuario,))
    resultado = cursor.fetchone()
    conn.close()

    if resultado:
        password_bd, rol = resultado
        if clave == password_bd:
            messagebox.showinfo("Éxito", f"Bienvenido {usuario} ({rol})")
            if rol == "administrador":
                ventana_admin()
            elif rol == "alumno":
                ventana_alumno(usuario)
        else:
            messagebox.showerror("Error", "Contraseña incorrecta")
    else:
        messagebox.showerror("Error", "Usuario no encontrado")

# Interfaz principal
root = tk.Tk()
root.title("Login - Sistema Escolar")

# Widgets
frame = tk.Frame(root, padx=20, pady=20)
frame.pack()

tk.Label(frame, text="Usuario:").grid(row=0, column=0, pady=5)
entry_usuario = tk.Entry(frame)
entry_usuario.grid(row=0, column=1, pady=5)

tk.Label(frame, text="Contraseña:").grid(row=1, column=0, pady=5)
entry_password = tk.Entry(frame, show="*")
entry_password.grid(row=1, column=1, pady=5)

tk.Button(frame, text="Iniciar sesión", command=verificar_login).grid(row=2, columnspan=2, pady=10)

root.mainloop()
