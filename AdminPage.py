import tkinter as tk
from tkinter import messagebox
import mysql.connector
from config import page

# Conexión a la base de datos
def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",  # Ajusta tu contraseña si es necesario
        database="db_vt0"
    )

class page_admin(page):

    def __init__(self):
        super().__init__() #Lammamos a la configuración de la página
        '''
        atrivutos heredados:
        self.background = tuple("color de fondo", "dimensiones de la ventana")
        self.tittle = tuple("Texto del titulo", "tamaño de fuente", "color de fondo", "color del texto", "la tipografia")
        self.logo = tuple("texto del logo", "tamaño de fuente", "color de fondo", "nombre del archivo con la imagen en png")
        '''
