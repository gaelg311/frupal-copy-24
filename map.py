import pn

class Map:

    def __init__(self):
        data = pn.load_map("pn/MAP.txt")
        self.cells = data["MAP"] # 2D List Array with Dict cells
        self.hero_loc = data["HERO_LOC"]
        self.dmd_loc = data["DIAMOND_LOC"]
        self.size = data["X_BOUNDARY"]

    def get_hero_coords(self):
        return self.hero_loc
    
    def get_dmd_coords(self):
        return self.dmd_loc