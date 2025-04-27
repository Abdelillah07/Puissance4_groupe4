import tkinter as tk
import main

def ouvrir_fenetre():
    main.fen_accueil()

# Création de la fenêtre principale
fen = tk.Tk()
fen.title("Puissance 4")
fen.geometry("400x400")  # Taille de la fenêtre
fen.configure(bg="#ADD8E6")  # Fond bleu clair

# Titre avec une police moderne et un fond coloré
label_haut = tk.Label(fen, text="Mode de jeu", font=("Arial", 18, "bold"), bg="#ADD8E6", fg="black")
label_haut.pack(pady=20)

# Style des boutons avec un fond coloré et une bordure arrondie
button_style = {
    "font": ("Arial", 14),
    "width": 20,
    "height": 2,
    "bd": 5,
    "relief": "raised",
    "activebackground": "#32CD32",  # Couleur de fond active
    "bg": "#FFD700",  # Couleur de fond des boutons
    "fg": "black"
}

# Boutons pour les différents modes de jeu
button_1vs1 = tk.Button(fen, text="1 VS 1", **button_style, command=ouvrir_fenetre)
button_1vsRobot = tk.Button(fen, text="1 VS ROBOT", **button_style, command=ouvrir_fenetre)
button_Set_et_Match = tk.Button(fen, text="Set et Match", **button_style, command=ouvrir_fenetre)

# Espacement des boutons et ajout à la fenêtre
button_1vs1.pack(pady=15)
button_1vsRobot.pack(pady=15)
button_Set_et_Match.pack(pady=15)

# Lancer la boucle principale de l'interface
fen.mainloop()

