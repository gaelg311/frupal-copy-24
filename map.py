import pn

class Map:

    def __init__(self):
        self.data = pn.load_map("pn/MAP.txt")
        self.cells = self.data["MAP"] # 2D List Array with Dict cells
        self.hero_loc = self.data["HERO_LOC"]
        self.dmd_loc = self.data["DIAMOND_LOC"]
        self.size = self.data["X_BOUNDARY"]
        self.hero_inv = self.data["INVENTORY"]

    def get_hero_coords(self):
        return self.hero_loc
    
    def get_dmd_coords(self):
        return self.dmd_loc
    
    def fetch(self,x:int,y:int) -> dict:
        if x < 0 or y < 0 or x >= self.size or y >= self.size: return None
        return self.cells[y][x]
    
    def set(self,x:int,y:int,layer:str,value):
        if self.fetch(x,y)[layer] != None:
            try: self.cells[y][x][layer] = int(value)
            except: self.cells[y][x][layer] = value
    