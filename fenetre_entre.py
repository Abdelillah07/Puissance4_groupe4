import tkinter as tk
from main import fen_parties
from set_et_match import fen_parties_set_et_match

fen = tk.Tk()
fen.title("Puissance 4")

label_haut  = tk.Label(fen, text="Mode de jeu")
button_1vs1 = tk.Button(fen, text="1 VS 1", command=fen_parties)
button_1vsRobot = tk.Button(fen, text="1 VS ROBOT")
button_Set_et_Match = tk.Button(fen, text="Set et Match", command=fen_parties_set_et_match)

label_haut.pack(padx=10, pady=10)
button_1vs1.pack(padx=10, pady=10)
button_1vsRobot.pack(padx=10, pady=10)
button_Set_et_Match.pack(padx=10, pady=10)

fen.mainloop()