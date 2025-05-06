import tkinter as tk
import copy

# Paramètres de la grille
ROWS = 6
COLS = 7
NB_JETONS_V = 4
CELL_SIZE = 100
RADIUS = CELL_SIZE // 2 - 5

# Couleurs des jetons
PLAYER_COLORS = {0:"white", 1: "#FF0000", 2: "#FFD700"}

# Grille de jeu (0 = vide, 1 = joueur 1, 2 = joueur 2)
grid = [[0] * COLS for _ in range(ROWS)]
liste_jetons = []
current_player = 1  # j1 commence
canvas = None

# Fonctions de logique de jeu
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

def undo():
    """Fonction permmettant de revenir en arrière"""
    global grid, liste_jetons
    if liste_jetons != []:
        element = liste_jetons[len(liste_jetons)-1]
        liste_jetons.remove(element)
        row, col = element[0], element[1]
        grid[row][col] = 0
        draw_grid()

def handle_click(event):
    """Ajoute le jeton du joueur dans la colonne sélectionnée"""
    global current_player, grid, liste_jetons
    current_player = 1
    col = event.x // CELL_SIZE
    for row in range(ROWS - 1, -1, -1):
        if grid[row][col] == 0:
            grid[row][col] = current_player
            liste_jetons.append((row,col))
            draw_grid()
            return

def click(event):
    """Ajoute le jeton du joueur puis celui du robot dans la grille et vérifie si il y a un gagnant"""
    global ROWS, COLS, CELL_SIZE
    handle_click(event)
    robot()
    draw_grid()
    winner = check_winner()
    if winner:
        #canvas.unbind("<Button-1>")  # Désactive les clics après la victoire
        canvas.create_text(COLS * CELL_SIZE // 2, ROWS * CELL_SIZE // 2, 
        text=f"Joueur {winner} a gagné !", font=("Arial", 45, "bold"), fill="black")

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

def recommencer(): 
    global grid 
    grid = [[0] * COLS for _ in range(ROWS)] 
    draw_grid()

# Fonctions permmettant de faire fonctionner le robot
def is_terminal(grid):
    """Fonction qui dit si la grille et rempli ou non"""
    tab_row = [i for i in range(len(grid))]
    for index_line in range(len(grid)):
        if 0 not in grid[index_line]:
            tab_row.remove(index_line)
    if tab_row == []:
        return True
    return False

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

def evaluate(grid, player):
    """Fonction qui évalue les lignes de toute la grille verticalement/horizontalement/diagonalameent
    et calcule le score dans une variable 'score' grâce à la fonction evaluate_window"""
    score = 0
    rows = len(grid)
    cols = len(grid[0])
    
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

def get_valid_moves(grid):
    """Renvoi les colonnes de la grille qui ne sont pas encore rempli"""
    lst_col_dispo = []
    for col in range(len(grid[0])):
        for row in range(len(grid)-1,-1,-1):
            if grid[row][col] == 0:
                lst_col_dispo.append(col)
                break
    return lst_col_dispo

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

def robot():
    """Fonction qui place le jeton du robot dans la grille"""
    global grid, current_player
    current_player = 2
    col = meilleur_coup(grid)
    row  = len(grid)-1
    while grid[row][col] != 0:
        row -= 1
    grid[row][col] = 2

# Fonction d'interface utilisateur (fenêtres)
def fenetre_robot():
    """"Fenêtre de l'interface du jeu"""
    global canvas, ROWS, COLS, CELL_SIZE

    fenetre = tk.Toplevel()
    fenetre.title("Jouons au puissance 4 !")
    fenetre.attributes("-fullscreen", True)

    # Obtenir les dimensions de l'écran
    SCREEN_WIDTH = fenetre.winfo_screenwidth()
    SCREEN_HEIGHT = fenetre.winfo_screenheight()

    CANVAS_WIDTH = COLS * CELL_SIZE
    CANVAS_HEIGHT =ROWS * CELL_SIZE

    # Position de la grille dans la fenetre
    pos_x = (SCREEN_WIDTH - CANVAS_WIDTH) // 2
    pos_y = (SCREEN_HEIGHT - CANVAS_HEIGHT) // 2

    # Créer le canvas avec la bonne taille
    canvas = tk.Canvas(fenetre, width=COLS * CELL_SIZE, height=ROWS * CELL_SIZE, bg="blue")
    canvas.place(x=pos_x, y=pos_y)
    canvas.bind("<Button-1>", click)

    # Bouton pour revenir en arrière
    bouton_undo = tk.Button(fenetre, text="🔙", font=("Arial", 32), command=undo)
    bouton_undo.place(x=pos_x+(CANVAS_WIDTH-100), y=pos_y-100)

    # Bouton pour recommencer la partie
    button_recommencer = tk.Button(fenetre, text="⟳", font=("Arial", 32), command=recommencer)
    button_recommencer.place(x=pos_x+CANVAS_WIDTH, y=pos_y-100)

    # Création du bouton pour supprimer la fenêtre principale
    bouton_detruire = tk.Button(fenetre, text="✖", font=("Arial", 32), command=fenetre.destroy)
    bouton_detruire.place(x=pos_x+CANVAS_WIDTH+300, y=pos_y-100)
    draw_grid()  # Dessiner la grille au début

    return fenetre
