import tkinter as tk

# Paramètres de la grille
ROWS = 6
COLS = 7
NB_JETONS_V = 4
CELL_SIZE = 80
RADIUS = CELL_SIZE // 2 - 5

# Couleurs des jetons
PLAYER_COLORS = {0:"white", 1: "red", 2: "yellow"}

# Grille de jeu (0 = vide, 1 = joueur 1, 2 = joueur 2)
grid = [[0] * COLS for _ in range(ROWS)]
current_player = 1  # j1 commence
canvas = None

def fenetre_robot():
    global canvas, ROWS, COLS, CELL_SIZE

    fenetre = tk.Toplevel()
    fenetre.title("Jouons au puissance 4 !")

    # Créer le canvas avec la bonne taille
    canvas = tk.Canvas(fenetre, width=COLS * CELL_SIZE, height=ROWS * CELL_SIZE, bg="blue")
    canvas.pack()
    canvas.bind("<Button-1>", click)

    # Bouton pour recommencer la partie
    button_recommencer = tk.Button(fenetre, text="Recommencer", command=recommencer)
    button_recommencer.pack()

    # Création du bouton pour enregistrer
    bouton_enregistrer = tk.Button(fenetre, text="Enregistrer la Partie")
    bouton_enregistrer.pack(pady=20)
    draw_grid()  # Dessiner la grille au début

    return fenetre

def recommencer(): 
    global grid 
    grid = [[0] * COLS for _ in range(ROWS)] 
    draw_grid()

#Fonctions déjà existantes dans main.py
def draw_grid():
    """Dessine la grille et les jetons déjà placés."""
    global ROWS, COLS, CELL_SIZE, RADIUS, PLAYER_COLORS, canvas

    canvas.delete("all")
    for row in range(ROWS):
        for col in range(COLS):
            x = col * CELL_SIZE + CELL_SIZE // 2
            y = row * CELL_SIZE + CELL_SIZE // 2
            color = PLAYER_COLORS[grid[row][col]]
            canvas.create_oval(x - RADIUS, y - RADIUS, x + RADIUS, y + RADIUS, fill=color, outline="black")

def check_winner():
    """Vérifie si un joueur a gagné."""
    global grid, NB_JETONS_V
    # Vérification horizontale
    for row in range(ROWS):
        for col in range(COLS - 3):
            if grid[row][col] != 0 and all(grid[row][col + i] == grid[row][col] for i in range(NB_JETONS_V)):
                return grid[row][col]
            
    # Vérification verticale
    for row in range(ROWS - 3):
        for col in range(COLS):
            if grid[row][col] != 0 and all(grid[row + i][col] == grid[row][col] for i in range(NB_JETONS_V)):
                return grid[row][col]

    # Vérification diagonale (bas gauche → haut droit)
    for row in range(3, ROWS):
         for col in range(COLS - 3):
            if grid[row][col] != 0 and all(grid[row - i][col + i] == grid[row][col] for i in range(NB_JETONS_V)):
                return grid[row][col]
            
    # Vérification diagonale (haut gauche → bas droit)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if grid[row][col] != 0 and all(grid[row + i][col + i] == grid[row][col] for i in range(NB_JETONS_V)):
                return grid[row][col]

    return None  # Aucun gagnant pour l'instant

def handle_click(event):
    """Ajoute le jeton du joueur dans la colonne sélectionnée"""
    global current_player, grid
    current_player = 1
    col = event.x // CELL_SIZE
    for row in range(ROWS - 1, -1, -1):
        if grid[row][col] == 0:
            grid[row][col] = current_player
            draw_grid()
            return