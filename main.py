import tkinter as tk
import Validation_Grille.py
import fenetre_entre as accueil

# Paramètres de la grille
ROWS = int(accueil.lignes)
COLS = int(accueil.colonnes)
CELL_SIZE = 80
RADIUS = CELL_SIZE // 2 - 5

# Couleurs des jetons
PLAYER_COLORS = {1: "red", 2: "yellow"}

# Grille de jeu (0 = vide, 1 = joueur 1, 2 = joueur 2)
grid = [[0] * COLS for _ in range(ROWS)]
current_player = 1  # j1 commence

def draw_grid():
    """Dessine la grille et les jetons déjà placés."""
    canvas.delete("all")
    for row in range(ROWS):
        for col in range(COLS):
            x = col * CELL_SIZE + CELL_SIZE // 2
            y = row * CELL_SIZE + CELL_SIZE // 2
            color = PLAYER_COLORS.get(grid[row][col], "white")
            canvas.create_oval(x - RADIUS, y - RADIUS, x + RADIUS, y + RADIUS, fill=color, outline="black")

def handle_click(event):
    """Ajoute un jeton dans la colonne sélectionnée."""
    global current_player
    col = event.x // CELL_SIZE
    for row in range(ROWS - 1, -1, -1):
        if grid[row][col] == 0:
            grid[row][col] = current_player
            current_player = 3 - current_player  # Alterne entre 1 et 2
            draw_grid()
            return

def recommencer(): 
    global grid 
    grid = [[0] * COLS for _ in range(ROWS)] 
    draw_grid()
            
# Création de la fenêtre
fenetre = tk.Tk()
fenetre.title("Jouons au puissance 4 !")

canvas = tk.Canvas(fenetre, width=COLS * CELL_SIZE, height=ROWS * CELL_SIZE, bg="blue")
canvas.pack()
button_recommencer = tk.Button(fenetre, text="Recommencer", command=recommencer)
draw_grid()
button_recommencer.pack()
canvas.bind("<Button-1>", handle_click)

fenetre.mainloop()
