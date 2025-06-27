import tkinter as tk
from tkinter import messagebox
from configuracion import page, get_config_entrada, get_config_boton, get_db_connection, get_config_logo
from AdminPage import page_admin
from StudentPage import page_student 
from PIL import Image, ImageTk

class LoginPage(page):
    def __init__(self):
        super().__init__()
        self.root.title("Iniciar sesión")
        self.root.configure(bg=self.background[0])
        self.root.geometry(self.background[1])

        # Logo
        logo_cfg = get_config_logo()
        img = Image.open(logo_cfg[2])
        img = img.resize((200, 252), Image.Resampling.LANCZOS)
        self.logo_img = ImageTk.PhotoImage(img)
        self.logo_label = tk.Label(self.root, image=self.logo_img, bg=self.background[0])
        self.logo_label.pack(pady=(30, 10))

        entrada_cfg = get_config_entrada()
        boton_cfg = get_config_boton()

        # Usuario
        self.label_user = tk.Label(self.root, text="Usuario:", font=(entrada_cfg[3], entrada_cfg[1]), bg=self.background[0], fg=entrada_cfg[2])
        self.label_user.pack(pady=(10, 5))
        self.entry_user = tk.Entry(self.root, font=(entrada_cfg[3], 12))
        self.entry_user.pack(pady=5)

        # Contraseña
        self.label_pass = tk.Label(self.root, text="Contraseña:", font=(entrada_cfg[3], entrada_cfg[1]), bg=self.background[0], fg=entrada_cfg[2])
        self.label_pass.pack(pady=(20, 5))
        self.entry_pass = tk.Entry(self.root, show="*", font=(entrada_cfg[3], 12))
        self.entry_pass.pack(pady=5)

        # Botón de inicio de sesión
        self.btn_login = tk.Button(
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
        self.btn_login.pack(pady=30)

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
            if user:
                self.root.destroy()
                rol = user[2]
                codigo_alumno = user[3] if rol == 'alumno' else None
                if rol == 'administrador':
                    app = page_admin(nombre_usuario=username)
                    app.root.mainloop()
                else:
                    app = page_student(nombre_usuario=username, codigo_alumno=codigo_alumno)
                    app.root.mainloop()
            else:
                messagebox.showerror("Error de acceso", "Usuario o contraseña incorrectos.")
            cursor.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Error de conexión", f"No se pudo conectar a la base de datos.\n{e}")

if __name__ == "__main__":
    app = LoginPage()
    app.root.mainloop()
