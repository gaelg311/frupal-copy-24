import pn

class Map:

    def __init__(self):
        data = pn.load_map("pn/MAP.txt")
        self.cells = data["MAP"] # 2D List Array with Dict cells
        self.hero_loc = data["HERO_LOC"]
        self.dmd_loc = data["DIAMOND_LOC"]
        self.size = data["X_BOUNDARY"]
        self.hero_inv = data["INVENTORY"]

    def get_hero_coords(self):
        return self.hero_loc
    
    def get_dmd_coords(self):
        return self.dmd_loc
    
    def fetch(self,x:int,y:int) -> dict:
        if x < 0 or y < 0 or x >= self.size or y >= self.size: return None
        return self.cells[y][x]