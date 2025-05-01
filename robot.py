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

#Fonctions manquantes en plusieurs lignes
    #PAS ENCORE FAIT

def evaluate(grid, player):
    """Fonction qui évalue les lignes de toute la grille verticalement/horizontalement/diagonalameent
    et calcule le score dans une variable 'score' grâce à la fonction evaluate_window"""
    score = 0
    rows = len(grid)
    cols = len(grid[0])

    ## Bonus pour jouer au centre (colonne centrale)
    center_col = cols // 2
    center_array = [grid[r][center_col] for r in range(rows)]
    center_count = center_array.count(player)
    score += center_count * 6

    ## Évaluer lignes horizontales
    for r in range(rows):
        for c in range(cols - 3):
            window = [grid[r][c+i] for i in range(4)]
            score += evaluate_window(window, player)

    ## Évaluer colonnes verticales
    for c in range(cols):
        for r in range(rows - 3):
            window = [grid[r+i][c] for i in range(4)]
            score += evaluate_window(window, player)

    ## Évaluer diagonales positives (bas-gauche → haut-droit)
    for r in range(rows - 3):
        for c in range(cols - 3):
            window = [grid[r+i][c+i] for i in range(4)]
            score += evaluate_window(window, player)

    ## Évaluer diagonales négatives (haut-gauche → bas-droit)
    for r in range(3, rows):
        for c in range(cols - 3):
            window = [grid[r-i][c+i] for i in range(4)]
            score += evaluate_window(window, player)

    return score

def minimax(grid, depth, maximizing_player):
    """Fonction qui renvoi le meilleur de score du meilleur 
    coup que le robot peut jouer tout en minimisant au maximum le score du joueur"""
    global current_player
    if depth == 0 or is_terminal(grid):
        return evaluate(grid, current_player)

    if maximizing_player:
        max_eval = float('-inf')
        for col in get_valid_moves(grid):
            new_grid = simulate_move(grid, col, current_player)
            eval = minimax(new_grid, depth-1, False)
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for col in get_valid_moves(grid):
            new_grid = simulate_move(grid, col, current_player)
            eval = minimax(new_grid, depth-1, True)
            min_eval = min(min_eval, eval)
        return min_eval
    
def meilleur_coup(grid):
    """Fonction qui renvoi la colonne qui permet de gagner au robot avec la meilleur stratégie"""
    global current_player
    meilleur_score = float('-inf')
    best_coup = None
    for col in get_valid_moves(grid):
        grille = simulate_move(grid, col, current_player)        
        score = minimax(grille, 3, False)
        if score > meilleur_score:
            meilleur_score = score
            best_coup = col
    return best_coup

def evaluate_window(window, player):
    """Calcul le score d'une fenêtre de la grille en fonction du nombre de jetons aligner dans une ligne"""
    score = 0
    opponent = 2 if player == 1 else 1

    if window.count(player) == 4:
        score += 1000
    elif window.count(player) == 3 and window.count(0) == 1:
        score += 50
    elif window.count(player) == 2 and window.count(0) == 2:
        score += 10

    if window.count(opponent) == 3 and window.count(0) == 1:
        score -= 80

    return score

def simulate_move(grid, col, player):
    """Renvoi une grille sumilant le prochain coup de jeton (Rouge ou Jaune)"""
    # Copier la grille pour ne pas modifier l'original
    new_grid = copy.deepcopy(grid)

    # Chercher la première case vide en partant du bas
    for row in range(len(grid) - 1, -1, -1):
        if new_grid[row][col] == 0:
            new_grid[row][col] = player
            break

    return new_grid

 def is_terminal(grid):
    """Fonction qui dit si la grille et rempli ou non"""
    tab_row = [i for i in range(len(grid))]
    for index_line in range(len(grid)):
        if 0 not in grid[index_line]:
            tab_row.remove(index_line)
    if tab_row == []:
        return True
    return False
