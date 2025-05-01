import tkinter as tk
from main import fen_parties
from set_et_match import fen_parties_set_et_match

fen = tk.Tk()
fen.title("Puissance 4")
fen.configure(bg="#fff8dc")  # Fond crème clair (jaune pâle)

# Style des boutons avec un fond coloré et une bordure arrondie
button_style = {
    "font": ("Arial", 14, "bold"),
    "width": 20,
    "height": 2,
    "bd": 5,
    "relief": "raised",
    "activebackground": "#32CD32",  # Couleur de fond active (vert clair)
    "bg": "#FFD700",  # Jaune doré
    "fg": "black"
}

# Titre
label_haut = tk.Label(
    fen, text="Choisissez le mode de jeu", font=("Arial", 20, "bold"),
    bg="#fff8dc", fg="#8b8000"
)

# Boutons de mode de jeu
button_1vs1 = tk.Button(fen, text="1 VS 1", command=fen_parties, **button_style)
button_1vsRobot = tk.Button(fen, text="1 VS ROBOT", **button_style)
button_Set_et_Match = tk.Button(fen, text="Set et Match", command=fen_parties_set_et_match, **button_style)

# Placement
label_haut.pack(pady=(30, 20))
button_1vs1.pack(pady=10)
button_1vsRobot.pack(pady=10)
button_Set_et_Match.pack(pady=10)



fen.mainloop()
