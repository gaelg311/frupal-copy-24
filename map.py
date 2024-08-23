import pn

FILE:str = "map_files/MAP01.txt"

class Map:

    def __init__(self):
        self.data = pn.load_map(FILE)
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

    def get_map(self,x:int,y:int,binoculars:bool):
        RADIUS = 10
        grid = []
        max_r = min(y + RADIUS, self.size - 1)
        min_r = max(y - RADIUS, 0)
        max_c = min(x + RADIUS, self.size - 1)
        min_c = max(x - RADIUS, 0)

        for r in range(max_r, min_r - 1, -1):
            row = []
            for c in range(min_c, max_c + 1):
                try:
                    curr_cell = [self.fetch(c, r)["S"], self.fetch(c, r)["T"], self.fetch(c, r)["V"], (c,r)]
                except:
                    curr_cell = ["BORDER", -1, 0, (c,r)]
                if abs(r - y) <= 2 and abs(c - x) <= 2 and binoculars:
                    self.cells[r][c]["V"] = 1
                elif abs(r - y) <= 1 and abs(c - x) <= 1:
                    self.cells[r][c]["V"] = 1
                if curr_cell[2] != 1:
                    curr_cell = ["BORDER", -1, 0, (c,r)]
                row.append(curr_cell)
            grid.append(row)

        return grid

    def fetch_item(self,item:str="None") -> dict:
        '''A "switch-case" that fetches item info formatted in this manner:
        {"info": str, "e": int, "cost": int}
        
        `item = fetch_item(item_name)`

        In this case, `item` would hold the following information:
        `item["info"]` holds details regarding the use of item.
        `item["e"]` holds the energy cost needed to use item (if any).
        `item["cost"]` holds the whiffle cost of buying the item.
        
        If the `item` cannot be found, it will return as `None`'''

        if item == "PowerBar": 
            return {
                "info": "gives +20 energy",
                "e": -20,
                "cost": 1
            }
        elif item == "Hatchet":
            return {
                "info": "can remove a tree for 8 energy",
                "e": 8,
                "cost": 15
            }
        elif item == "Axe":
            return {
                "info": "can remove a tree for 6 energy",
                "e": 6,
                "cost": 30
            }
        elif item == "Chainsaw":
            return {
                "info": "can remove a tree for 2 energy",
                "e": 2,
                "cost": 60
            }
        elif item == "Chisel":
            return {
                "info": "can remove a boulder for 15 energy",
                "e": 15,
                "cost": 5
            }
        elif item == "Sledge":
            return {
                "info": "can remove a boulder for 12 energy",
                "e": 12,
                "cost": 25
            }
        elif item == "Jackhammer":
            return {
                "info": "can remove a boulder for 4 energy",
                "e": 4,
                "cost": 100
            }
        elif item == "Machete":
            return {
                "info": "can remove a blackberry bushes for 2 energy",
                "e": 2,
                "cost": 25
            }
        elif item == "Shears":
            return {
                "info": "can remove a blackberry bushes for 2 energy",
                "e": 2,
                "cost": 35
            }
        elif item == "Binoculars":
            return {
                "info": "increases the distance of your vision",
                "e": 0,
                "cost": 50
            }
        elif item == "Boat":
            return {
                "info": "it allows water traversal at zero energy cost",
                "e": 0,
                "cost": 250
            }
        else:
            return None