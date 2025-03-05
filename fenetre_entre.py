import tkinter as tk

def access():
    """Bouton qui prend le nombre de lignes et de colonne de la grille puissance 4 et qui change de fenêtre"""
    global lignes, colonnes
    lignes = entre_lignes.get()
    colonnes = entre_colonnes.get()
    fenetre.quit()

def default():
    """Bouton qui prend le nombre de lignes et de colonne par défaut de la grille puissance 4 et qui change de fenêtre"""
    global lignes, colonnes
    lignes = 6
    colonnes = 7
    fenetre.quit()

lignes, colonnes = 0, 0
fenetre = tk.Tk()
fenetre.title("Puissance 4")

titre = tk.Label(fenetre, text="Choisis le nombre de:")
label_lignes = tk.Label(fenetre, text="Lignes")
label_colonnes = tk.Label(fenetre, text="Colonnes")
entre_lignes = tk.Entry(fenetre)
entre_colonnes = tk.Entry(fenetre)
button_confirmer = tk.Button(fenetre, text="Confirmer", command=access)
button_default = tk.Button(fenetre, text="Par défaut", command=default)

titre.grid(row=0, column=0, columnspan=2)
label_lignes.grid(row=1, column=0, padx=10, pady=10, sticky="e")
label_colonnes.grid(row=2, column=0, padx=10, pady=10, sticky="e")
entre_lignes.grid(row=1, column=1)
entre_colonnes.grid(row=2, column=1)
button_default.grid(row=3, column=0)
button_confirmer.grid(row=3, column=1)

fenetre.mainloop()