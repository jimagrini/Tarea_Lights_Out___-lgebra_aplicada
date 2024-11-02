import pygame
import numpy as np

# Configuración de Pygame
pygame.init()
WIDTH, HEIGHT = 300, 300
ROWS, COLS = 6, 6
CELL_SIZE = WIDTH // COLS

# Colores
WHITE = (255, 255, 255)
RED = (255, 0, 0)  # Luz apagada en rojo
BLUE = (0, 0, 255)  # Luz encendida en azul

# Inicializar ventana
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lights Out")

# Generar tablero inicial aleatorio (1 para encendido, 0 para apagado)
board = np.random.randint(2, size=(ROWS, COLS))

def draw_board():
    #Dibuja el tablero de luces.
    for row in range(ROWS):
        for col in range(COLS):
            color = BLUE if board[row, col] == 1 else RED
            pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, WHITE, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

def toggle_light(row, col):
    """Cambia el estado de la luz en (row, col) y sus vecinos adyacentes."""
    if 0 <= row < ROWS and 0 <= col < COLS:
        board[row, col] = 1 - board[row, col]  # Cambia el estado de la luz misma
    # Cambia el estado de las luces adyacentes
    if row > 0: board[row - 1, col] = 1 - board[row - 1, col]  # Arriba
    if row < ROWS - 1: board[row + 1, col] = 1 - board[row + 1, col]  # Abajo
    if col > 0: board[row, col - 1] = 1 - board[row, col - 1]  # Izquierda
    if col < COLS - 1: board[row, col + 1] = 1 - board[row, col + 1]  # Derecha

def check_win():
    """Verifica si todas las luces están apagadas."""
    return np.all(board == 0)

def create_system():
    """Crea el sistema de ecuaciones en binario para Lights Out en una matriz aumentada."""
    n = ROWS * COLS
    A = np.zeros((n, n), dtype=int)
    b = board.flatten()

    for i in range(n):
        A[i, i] = 1  # La luz misma
        row, col = divmod(i, COLS)
        # Luz arriba
        if row > 0:
            A[i, i - COLS] = 1
        # Luz abajo
        if row < ROWS - 1:
            A[i, i + COLS] = 1
        # Luz izquierda
        if col > 0:
            A[i, i - 1] = 1
        # Luz derecha
        if col < COLS - 1:
            A[i, i + 1] = 1

    return A, b

def elminacion_gaussiana(A, b):
    """Aplica eliminación gaussiana en binario para resolver el sistema."""
    n = len(b)

    # Eliminar hacia adelante
    for i in range(n):
        if A[i, i] == 0:
            for j in range(i + 1, n):
                if A[j, i] == 1:
                    A[[i, j]] = A[[j, i]]
                    b[i], b[j] = b[j], b[i]
                    break
        for j in range(i + 1, n):
            if A[j, i] == 1:
                A[j] = (A[j] + A[i]) % 2
                b[j] = (b[j] + b[i]) % 2

    # Sustitución hacia atrás
    x = np.zeros(n, dtype=int)
    for i in range(n - 1, -1, -1):
        x[i] = b[i]
        for j in range(i + 1, n):
            x[i] = (x[i] - A[i, j] * x[j]) % 2
        if A[i, i] != 0:  # Evitar división por 0 en binario
            x[i] = x[i] // A[i, i]

    return x

def solve_lights_out():
    #Resuelve el juego Lights Out utilizando eliminación gaussiana en binario y muestra la matriz solución.
    A, b = create_system()
    solucion = elminacion_gaussiana(A, b)
    
    # Convertimos la solución en una matriz para visualización
    matriz_solucion = solucion.reshape((ROWS, COLS))
    print("Matriz solución (celdas a presionar para apagar todas las luces):")
    print(matriz_solucion)
    
    return matriz_solucion  # Retornamos la matriz solución para otros usos


# Loop principal del juego
matriz_solucion = solve_lights_out()
running = True
while running:
    screen.fill(WHITE)
    draw_board()
    
    # Chequear eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Detectar clic en el tablero
            x, y = pygame.mouse.get_pos()
            row, col = y // CELL_SIZE, x // CELL_SIZE
            toggle_light(row, col)  # Cambia la luz y sus vecinos
            if check_win():
                print("¡Ganaste! ¡Has apagado todas las luces!")
                print(matriz_solucion); 
                running = False
    pygame.display.flip()

pygame.quit()