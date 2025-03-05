import tkinter as tk

CANVAS_WIDTH, CANVAS_HEIGHT = 250, 250

fenetre = tk.Tk()
canvas = tk.Canvas(fenetre, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)

titre = tk.Label(fenetre, text="Choisis le nombre de:")
lignes = tk.Label(fenetre, text="Lignes")
colonnes = tk.Label(fenetre, text="Colonnes")


titre.grid(row=0, column=0)

fenetre.mainloop()