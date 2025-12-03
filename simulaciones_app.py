import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.colors import ListedColormap
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from game_of_life_2d import GameOfLife2D
from game_of_life_1d import GameOfLife1D
from covid_simulation import CovidSimulation

class SimulacionesApp:
    def __init__(self, root):
        self.root = root
        root.title('✨ Simulaciones Dinámicas (JdV & COVID) ✨')
        root.geometry('1150x750')
        self.style = ttk.Style()
        self._setup_styles()
        root.configure(bg='#F0F0F0')

        self.nb = ttk.Notebook(root, style='Pink.TNotebook')
        self.nb.pack(fill='both', expand=True, padx=10, pady=10)

        self._build_gameoflife_tab()
        self._build_gameoflife1d_tab()
        self._build_covid_tab()

    def _setup_styles(self):
        # Colores personalizados
        pink_bg_light = "#EEC6D3"   # Pink Pastel (Fondo general)
        pink_button_color = '#C71585' # DeepPink (Fondo de botones y pestañas)
        purple_fg = '#800080'       # Purple (Texto oscuro para Labels)
        
        # Estilo de TFrame para el fondo general de las pestañas
        self.style.configure('Pink.TFrame', background=pink_bg_light)
        
        # Estilo de TNotebook para el color de las pestañas
        self.style.configure('Pink.TNotebook', background=pink_bg_light, tabposition='wn')
        
        # CORRECCIÓN CLAVE: Pestañas Inactivas con alto contraste (Fondo DeepPink, Texto púrpura)
        self.style.configure('Pink.TNotebook.Tab', 
                             background=pink_button_color, # Fondo DeepPink
                             foreground='purple',           # Texto PÚRPURA
                             font=('Helvetica', 10, 'bold'),
                             padding=[10, 5])
        
        # Pestaña Activa (Se mantiene igual: DeepPink y Texto púrpura)
        self.style.map('Pink.TNotebook.Tab', 
                       background=[('selected', pink_button_color)], 
                       foreground=[('selected', 'purple')])

        # Estilo de Labels (Etiquetas)
        self.style.configure('Pink.TLabel', background=pink_bg_light, foreground=purple_fg, font=('Helvetica', 10))
        
        # Estilo de Entries (Entradas de texto)
        self.style.configure('Pink.TEntry', 
                             fieldbackground='blue', 
                             foreground='#000000') # Texto de entrada: NEGRO
        
        # Estilo de Botones
        self.style.configure('Pink.TButton', 
                             background=pink_button_color, 
                             foreground='blue', # Texto de botón: BLANCO
                             font=('Helvetica', 10, 'bold'),
                             padding=8)
        self.style.map('Pink.TButton', 
                       background=[('active', '#FF69B4')], 
                       foreground=[('active', 'white')])
    
    # ---------------- Game of Life 2D ----------------
    def _build_gameoflife_tab(self):
        tab = ttk.Frame(self.nb, style='Pink.TFrame')
        self.nb.add(tab, text='Juego de la Vida 2D 💖')

        left = ttk.Frame(tab, padding="15", style='Pink.TFrame')
        left.pack(side='left', fill='y', padx=10, pady=10)
        right = ttk.Frame(tab, style='Pink.TFrame')
        right.pack(side='right', fill='both', expand=True, padx=10, pady=10)

        # Etiquetas y Entradas
        ttk.Label(left, text='Filas:', style='Pink.TLabel').pack(anchor='w')
        self.g2_rows = tk.IntVar(value=50)
        ttk.Entry(left, textvariable=self.g2_rows, style='Pink.TEntry').pack(fill='x')
        ttk.Label(left, text='Columnas:', style='Pink.TLabel').pack(anchor='w', pady=(10, 0))
        self.g2_cols = tk.IntVar(value=50)
        ttk.Entry(left, textvariable=self.g2_cols, style='Pink.TEntry').pack(fill='x')
        ttk.Label(left, text='Prob. vivo inicial:', style='Pink.TLabel').pack(anchor='w', pady=(10, 0))
        self.g2_p = tk.DoubleVar(value=0.2)
        ttk.Entry(left, textvariable=self.g2_p, style='Pink.TEntry').pack(fill='x')
        
        ttk.Separator(left).pack(fill='x', pady=15)

        # Botones
        ttk.Button(left, text='Crear Aleatorio', command=self._g2_create_random, style='Pink.TButton').pack(fill='x', pady=5)
        ttk.Button(left, text='Siguiente Paso', command=self._g2_step, style='Pink.TButton').pack(fill='x')
        ttk.Button(left, text='Ejecutar/Parar', command=self._g2_toggle_run, style='Pink.TButton').pack(fill='x', pady=5)
        ttk.Button(left, text='Limpiar', command=self._g2_clear, style='Pink.TButton').pack(fill='x')

        fig = Figure(figsize=(6,6), dpi=100)
        self.g2_ax = fig.add_subplot(111)
        fig.patch.set_facecolor('#F0F0F0')
        self.g2_canvas = FigureCanvasTkAgg(fig, master=right)
        self.g2_canvas.get_tk_widget().pack(fill='both', expand=True)

        self.g2 = None
        self.g2_running = False

    def _g2_draw(self):
        self.g2_ax.clear()
        cmap = ListedColormap(['#FCE4EC', '#C71585'])
        self.g2_ax.imshow(self.g2.grid, interpolation='nearest', cmap=cmap)
        self.g2_ax.set_title('Juego de la Vida 2D', color='#800080', fontsize=14)
        self.g2_canvas.draw()
        
    def _g2_create_random(self):
        rows = max(5, int(self.g2_rows.get()))
        cols = max(5, int(self.g2_cols.get()))
        p = float(self.g2_p.get())
        self.g2 = GameOfLife2D(rows=rows, cols=cols)
        self.g2.randomize(p=p)
        self._g2_draw()

    def _g2_step(self):
        if self.g2 is None:
            self._g2_create_random()
        self.g2.step()
        self._g2_draw()

    def _g2_toggle_run(self):
        self.g2_running = not self.g2_running
        if self.g2_running:
            self._g2_run_loop()

    def _g2_run_loop(self):
        def loop():
            while self.g2_running:
                time.sleep(0.1)
                try:
                    self._g2_step()
                except Exception as e:
                    print('Error en loop GOL2D:', e)
                    self.g2_running = False
        threading.Thread(target=loop, daemon=True).start()

    def _g2_clear(self):
        if self.g2 is None:
            self._g2_create_random()
        self.g2.grid = np.zeros_like(self.g2.grid)
        self._g2_draw()
    
    # ---------------- Game of Life 1D ----------------
    def _build_gameoflife1d_tab(self):
        tab = ttk.Frame(self.nb, style='Pink.TFrame')
        self.nb.add(tab, text='Autómata Celular 1D 💜')

        left = ttk.Frame(tab, padding="15", style='Pink.TFrame')
        left.pack(side='left', fill='y', padx=10, pady=10)
        right = ttk.Frame(tab, style='Pink.TFrame')
        right.pack(side='right', fill='both', expand=True, padx=10, pady=10)

        ttk.Label(left, text='Longitud de la rejilla:', style='Pink.TLabel').pack(anchor='w')
        self.g1_length = tk.IntVar(value=300)
        ttk.Entry(left, textvariable=self.g1_length, style='Pink.TEntry').pack(fill='x')
        ttk.Label(left, text='Regla (0-255):', style='Pink.TLabel').pack(anchor='w', pady=(10, 0))
        self.g1_rule = tk.IntVar(value=30)
        ttk.Entry(left, textvariable=self.g1_rule, style='Pink.TEntry').pack(fill='x')
        
        ttk.Separator(left).pack(fill='x', pady=15)
        
        ttk.Button(left, text='Crear', command=self._g1_create, style='Pink.TButton').pack(fill='x', pady=5)
        ttk.Button(left, text='Siguiente Paso', command=self._g1_step, style='Pink.TButton').pack(fill='x')
        ttk.Button(left, text='Ejecutar (200 Pasos)', command=self._g1_run, style='Pink.TButton').pack(fill='x', pady=5)
        ttk.Button(left, text='Ejecutar/Parar', command=self._g1_run, style='Pink.TButton').pack(fill='x', pady=5)

        fig = Figure(figsize=(8,5), dpi=100)
        self.g1_ax = fig.add_subplot(111)
        fig.patch.set_facecolor('#F0F0F0')
        self.g1_canvas = FigureCanvasTkAgg(fig, master=right)
        self.g1_canvas.get_tk_widget().pack(fill='both', expand=True)

        self.g1 = None
        self.g1_history = []

    def _g1_draw(self):
        self.g1_ax.clear()
        img = np.array(self.g1_history)
        cmap = ListedColormap(['#F0F0F0', '#800080'])
        self.g1_ax.imshow(img, aspect='auto', interpolation='nearest', cmap=cmap)
        self.g1_ax.set_title(f'Autómata 1D (Regla {self.g1.rule})', color='#800080', fontsize=14)
        self.g1_ax.set_ylabel('Tiempo (Pasos)')
        self.g1_ax.set_xlabel('Posición')
        self.g1_canvas.draw()
        
    def _g1_create(self):
        length = max(10, int(self.g1_length.get()))
        rule = min(255, max(0, int(self.g1_rule.get())))
        self.g1 = GameOfLife1D(length=length, rule=rule)
        self.g1.reset()
        self.g1_history = [self.g1.state.copy()]
        self._g1_draw()

    def _g1_step(self):
        if self.g1 is None:
            self._g1_create()
        self.g1.step()
        self.g1_history.append(self.g1.state.copy())
        if len(self.g1_history) > 200:
            self.g1_history.pop(0)
        self._g1_draw()

    def _g1_run(self):
        def run_loop():
            if self.g1 is None: self._g1_create()
            for _ in range(200):
                time.sleep(0.05)
                self._g1_step()
        threading.Thread(target=run_loop, daemon=True).start()

    # ---------------- COVID Tab ----------------
    def _build_covid_tab(self):
        tab = ttk.Frame(self.nb, style='Pink.TFrame')
        self.nb.add(tab, text='Simulación COVID 🦠')

        left = ttk.Frame(tab, padding="15", style='Pink.TFrame')
        left.pack(side='left', fill='y', padx=10, pady=10)
        right = ttk.Frame(tab, style='Pink.TFrame')
        right.pack(side='right', fill='both', expand=True, padx=10, pady=10)

        # Controles
        ttk.Label(left, text='Filas:', style='Pink.TLabel').pack(anchor='w')
        self.cv_rows = tk.IntVar(value=60)
        ttk.Entry(left, textvariable=self.cv_rows, style='Pink.TEntry').pack(fill='x')
        ttk.Label(left, text='Columnas:', style='Pink.TLabel').pack(anchor='w', pady=(10, 0))
        self.cv_cols = tk.IntVar(value=60)
        ttk.Entry(left, textvariable=self.cv_cols, style='Pink.TEntry').pack(fill='x')
        ttk.Label(left, text='Inicial infectados:', style='Pink.TLabel').pack(anchor='w', pady=(10, 0))
        self.cv_init = tk.IntVar(value=5)
        ttk.Entry(left, textvariable=self.cv_init, style='Pink.TEntry').pack(fill='x')

        ttk.Separator(left).pack(fill='x', pady=15)
        
        ttk.Label(left, text='P(infect) por vecino:', style='Pink.TLabel').pack(anchor='w')
        self.cv_pinf = tk.DoubleVar(value=0.25)
        ttk.Entry(left, textvariable=self.cv_pinf, style='Pink.TEntry').pack(fill='x')
        ttk.Label(left, text='P(recover) por paso:', style='Pink.TLabel').pack(anchor='w', pady=(10, 0))
        self.cv_prec = tk.DoubleVar(value=0.02)
        ttk.Entry(left, textvariable=self.cv_prec, style='Pink.TEntry').pack(fill='x')
        ttk.Label(left, text='P(die) por paso:', style='Pink.TLabel').pack(anchor='w', pady=(10, 0))
        self.cv_pdie = tk.DoubleVar(value=0.005)
        ttk.Entry(left, textvariable=self.cv_pdie, style='Pink.TEntry').pack(fill='x')

        ttk.Separator(left).pack(fill='x', pady=15)

        ttk.Button(left, text='Crear Simulación', command=self._cv_create, style='Pink.TButton').pack(fill='x', pady=5)
        ttk.Button(left, text='Siguiente Paso', command=self._cv_step, style='Pink.TButton').pack(fill='x')
        ttk.Button(left, text='Ejecutar/Parar', command=self._cv_toggle_run, style='Pink.TButton').pack(fill='x', pady=5)

        # Gráficos
        fig = Figure(figsize=(7,6), dpi=100)
        self.cv_ax_grid = fig.add_subplot(211)
        self.cv_ax_chart = fig.add_subplot(212)
        fig.tight_layout(pad=3.0)
        fig.patch.set_facecolor('#F0F0F0')
        self.cv_canvas = FigureCanvasTkAgg(fig, master=right)
        self.cv_canvas.get_tk_widget().pack(fill='both', expand=True)

        self.cv = None
        self.cv_running = False
        self.cv_history = []

    def _cv_draw(self):
        self.cv_ax_grid.clear()
        cmap = ListedColormap(['#FCE4EC', '#FF69B4', '#C71585', '#800080', '#000000']) 
        self.cv_ax_grid.imshow(self.cv.grid, interpolation='nearest', cmap=cmap, vmin=0, vmax=4)
        self.cv_ax_grid.set_title(f'Simulación COVID t={self.cv.t}', color='#800080', fontsize=14)

        self.cv_ax_chart.clear()
        times = list(range(len(self.cv_history)))
        s = [h[1] for h in self.cv_history]
        i = [h[2] for h in self.cv_history]
        r = [h[3] for h in self.cv_history]
        d = [h[4] for h in self.cv_history]
        
        self.cv_ax_chart.plot(times, s, label='Susceptibles', color='#FF69B4') 
        self.cv_ax_chart.plot(times, i, label='Infectados', color='#C71585') 
        self.cv_ax_chart.plot(times, r, label='Recuperados', color='#800080') 
        self.cv_ax_chart.plot(times, d, label='Muertos', color='#000000')
        
        self.cv_ax_chart.set_xlabel('Tiempo')
        self.cv_ax_chart.set_ylabel('Población')
        self.cv_ax_chart.legend()
        self.cv_canvas.draw()

    def _cv_create(self):
        rows = max(5, int(self.cv_rows.get()))
        cols = max(5, int(self.cv_cols.get()))
        init = max(1, int(self.cv_init.get()))
        pinf = float(self.cv_pinf.get())
        prec = float(self.cv_prec.get())
        pdie = float(self.cv_pdie.get())
        self.cv = CovidSimulation(rows=rows, cols=cols, init_infected=init, p_infect=pinf, p_recover=prec, p_die=pdie)
        self.cv_history = [self.cv.counts()]
        self._cv_draw()

    def _cv_step(self):
        if self.cv is None:
            self._cv_create()
        self.cv.step()
        self.cv_history.append(self.cv.counts())
        self._cv_draw()

    def _cv_toggle_run(self):
        self.cv_running = not self.cv_running
        if self.cv_running:
            self._cv_run_loop()

    def _cv_run_loop(self):
        def loop():
            while self.cv_running:
                time.sleep(0.1)
                try:
                    self._cv_step()
                except Exception as e:
                    print('Error en loop COVID:', e)
                    self.cv_running = False
        threading.Thread(target=loop, daemon=True).start()


def main():
    root = tk.Tk()
    app = SimulacionesApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()