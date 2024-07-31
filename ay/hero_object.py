#Andrew Young
#CS314
#Hero Object File
#Still in progress

class hero:
    def __init__(self):
        self.energy = 100 #Starting energy
        self.whiffles = 1000 #Starting whiffles
        self.inventory = ["","",""] #3 item inventory
        self.items = 0
        #self.diamonds = 0 #Royal Diamond count
    
    #Update energy, if it runs out it returns False
    def update_energy(self,to_update) -> bool:
        try:
            self.energy += to_update
            assert self.energy <= 0
        except:
            return False
        return True
    
    def update_whiffles(self,to_update):
        self.whiffles += to_update
        return True
    
    def update_inventory(self,item_to_add):
        if self.items == 3:
            self.change_item(self,item_to_add)
        
        if self.items == 0:
            self.inventory[0] = item_to_add
            self.items += 1
        elif self.items == 1:
            self.inventory[1] = item_to_add
            self.items += 1
        elif self.items == 2:
            self.inventory[2] = item_to_add
            self.items += 1
    
    def change_item(self,item_to_add):
        #Will need to ask them if they want to leave an item
        #0 for no 1 for first item, 2 for second item, 3 for third item
        decision = 0
        if decision == 0:
            return False
        elif decision == 1:
            self.inventory[1] = item_to_add
            return True
        elif decision == 2:
            self.inventory[2] = item_to_add
        elif decision == 3:
            self.inventory[3] = item_to_add
        
    def buy_tool(self,tool,price):
        self.update_inventory(tool)
        self.update_whiffles(-abs(price))
        
        
    
        
        
        
        
            
    
   
        
            
            
