import tkinter as tk
import Validation_Grille.py

# Paramètres de la grille
ROWS = 6
COLS = 7
CELL_SIZE = 80
RADIUS = CELL_SIZE // 2 - 5

# Couleurs des jetons
PLAYER_COLORS = {1: "red", 2: "yellow"}

# Grille de jeu (0 = vide, 1 = joueur 1, 2 = joueur 2)
grid = [[0] * COLS for _ in range(ROWS)]
current_player = 1  # j1 commence
canvas = None

def access(r, c):
    """Bouton qui prend le nombre de lignes et de colonne de la grille puissance 4 et qui change de fenêtre"""
    global ROWS, COLS
    ROWS = int(r)
    COLS = int(c)
    main()

def fen_accueil():
    
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

    button_confirmer = tk.Button(fenetre, text="Confirmer", command=lambda: access(entre_lignes.get(), entre_colonnes.get()))
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
def main():
    global canvas

    fenetre = tk.Toplevel()
    fenetre.title("Jouons au puissance 4 !")

    # Créer le canvas avec la bonne taille
    canvas = tk.Canvas(fenetre, width=COLS * CELL_SIZE, height=ROWS * CELL_SIZE, bg="blue")
    canvas.pack()
    canvas.bind("<Button-1>", handle_click)

    # Bouton pour recommencer la partie
    button_recommencer = tk.Button(fenetre, text="Recommencer", command=recommencer)
    button_recommencer.pack()

    draw_grid()  # Dessiner la grille au début

    return fenetre

# Création de la fenêtre principale
root = tk.Tk()
root.title("Jeu avec bouton de redémarrage")

# Bouton pour recommencer le jeu
restart_button = tk.Button(root, text="Recommencer", command=restart_game)
restart_button.pack(pady=20)

# Bouton pour enregistrer la partie
save_button = tk.Button(root, text="Enregistrer la partie", command=save_game)
save_button.pack(pady=10)

# commande qui permet de relancer la boucle principale de Tkinter
root.mainloop()
