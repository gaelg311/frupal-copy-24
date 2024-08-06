#Andrew Young
#CS314
#Hero Object File
#Still in progress

class hero:
    def __init__(self):
        self.energy = 100 #Starting energy
        self.whiffles = 1000 #Starting whiffles
        self.inventory = [] #Empty inventory
        self.items = 0
        #self.diamonds = 0 #Royal Diamond count
    
   
    def increase_whiffles(self,to_update):
        self.whiffles += to_update
        return True
    
    
    def update_inventory(self,item_to_add):
        self.inventory.append(item_to_add)
        self.items += 1
        return True
    '''
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
            self.inventory[3] = item_to_add'''
        
    def buy_tool(self,tool,price):
        if (self.whiffles - price) > -1:
            self.update_inventory(tool)
            self.whiffles -= price
            return True
        else:
            return False
    
    def use_item(self,item_needed):
        if len(self.inventory) == 0:
            return False
        
        itm_index= None
        try:
            itm_index = self.inventory.index(item_needed)
        except:
            return False
        
        self.inventory.pop(itm_index)
        return True
        



        
    
        
        
        
        
            
    
   
        
            
            
