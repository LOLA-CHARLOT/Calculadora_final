# Simulaciones y Análisis de Sistemas Dinámicos

Este proyecto es una suite integral de herramientas desarrolladas en Python con `tkinter` y `Matplotlib` para la simulación de fenómenos dinámicos y la generación/análisis de números pseudoaleatorios y distribuciones de probabilidad. La interfaz utiliza un diseño personalizado con tonos rosados y morados.

# Descripción General

Este proyecto integra dos aplicaciones principales:

# 1. Calculadora de Generadores, Pruebas y Distribuciones

Permite:

- Generar números pseudoaleatorios mediante algoritmos clásicos

- Evaluar aleatoriedad con pruebas estadísticas

- Generar variables aleatorias mediante diversas distribuciones

<img width="556" height="376" alt="image" src="https://github.com/user-attachments/assets/d6832038-00de-4758-9228-99a567f52a6b" />


# Ideal para cursos de Simulación, Probabilidad y Estadística.

# 2. Calculadora de Simulaciones (Juego de la Vida + COVID)
<img width="298" height="161" alt="image" src="https://github.com/user-attachments/assets/edd3632d-b032-4307-ad7c-d5af67508be1" />

Incluye tres modelos interactivos:

- Juego de la Vida 2D

<img width="861" height="401" alt="image" src="https://github.com/user-attachments/assets/acd0724e-0543-4b59-a333-cac436d09e25" />


- Autómata Celular 1D
<img width="870" height="408" alt="image" src="https://github.com/user-attachments/assets/d1777030-d219-4493-ad17-baddb7ad0a63" />


- Simulación tipo SIR (COVID) en una grilla
<img width="930" height="673" alt="image" src="https://github.com/user-attachments/assets/27787989-8e2c-46b0-ad2b-2f0a5beb1d7d" />


Perfecto para explorar autómatas celulares y modelos epidemiológicos.


# Tecnologías Usadas

- Python 3.x

- Tkinter (interfaz gráfica)

- Matplotlib (visualización)

- NumPy (cálculos numéricos)

- Threading (simulaciones en tiempo real)

<img width="387" height="231" alt="image" src="https://github.com/user-attachments/assets/393bee9f-279b-488e-a74c-74739bbc9452" />


# 1. Calculadora de Generadores, Pruebas y Distribuciones
🔹 Generadores Pseudoaleatorios

Algoritmos implementados:

- Cuadrados Medios

- Productos Medios

- Multiplicador Constante

Cada método permite:

- Definir semillas

- Elegir número de dígitos n

- Generar N valores Ri

🔹 Pruebas de Aleatoriedad

- Pruebas estadísticas disponibles:

- Prueba de Medias

- Prueba de Varianza

- Chi-Cuadrado

Incluye botón para importar automáticamente la última secuencia generada.

🔹 Distribuciones

Genera variables aleatorias para:

- Uniforme

<img width="858" height="336" alt="image" src="https://github.com/user-attachments/assets/c34d3008-6c61-4d54-9cb3-35200fa7f721" />

- Exponencial

<img width="846" height="318" alt="image" src="https://github.com/user-attachments/assets/9e4c89b8-80a3-43e0-8a58-15984118718f" />

- Erlang

<img width="851" height="323" alt="image" src="https://github.com/user-attachments/assets/7e0fddff-4bcc-4296-8425-cb7c3264e272" />

- Gamma

<img width="843" height="322" alt="image" src="https://github.com/user-attachments/assets/7f71d7e5-05c2-44a9-863e-48c557d1c6cf" />

- Normal

<img width="855" height="323" alt="image" src="https://github.com/user-attachments/assets/f1c047de-43b7-443d-8195-cb1ea851477a" />

- Weibull

<img width="854" height="321" alt="image" src="https://github.com/user-attachments/assets/aa197dd8-bc1d-47cf-96a1-54828705f69c" />

- Bernoulli

<img width="844" height="323" alt="image" src="https://github.com/user-attachments/assets/9b8d3dc1-e9c0-4bfb-9e4d-62e08f3df6a1" />

- Binomial

<img width="849" height="322" alt="image" src="https://github.com/user-attachments/assets/fea8a839-b628-4525-b33b-cdb2c7f0e3b3" />

- Poisson

<img width="854" height="318" alt="image" src="https://github.com/user-attachments/assets/e8c09c5b-5643-44f1-b027-4d923c970f52" />

Cada distribución se grafica automáticamente con histograma.

# 2. Aplicación de Simulaciones
🔹 Juego de la Vida 2D

Permite:

- Configurar filas, columnas y probabilidad inicial
- Generar patrón aleatorio
- Ejecutar paso a paso o en bucle
- Limpiar la grilla

🔹 Autómata Celular 1D

Incluye:

- Longitud de la línea
- Regla de Wolfram (0–255)
- Evolución manual o automática (200 pasos)
- Visualización completa de la historia

🔹 Simulación COVID (Modelo SIR Simplificado)

Control de parámetros:

- Filas y columnas
- Infectados iniciales
- Probabilidad de infección
- Probabilidad de recuperación
- Probabilidad de muerte

Se muestran:

- La grilla en tiempo real

- Gráfica de S, I, R, D

# ¿Cómo ejecutar?

Instala dependencias:

pip install numpy matplotlib


Para ejecutar la app de simulaciones:

python simulaciones_app.py


Para la calculadora de distribuciones:

python distribuciones_app.py

# Créditos

Proyecto desarrollado para fines educativos, demostrativos y de práctica en simulación.

