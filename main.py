from hero_object import hero 
from gamestate import game_logic 
import tkinter as tk
import pn as map_loader

def main():
    sample = tk.Tk() 
    game = game_logic(sample)

    game.game_start()
    sample.mainloop()

if __name__ == "__main__":
    main()