def check_winner():
    """Vérifie si un joueur a gagné."""
    # Vérification horizontale
    for row in range(ROWS):
        for col in range(COLS - 3):
            if grid[row][col] != 0 and all(grid[row][col + i] == grid[row][col] for i in range(4)):
                return grid[row][col]
            

    # Vérification verticale
    for row in range(ROWS - 3):
        for col in range(COLS):
            if grid[row][col] != 0 and all(grid[row + i][col] == grid[row][col] for i in range(4)):
                return grid[row][col]
            
            
    # Vérification diagonale (bas gauche → haut droit)
    for row in range(3, ROWS):
         for col in range(COLS - 3):
            if grid[row][col] != 0 and all(grid[row - i][col + i] == grid[row][col] for i in range(4)):
                return grid[row][col]
            
    # Vérification diagonale (haut gauche → bas droit)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if grid[row][col] != 0 and all(grid[row + i][col + i] == grid[row][col] for i in range(4)):
                return grid[row][col]

    return None  # Aucun gagnant pour l'instant


#On doit modifier handle_click pour vérifier après chaque coup :
def handle_click(event):
    """Ajoute un jeton dans la colonne sélectionnée et vérifie la victoire."""
    global current_player
    col = event.x // CELL_SIZE