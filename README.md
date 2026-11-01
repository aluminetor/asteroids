# Asteroids en Pygame: Arquitectura y Fundamentos

Este proyecto implementa una versión del clásico juego de arcade *Asteroids* utilizando Python y la biblioteca Pygame. El objetivo principal de este desarrollo es pedagógico, diseñado para ilustrar conceptos de programación orientada a objetos, matemáticas vectoriales bidimensionales y el ciclo de vida de un motor de videojuegos en 2D.

---

## El Bucle Principal del Juego (Game Loop)

El motor opera bajo un patrón de bucle continuo dividido en fases secuenciales que se ejecutan 60 veces por segundo:

1. **Gestión de eventos (Input):** Captura interacciones del sistema operativo y pulsaciones de teclas (salida de ventana, rotación, aceleración, disparo).
2. **Actualización lógica (Update):** Desplaza posiciones espaciales, procesa colisiones y actualiza los estados internos de cada entidad en función del tiempo transcurrido (`dt`).
3. **Renderizado (Draw):** Limpia la pantalla sobre un búfer oculto, dibuja las figuras geométricas en orden de capas y actualiza el búfer visible mediante `pygame.display.flip()`.
4. **Control de tiempo (Tick):** El reloj del sistema (`pygame.time.Clock`) pausa la ejecución para mantener una tasa constante de 60 cuadros por segundo y calcular el tiempo delta exacto.

---

## Conceptos Técnicos y Matemáticos Aplicados

### 1. Independencia de Cuadros por Segundo (Delta Time)

Para evitar que la velocidad de los objetos varíe según la potencia de la CPU, las traslaciones espaciales no se calculan por cuadro sino por segundo:

$$\text{posición}_{\text{nueva}} = \text{posición}_{\text{actual}} + (\text{velocidad} \times dt)$$

Donde $dt$ (delta time) representa la fracción de segundo transcurrida entre un cuadro y el siguiente ($dt \approx 0.0166\text{ s}$ a 60 FPS).

### 2. Rotación y Geometría Vectorial

* **Orientación:** La dirección de la nave y las trayectorias de las balas se manejan mediante instancias de `pygame.Vector2`. El método `.rotate()` aplica matrices de rotación trigonométricas internamente para modificar el ángulo del vector director.
* **Forma triangular:** La nave se renderiza calculando tres vértices en el espacio a partir de un vector frontal (`forward`) y uno lateral (`right`), manteniendo la coherencia visual durante cualquier rotación.

### 3. Detección de Colisiones Circular

Para optimizar el costo computacional, todas las entidades físicas derivan de una clase base `CircleShape`. Dos objetos colisionan si la distancia euclidiana entre sus centros es menor o igual a la suma de sus respectivos radios:

$$\text{distancia}(A, B) \le \text{radio}_A + \text{radio}_B$$

### 4. Patrón de Diseño con Grupos de Sprites (`pygame.sprite.Group`)

En lugar de actualizar y dibujar manualmente cada entidad en el archivo principal, se utiliza la propiedad de clase `containers`:

* **`updatable`:** Agrupa todas las entidades con lógica temporal que requieren llamadas a `.update(dt)`.
* **`drawable`:** Agrupa todos los elementos visibles que deben pasar por `.draw(screen)`.
* **`asteroids` y `shots`:** Subconjuntos especializados para resolver colisiones específicas sin iterar sobre entidades ajenas.

---

## Estructura del Proyecto

* **`main.py`:** Punto de entrada del programa. Inicializa Pygame, configura la resolución de pantalla, inicializa los grupos y ejecuta el bucle de juego.
* **`constants.py`:** Parámetros configurables globales (dimensiones de pantalla, radios, velocidades, tasas de generación).
* **`circleshape.py`:** Clase base que hereda de `pygame.sprite.Sprite`. Define la posición, velocidad, radio y la función genérica `collides_with`.
* **`player.py`:** Define la nave espacial, cálculo de vértices para renderizado, captura de entradas de teclado y lógica de disparo.
* **`asteroid.py`:** Entidad asteroide. Implementa el método `.split()` para dividirse en fragmentos menores tras recibir un disparo.
* **`asteroidfield.py`:** Sistema de generación procedural (`spawner`) que introduce asteroides en las coordenadas límite de la pantalla.
* **`shot.py`:** Balas disparadas por el jugador que viajan a alta velocidad lineal.
* **`logger.py`:** Módulo de instrumentación para registrar estados y eventos del juego en formato JSONL.

---

## Requisitos y Ejecución

### Requisitos del Sistema

* Python 3.10 o superior
* Gestor de paquetes `uv`
* Pygame 2.6.1

### Instalación de Dependencias

```bash
uv add pygame==2.6.1

```

### Ejecución en Entornos Locales

```bash
uv run main.py

```

### Ejecución en WSL2 (Windows Subsystem for Linux)

En entornos WSL sin servidor X nativo o WSLg, se puede ejecutar la simulación en modo headless para pruebas automatizadas:

```bash
SDL_VIDEODRIVER=dummy uv run main.py

```

O bien configurar un servidor gráfico X11 (como VcXsrv) exportando el display correspondiente:

```bash
export DISPLAY=$(ip route | grep default | awk '{print $3}'):0
export LIBGL_ALWAYS_INDIRECT=1
uv run main.py

```

---

## Controles del Juego

| Tecla | Acción |
| --- | --- |
| A / Flecha Izquierda | Rotar la nave en sentido antihorario |
| D / Flecha Derecha | Rotar la nave en sentido horario |
| W / Flecha Arriba | Acelerar hacia adelante |
| S / Flecha Abajo | Acelerar hacia atrás |
| Barra Espaciadora | Disparar |
| Cerrar Ventana | Salir del juego |