import tkinter as tk

# Paramètres de la grille
ROWS = 6
COLS = 7
NB_JETONS_V = 4
CELL_SIZE = 80
RADIUS = CELL_SIZE // 2 - 5

# Couleurs des jetons
PLAYER_COLORS = {1: "red", 2: "yellow"}

# Grille de jeu (0 = vide, 1 = joueur 1, 2 = joueur 2)
grid = [[0] * COLS for _ in range(ROWS)]
current_player = 1  # j1 commence
canvas = None

def access(r, c, nb_jetons_valid):
    """Bouton qui prend le nombre de lignes et de colonne de la grille et qui change de fenêtre"""
    global ROWS, COLS, NB_JETONS_V
    ROWS = int(r)
    COLS = int(c)
    NB_JETONS_V = int(nb_jetons_valid)
    main()

def fen_accueil():
    """Fenêtre d'accueil permettant de changer les parametres du jeu"""
    #Fenêtre de la liste
    fenetre = tk.Toplevel()
    fenetre.title("Puissance 4")

    #Différents widgets de la première fenêtre
    titre = tk.Label(fenetre, text="Choisis le nombre de:")
    label_lignes = tk.Label(fenetre, text="Lignes")
    label_colonnes = tk.Label(fenetre, text="Colonnes")
    label_jetons_valid = tk.Label(fenetre, text="Nombre de jetons pour valider le jeu")
    entre_lignes = tk.Entry(fenetre)
    entre_colonnes = tk.Entry(fenetre)
    entre_jetons_valid = tk.Entry(fenetre)

    button_confirmer = tk.Button(fenetre, text="Confirmer", command=lambda: access(entre_lignes.get(), entre_colonnes.get(), entre_jetons_valid.get()))
    button_default = tk.Button(fenetre, text="Par défaut", command=main)

    #Emplacement des widgets dans la fenêtre
    titre.grid(row=0, column=0, columnspan=2)
    label_lignes.grid(row=1, column=0, padx=10, pady=10, sticky="e")
    label_colonnes.grid(row=2, column=0, padx=10, pady=10, sticky="e")
    label_jetons_valid.grid(row=3, column=0, padx=10, pady=10, sticky="e")
    entre_lignes.grid(row=1, column=1)
    entre_colonnes.grid(row=2, column=1)
    entre_jetons_valid.grid(row=3, column=1)
    button_default.grid(row=4, column=0)
    button_confirmer.grid(row=4, column=1)

    return fenetre

def draw_grid():
    """Dessine la grille et les jetons déjà placés."""
    global ROWS, COLS, CELL_SIZE, RADIUS, PLAYER_COLORS, canvas
    
    canvas.delete("all")
    for row in range(ROWS):
        for col in range(COLS):
            x = col * CELL_SIZE + CELL_SIZE // 2
            y = row * CELL_SIZE + CELL_SIZE // 2
            color = PLAYER_COLORS.get(grid[row][col], "white")
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

#On doit modifier handle_click pour vérifier après chaque coup :
def handle_click(event):
    """Ajoute un jeton dans la colonne sélectionnée et vérifie la victoire."""
    global current_player
    col = event.x // CELL_SIZE
    for row in range(ROWS - 1, -1, -1):
        if grid[row][col] == 0:
            grid[row][col] = current_player
            draw_grid()
            winner = check_winner()
            if winner:
                canvas.unbind("<Button-1>")  # Désactive les clics après la victoire
                canvas.create_text(COLS * CELL_SIZE // 2, ROWS * CELL_SIZE // 2, 
                                   text=f"Joueur {winner} a gagné !", font=("Arial", 45, "bold"), fill="black")
            else:
                current_player = 3 - current_player  # Alterne entre 1 et 2
            return

def recommencer(): 
    global grid 
    grid = [[0] * COLS for _ in range(ROWS)] 
    draw_grid()
            
# Création de la fenêtre
def main():
    global canvas, ROWS, COLS, CELL_SIZE

    fenetre = tk.Toplevel()
    fenetre.title("Jouons au puissance 4 !")

    # Créer le canvas avec la bonne taille
    canvas = tk.Canvas(fenetre, width=COLS * CELL_SIZE, height=ROWS * CELL_SIZE, bg="blue")
    canvas.pack()
    canvas.bind("<Button-1>", handle_click)

    # Bouton pour recommencer la partie
    button_recommencer = tk.Button(fenetre, text="Recommencer", command=recommencer)
    button_recommencer.pack()

    # Création du bouton pour enregistrer
    bouton_enregistrer = tk.Button(fenetre, text="Enregistrer la Partie", command=enregistrer_partie)
    bouton_enregistrer.pack(pady=20)
    draw_grid()  # Dessiner la grille au début

    return fenetre

# Fonction pour enregistrer la partie
def enregistrer_partie():
    with open("sauvegarde.txt", "w") as fichier:
        fichier.write(f"{len(grid)}\n")
        fichier.write(f"{len(grid[0])} \n")
        for i in grid:
            for j in i:
                fichier.write(f"{j}\n")
