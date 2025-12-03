import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from random_generators import RandomGenerators

def plot_histogram(data, ax, bins=50, title='', xlabel='x', color='#C71585'): # DeepPink
    ax.clear()
    ax.hist(data, bins=bins, density=True, alpha=0.7, color=color)
    ax.set_title(title, color='#800080', fontsize=14) # Purple
    ax.set_xlabel(xlabel)
    ax.set_ylabel('Densidad')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.grid(axis='y', linestyle='--', alpha=0.5)

class DistribucionesApp:
    def __init__(self, root):
        self.root = root
        root.title('🌸 Generador de Distribuciones Aleatorias 🌸')
        root.geometry('1000x650')
        self.style = ttk.Style()
        self._setup_styles()
        root.configure(bg='#F0F0F0')

        # Contenedores principales
        left_frame = ttk.Frame(root, padding="15 15 15 15", style='Pink.TFrame')
        left_frame.pack(side='left', fill='y', padx=10, pady=10)
        right_frame = ttk.Frame(root, style='Pink.TFrame')
        right_frame.pack(side='right', fill='both', expand=True, padx=10, pady=10)

        # Configuración de Controles (Izquierda)
        self._build_controls(left_frame)

        # Configuración de Gráfico (Derecha)
        self._build_plot(right_frame)

        # Llama a la generación inicial
        self._generate_and_plot()


    def _setup_styles(self):
        # Colores personalizados (Rosa, Morado, Blanco/Gris claro)
        pink_bg = '#FCE4EC'    # Pink Pastel
        pink_fg = '#C71585'    # DeepPink (Oscuro)
        purple_fg = '#800080'  # Purple
        
        self.style.configure('Pink.TFrame', background=pink_bg)
        self.style.configure('Pink.TLabel', background=pink_bg, foreground=purple_fg, font=('Helvetica', 10, 'bold'))
        self.style.configure('Pink.TCombobox', fieldbackground='white', foreground=pink_fg)
        self.style.configure('Pink.TEntry', fieldbackground='white', foreground=pink_fg)
        
        # Estilo del botón
        self.style.configure('Pink.TButton', 
                             background=pink_fg, 
                             foreground='blue', 
                             font=('Helvetica', 10, 'bold'),
                             padding=8)
        self.style.map('Pink.TButton', 
                       background=[('active', '#FF69B4')], # HotPink al pasar el ratón
                       foreground=[('active', 'purple')])


    def _build_controls(self, frame):
        # Distribución
        ttk.Label(frame, text='Selecciona la Distribución:', style='Pink.TLabel').pack(anchor='w', pady=(5, 0))
        self.dist_var = tk.StringVar(value='normal')
        dists = ['uniform','exponential','erlang','gamma','normal','weibull','bernoulli','binomial','poisson']
        self.dist_combo = ttk.Combobox(frame, values=dists, textvariable=self.dist_var, state='readonly', style='Pink.TCombobox', font=('Helvetica', 10))
        self.dist_combo.pack(fill='x', pady=5)
        self.dist_combo.bind("<<ComboboxSelected>>", lambda e: self._set_default_params())

        # Tamaño
        ttk.Label(frame, text='Tamaño de la Muestra (n):', style='Pink.TLabel').pack(anchor='w', pady=(10, 0))
        self.dist_size = tk.IntVar(value=1000)
        ttk.Entry(frame, textvariable=self.dist_size, style='Pink.TEntry', font=('Helvetica', 10)).pack(fill='x', pady=5)

        # Parámetros
        ttk.Label(frame, text='Parámetros (ej: mu=0,sigma=1):', style='Pink.TLabel').pack(anchor='w', pady=(10, 0))
        self.params_entry = ttk.Entry(frame, style='Pink.TEntry', font=('Helvetica', 10))
        self.params_entry.insert(0, 'mu=0,sigma=1')
        self.params_entry.pack(fill='x', pady=5)
        
        # Botón
        ttk.Separator(frame).pack(fill='x', pady=15)
        ttk.Button(frame, text='Generar y Graficar ✨', command=self._generate_and_plot, style='Pink.TButton').pack(fill='x', pady=5)

    def _build_plot(self, frame):
        fig = Figure(figsize=(7,5), dpi=100)
        self.ax = fig.add_subplot(111)
        fig.patch.set_facecolor('#F0F0F0') # Fondo del gráfico
        self.canvas = FigureCanvasTkAgg(fig, master=frame)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)

    def _set_default_params(self):
        dist = self.dist_var.get()
        defaults = {
            'uniform': 'a=0.0,b=1.0',
            'exponential': 'lam=1.0',
            'erlang': 'k=2,lam=1.0',
            'gamma': 'shape=2.0,scale=1.0',
            'normal': 'mu=0,sigma=1',
            'weibull': 'k=1.5,lam=1.0',
            'bernoulli': 'p=0.5',
            'binomial': 'n=10,p=0.5',
            'poisson': 'lam=1.0'
        }
        self.params_entry.delete(0, tk.END)
        self.params_entry.insert(0, defaults.get(dist, ''))

    def _parse_params(self, text):
        # ... (Lógica de análisis de parámetros, idéntica a la original) ...
        d = {}
        if not text:
            return d
        parts = [p.strip() for p in text.split(',') if p.strip()]
        for p in parts:
            if '=' in p:
                k, v = p.split('=',1)
                try:
                    d[k.strip()] = float(v)
                except:
                    try:
                        d[k.strip()] = int(v)
                    except:
                        d[k.strip()] = v
        return d

    def _generate_and_plot(self):
        dist = self.dist_var.get()
        try:
            n = max(1, int(self.dist_size.get()))
            params = self._parse_params(self.params_entry.get())
            data = []
            title = 'Distribución'

            if dist == 'uniform':
                a = params.get('a', 0.0)
                b = params.get('b', 1.0)
                data = RandomGenerators.uniform(a=a,b=b,size=n)
                title = f'Uniforme U({a:.2f},{b:.2f})'
                plot_histogram(data, self.ax, bins=50, title=title)
            elif dist == 'exponential':
                lam = params.get('lam', params.get('lambda',1.0))
                data = RandomGenerators.exponential(lam=lam,size=n)
                title = f'Exponencial (λ={lam:.2f})'
                plot_histogram(data, self.ax, bins=50, title=title)
            elif dist == 'erlang':
                k = int(params.get('k',2))
                lam = params.get('lam',1.0)
                data = RandomGenerators.erlang(k=k,lam=lam,size=n)
                title = f'Erlang k={k}, λ={lam:.2f}'
                plot_histogram(data, self.ax, bins=50, title=title)
            elif dist == 'gamma':
                shape = params.get('shape',2.0)
                scale = params.get('scale',1.0)
                data = RandomGenerators.gamma(shape=shape, scale=scale, size=n)
                title = f'Gamma(shape={shape:.2f}, scale={scale:.2f})'
                plot_histogram(data, self.ax, bins=50, title=title)
            elif dist == 'normal':
                mu = params.get('mu',0.0)
                sigma = params.get('sigma',1.0)
                data = RandomGenerators.normal(mu=mu,sigma=sigma,size=n)
                title = f'Normal N({mu:.2f},{sigma**2:.2f})'
                plot_histogram(data, self.ax, bins=50, title=title)
            elif dist == 'weibull':
                k = params.get('k',1.5)
                lam = params.get('lam',1.0)
                data = RandomGenerators.weibull(k=k,lam=lam,size=n)
                title = f'Weibull k={k:.2f}, λ={lam:.2f}'
                plot_histogram(data, self.ax, bins=50, title=title)
            elif dist == 'bernoulli':
                p = params.get('p',0.5)
                data = RandomGenerators.bernoulli(p=p,size=n)
                title = f'Bernoulli p={p:.2f}'
                plot_histogram(data, self.ax, bins=2, title=title)
            elif dist == 'binomial':
                nn = int(params.get('n',10))
                p = params.get('p',0.5)
                data = RandomGenerators.binomial(n=nn,p=p,size=n)
                title = f'Binomial n={nn}, p={p:.2f}'
                plot_histogram(data, self.ax, bins=range(0,nn+2), title=title)
            elif dist == 'poisson':
                lam = params.get('lam',1.0)
                data = RandomGenerators.poisson(lam=lam,size=n)
                title = f'Poisson λ={lam:.2f}'
                plot_histogram(data, self.ax, bins=range(0,int(max(data))+2), title=title)
            else:
                raise ValueError('Distribución no soportada')

            self.canvas.draw()
        except Exception as e:
            messagebox.showerror('Error de Distribución', f'Verifica los parámetros o el tamaño. Error: {e}')

def main():
    root = tk.Tk()
    app = DistribucionesApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()