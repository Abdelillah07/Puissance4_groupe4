def check_winner():
    """Vérifie si un joueur a gagné."""
    # Vérification horizontale
    for row in range(ROWS):
        for col in range(COLS - 3):
            if grid[row][col] != 0 and all(grid[row][col + i] == grid[row][col] for i in range(4)):
                return grid[row][col]
            