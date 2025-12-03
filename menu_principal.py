import tkinter as tk
from tkinter import ttk, messagebox
import threading
import subprocess
import os

# --- Importación de las Clases de las Aplicaciones ---
# Usamos imports locales, asumimos que están en el mismo directorio.
try:
    from simulaciones_app import SimulacionesApp
    from distribuciones_app import DistribucionesApp
except ImportError as e:
    # Esto ayuda si el usuario ejecuta el menú en un entorno donde no puede usar threading/subprocess fácilmente
    print(f"Error al importar módulos de aplicación: {e}")
    # Definir funciones placeholder si la importación falla
    def run_simulaciones():
        messagebox.showerror("Error", "No se pudo iniciar la aplicación de Simulaciones. Asegúrate de que 'simulaciones_app.py' esté en el mismo directorio.")
    def run_distribuciones():
        messagebox.showerror("Error", "No se pudo iniciar la aplicación de Distribuciones. Asegúrate de que 'distribuciones_app.py' esté en el mismo directorio.")


class MenuPrincipalApp:
    def __init__(self, root):
        self.root = root
        root.title('Menú Principal de Simulaciones y Análisis')
        root.geometry('500x350')
        root.configure(bg='#FCE4EC') # Pink Pastel
        
        self.style = ttk.Style()
        self._setup_styles()

        # Contenedor principal centrado
        main_frame = ttk.Frame(root, padding="30", style='Pink.TFrame')
        main_frame.pack(expand=True, padx=20, pady=20)

        # Título
        ttk.Label(main_frame, text='SELECCIONA UNA APLICACIÓN', style='Pink.Title.TLabel').pack(pady=(0, 30))

        # Botones de las aplicaciones
        ttk.Button(main_frame, text='1. Simulaciones (GOL + COVID)', 
                   command=self._open_simulaciones, 
                   style='Menu.Pink.TButton').pack(fill='x', pady=10)

        ttk.Button(main_frame, text='2. Generador de Distribuciones', 
                   command=self._open_distribuciones, 
                   style='Menu.Pink.TButton').pack(fill='x', pady=10)

        ttk.Button(main_frame, text='Salir', 
                   command=root.quit, 
                   style='Menu.Exit.TButton').pack(fill='x', pady=20)

    def _setup_styles(self):
        pink_bg_light = '#FCE4EC'    # Pink Pastel
        pink_button_color = '#C71585' # DeepPink
        purple_fg = '#800080'        # Purple

        # Estilo general del Frame y Labels
        self.style.configure('Pink.TFrame', background=pink_bg_light)
        self.style.configure('Pink.Title.TLabel', 
                             background=pink_bg_light, 
                             foreground=purple_fg, 
                             font=('Helvetica', 14, 'bold'))

        # Estilo para los botones del Menú (DeepPink)
        self.style.configure('Menu.Pink.TButton', 
                             background=pink_button_color, 
                             foreground='blue', 
                             font=('Helvetica', 11, 'bold'),
                             padding=12)
        self.style.map('Menu.Pink.TButton', 
                       background=[('active', '#FF69B4')], 
                       foreground=[('active', 'purple')])

        # Estilo para el botón de Salir (ligeramente diferente para destacarlo)
        self.style.configure('Menu.Exit.TButton', 
                             background=purple_fg, 
                             foreground='purple', 
                             font=('Helvetica', 11, 'bold'),
                             padding=12)
        self.style.map('Menu.Exit.TButton', 
                       background=[('active', '#5D3FD3')], 
                       foreground=[('active', 'purple')])

    def _open_app_in_new_window(self, AppClass):
        # Oculta la ventana principal mientras se abre la nueva
        self.root.withdraw()
        
        # Crea una nueva ventana (Toplevel) para la aplicación
        new_window = tk.Toplevel(self.root)
        AppClass(new_window)
        
        # Configura qué hacer cuando se cierra la nueva ventana
        def on_close():
            new_window.destroy()
            self.root.deiconify() # Muestra la ventana principal de nuevo

        new_window.protocol("WM_DELETE_WINDOW", on_close)


    def _open_simulaciones(self):
        # Abre la aplicación de Simulaciones en una nueva ventana (Toplevel)
        self._open_app_in_new_window(SimulacionesApp)
    
    def _open_distribuciones(self):
        # Abre la aplicación de Distribuciones en una nueva ventana (Toplevel)
        self._open_app_in_new_window(DistribucionesApp)


def main():
    root = tk.Tk()
    app = MenuPrincipalApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()