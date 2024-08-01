class Cell:
    
    def __init__(self, coord:list, terrain:int, sprite:str, visibility:int):
        self.coord = coord
        self.terrain = terrain
        self.sprite = sprite
        self.visibility = visibility
        