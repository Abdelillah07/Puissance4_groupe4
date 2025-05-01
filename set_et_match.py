import tkinter as tk
from main import main, access

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

#Parametres Set et match
winner = None
nb_parties = 0
nb_parties_reserve = 0
VictoireRouge = 0
VictoireJaune = 0
VictoireRougeText = None
VictoireJauneText = None

def fen_parties_set_et_match():
    """Fenêtre de configuration stylisée pour Set et Match."""
    fenetre = tk.Toplevel()
    fenetre.title("Mode Set et Match")
    fenetre.configure(bg="#fff8dc")  # Fond crème

    # Titre
    titre = tk.Label(fenetre, text="Configurer le Set et Match", font=("Arial", 20, "bold"),
                     bg="#fff8dc", fg="#8b8000")
    titre.grid(row=0, column=0, columnspan=2, pady=(20, 10))

    # Champs de configuration
    champs = [
        ("Nombre de lignes :", 1),
        ("Nombre de colonnes :", 2),
        ("Jetons pour gagner :", 3),
        ("Nombre de parties :", 4)
    ]

    entries = {}

    for text, row in champs:
        label = tk.Label(fenetre, text=text, font=("Arial", 12), bg="#fff8dc", fg="black")
        label.grid(row=row, column=0, padx=10, pady=5, sticky="e")
        entry = tk.Entry(fenetre, font=("Arial", 12))
        entry.grid(row=row, column=1, padx=10, pady=5)
        entries[text] = entry

    # Boutons
    confirmer = tk.Button(
        fenetre, text="Confirmer", font=("Arial", 12, "bold"),
        bg="#FFD700", fg="black",
        command=lambda: access(entries["Nombre de lignes :"].get(),
                               entries["Nombre de colonnes :"].get(),
                               entries["Jetons pour gagner :"].get())
    )
    confirmer.grid(row=5, column=1, pady=20)

    annuler = tk.Button(
        fenetre, text="Annuler", font=("Arial", 12, "bold"),
        bg="#e0e0e0", fg="black", command=fenetre.destroy
    )
    annuler.grid(row=5, column=0, pady=20)
def set_et_match(nb_parties_choisis):
    global canvas, ROWS, COLS, CELL_SIZE, nb_parties, nb_parties_reserve, VictoireRougeText, VictoireJauneText

    nb_parties = int(nb_parties_choisis)
    nb_parties_reserve = int(nb_parties_choisis)
    fenetre = tk.Toplevel()
    fenetre.title("Jouons au puissance 4 !")

    VictoireRougeText = tk.Label(fenetre, text=f"Victoires du joueur Rouge: {VictoireRouge}")
    VictoireJauneText = tk.Label(fenetre, text=f"Victoires du joueur Jaune: {VictoireJaune}")
    VictoireRougeText.pack()
    VictoireJauneText.pack()
    # Créer le canvas avec la bonne taille
    canvas = tk.Canvas(fenetre, width=COLS * CELL_SIZE, height=ROWS * CELL_SIZE, bg="blue")
    canvas.pack()
    canvas.bind("<Button-1>", handle_click)

    # Bouton pour Continuer la partie
    button_continuer = tk.Button(fenetre, text="Continuer", command=continuer)
    button_continuer.pack()

    # Bouton pour recommencer la partie
    button_recommencer = tk.Button(fenetre, text="Recommencer à nouveau", command=recommencer)
    button_recommencer.pack()

    draw_grid()  # Dessiner la grille au début

    return fenetre

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
    """Ajoute un jeton dans la colonne sélectionnée et vérifie la victoire."""
    global current_player, grid, winner
    col = event.x // CELL_SIZE
    for row in range(ROWS - 1, -1, -1):
        if grid[row][col] == 0:
            grid[row][col] = current_player
            draw_grid()
            winner = check_winner()
            if winner:
                #canvas.unbind("<Button-1>")  # Désactive les clics après la victoire
                canvas.create_text(COLS * CELL_SIZE // 2, ROWS * CELL_SIZE // 2, 
                                   text=f"Joueur {winner} a gagné !", font=("Arial", 45, "bold"), fill="black")
            else:
                current_player = 3 - current_player  # Alterne entre 1 et 2
            return
        
def continuer(): 
    global grid, winner, nb_parties, VictoireRouge, VictoireJaune, VictoireRougeText, VictoireJauneText

    if winner == 1:
        VictoireRouge += 1
        VictoireRougeText.config(text=f"Victoires du joueur Rouge: {VictoireRouge}")
    elif winner == 2:
        VictoireJaune += 1
        VictoireJauneText.config(text=f"Victoires du joueur Jaune: {VictoireJaune}")
    
    nb_parties -= 1
    if nb_parties != 0:
        grid = [[0] * COLS for _ in range(ROWS)]
        winner = None
        draw_grid()
    else:
        canvas.delete(all)
        draw_grid()
        if VictoireRouge > VictoireJaune:
            canvas.create_text(COLS * CELL_SIZE // 2, ROWS * CELL_SIZE // 2, 
                                   text=f"Joueur 1 a gagné avec\n   {VictoireRouge} points contre {VictoireJaune}!", font=("Arial", 30, "bold"), fill="black")
        elif VictoireJaune > VictoireRouge:
            canvas.create_text(COLS * CELL_SIZE // 2, ROWS * CELL_SIZE // 2, 
                                   text=f"Joueur 2 a gagné avec\n   {VictoireJaune} points contre {VictoireRouge}!", font=("Arial", 30, "bold"), fill="black")
        else:
            grid = [[0] * COLS for _ in range(ROWS)]
            winner = None
            draw_grid()
            nb_parties += 1

def recommencer():
    global grid, current_player, nb_parties, nb_parties_reserve, winner, VictoireRouge, VictoireJaune, VictoireRougeText, VictoireJauneText

    grid = [[0] * COLS for _ in range(ROWS)]
    current_player = 1  # j1 commence
    nb_parties = nb_parties_reserve

    winner = None
    VictoireRouge = 0
    VictoireJaune = 0
    VictoireRougeText.config(text=f"Victoires du joueur Rouge: {VictoireRouge}")
    VictoireJauneText.config(text=f"Victoires du joueur Jaune: {VictoireJaune}")
