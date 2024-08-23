import tkinter
from tkinter import ttk 
from hero_object import hero 
from pn import coord_to_string
from map import Map


class game_logic: 
    def __init__(self, window):
        self.window = window
        self.map = Map()
        self.x_cord = self.map.hero_loc[0]
        self.y_cord = self.map.hero_loc[1]
        self.diamond_cords = coord_to_string(self.map.dmd_loc)
        self.game_over = False
        self.map_size_x = self.map.size
        self.map_size_y = self.map.size
        self.itemUse = False
        self.ask_label = None
        self.yes_button = None
        self.no_button = None

        self.hero = hero(self.map.data["ENERGY"],self.map.data["WHIFFLE"],self.map.data["INVENTORY"])
            
        print(self.hero.inventory)

        self.cord_header = tkinter.Label(text="Current Position: ("+str(self.x_cord)+","+str(self.y_cord)+")")
        self.energy_header = tkinter.Label(text="Energy: "+str(self.hero.energy))                
        self.whiffel_header = tkinter.Label(text="Whiffles: "+ str(self.hero.whiffles))

        #movement buttons
        self.north_button = tkinter.Button(self.window, text = "NORTH", command=lambda: self.click_north())
        self.east_button = tkinter.Button(self.window, text = "EAST", command=lambda: self.click_east())
        self.west_button = tkinter.Button(self.window, text = "WEST", command=lambda: self.click_west())
        self.south_button = tkinter.Button(self.window, text = "SOUTH", command=lambda: self.click_south())

        #button to toggle inventory 
        self.inventory_button = tkinter.Button(self.window, text = "Show Inventory", command=lambda: self.toggle_inventory())
        self.inventory_visibility = False 
        self.inventory_frame = None
        
        #Map labels
        self.map_grid_labels = [tkinter.Label(self.window, text=""),tkinter.Label(self.window, text=""),tkinter.Label(self.window, text=""),tkinter.Label(self.window, text=""),tkinter.Label(self.window, text="")]
        self.sprite_grid = None
        
        window.title("Frupal Test")
        window.geometry("400x500")

    def game_start(self):
        self.update_labels()
        self.create_buttons()

    def update_labels(self):
        if not self.game_over:
            self.cord_header.config(text="Current Position: ("+str(self.x_cord)+","+str(self.y_cord)+")")
            self.energy_header.config(text="Energy: "+str(self.hero.energy))
            self.whiffel_header.config(text="Whiffels: "+ str(self.hero.whiffles))
            self.update_map_labels()
            
            for label in self.map_grid_labels:
                label.pack()
            self.cord_header.pack()
            self.energy_header.pack()
            self.whiffel_header.pack()

            if self.ask_label != None:
                self.ask_label.destroy()
                self.ask_label = None
            if self.no_button != None:
                self.no_button.destroy()
                self.yes_button.destroy()
                self.no_button, self.yes_button = None, None

    def create_buttons(self):
        self.north_button.pack()
        self.east_button.pack()
        self.west_button.pack()
        self.south_button.pack()
        self.inventory_button.pack()

    def click_north(self):
        self.y_cord += 1
        self.map.update(self.x_cord,self.y_cord,"Binoculars" in self.hero.inventory)
        self.update_energy()
             
        self.check_map_edge()     
        self.check_end()
        self.update_labels()
        self.obstacle_check()
        self.item_check()
        return
    
    def click_east(self):
        self.x_cord += 1
        self.map.update(self.x_cord,self.y_cord,"Binoculars" in self.hero.inventory)
        self.update_energy()

        self.check_map_edge()  
        self.check_end()
        self.update_labels()
        self.obstacle_check()
        self.item_check()
        return
    
    def click_west(self):
        self.x_cord -= 1
        self.map.update(self.x_cord,self.y_cord,"Binoculars" in self.hero.inventory)
        self.update_energy()

        self.check_map_edge()  
        self.check_end()
        self.update_labels()
        self.obstacle_check()
        self.item_check()
        return
    
    def click_south(self):
        self.y_cord -= 1
        self.map.update(self.x_cord,self.y_cord,"Binoculars" in self.hero.inventory)
        self.update_energy()
    
        self.check_map_edge()  
        self.check_end()
        self.update_labels()
        self.obstacle_check()
        self.item_check()
        return
    
    def check_map_edge(self):
        if(self.x_cord >= self.map_size_x):
            self.x_cord = 0

        if(self.x_cord < 0):
            self.x_cord = self.map_size_x - 1
        
        if(self.y_cord >= self.map_size_y):
            self.y_cord = 0
        
        if(self.y_cord < 0):
            self.y_cord = self.map_size_y - 1 
        return
    
    def update_energy(self):
        cell = self.map.fetch(self.x_cord, self.y_cord)["T"]

        if cell == 0 or cell == 1:
            self.hero.energy -= 1

        if cell == 4 or cell == 5:
            self.hero.energy -= 2
        
    def item_check(self):
        item = self.map.fetch(self.x_cord, self.y_cord)["S"]
        details = self.map.fetch_item(item)

        if item == "None" or details == None: return None
        else: return self.shop_item(item,details["info"],details["cost"])

    def shop_item(self,item:str,msg:str,cost:int):
        self.ask_label = tkinter.Label(text=f"Encountered a{"n" if item.lower()[0] in ["a","o","u","y","i"] else ""}" 
                                    + f" {item} ({msg}), it costs {cost} whiffle{"s" if cost > 1 else ""}.\nBuy it?",
                                    wraplength=400)
        self.yes_button = tkinter.Button(self.window, text = "Yes", command=lambda: self.buy_item(item,cost))
        self.no_button = tkinter.Button(self.window, text = "No", command=lambda: self.dont_buy_item())
        self.ask_label.pack()
        self.yes_button.pack(side="right",padx=60)
        self.no_button.pack(side="left",padx=60)

    def buy_item(self,item:str,cost:int):
        self.dont_buy_item() # Calling this to delete the buttons and labels
        if not self.hero.buy_tool(item,cost):
            self.ask_label = tkinter.Label(text=f"Not enough whiffles to buy that!")
            self.ask_label.pack()
        else:
            self.update_labels()
            self.map.set(self.x_cord, self.y_cord, "S", "None")

    def dont_buy_item(self):
        self.ask_label.destroy(), self.yes_button.destroy(), self.no_button.destroy()
        self.ask_label, self.yes_button, self.no_button = None, None, None
        

    def obstacle_check(self):
        obstacle = self.map.fetch(self.x_cord, self.y_cord)["S"]
        print(obstacle)
        print(self.hero.inventory)

        if obstacle.upper() == "TREE":
            self.obstacle_tree()
        
        elif obstacle.upper() == "BOULDER":
            self.hero.energy -= 16
        
        elif obstacle.upper() == "BLACKBERRY_BUSHES":
            self.hero.energy -= 4

    def obstacle_tree(self):
        self.itemUse = False
        if self.hero.check_item("Hatchet") == True and self.itemUse == False:    
            self.use_item_buttons(8, "Hatchet")

        else:       
            self.use_item_buttons(10, "None")

    def use_item_buttons(self, energyUse, name):
        if name == "None":
            self.hero.energy -= energyUse
            return
        
        self.hide_movement_btns()
        self.user_item_question = tkinter.Label(text="Do you want to use a " + name)  
        self.yes_button = tkinter.Button(self.window, text = "Yes", command=lambda: self.assignItemUse(True, energyUse, name))
        self.no_button = tkinter.Button(self.window, text = "No", command=lambda: self.assignItemUse(False, energyUse, name))

        self.user_item_question.pack()
        self.yes_button.pack()
        self.no_button.pack()

    def assignItemUse(self, didUse, energyUse, name):
        self.itemUse = didUse
        if didUse == True:
            self.hero.energy -= energyUse
            self.hero.use_item(name)
        
        self.hide_use_item()
        self.create_buttons()
        
    def hide_use_item(self):
        self.user_item_question.pack_forget()
        self.yes_button.pack_forget()
        self.no_button.pack_forget()

    def hide_movement_btns(self):
        self.north_button.pack_forget()
        self.south_button.pack_forget()
        self.east_button.pack_forget()
        self.west_button.pack_forget()
    


    def check_end(self):
        if(self.hero.energy <= 0):
            self.energy_depleted_end()

        if("("+str(self.x_cord)+","+str(self.y_cord)+")" == self.diamond_cords):
            self.victory() 

    def energy_depleted_end(self):
        self.clear_screen()
        self.game_over = True

        end_text = tkinter.Label(self.window, text="You have run out of energy! Game over!")

        end_text.pack()

        quit_button = tkinter.Button(self.window, text="Quit", command=self.window.quit)

        quit_button.pack()

    def victory(self):
        self.clear_screen()

        self.game_over = True
        victory_text = tkinter.Label(self.window, text= "You have found the diamonds! Congratulations!")
        victory_text.pack()
        
        quit_button = tkinter.Button(self.window, text="Quit", command=self.window.quit)

        quit_button.pack()
        
    def clear_screen(self):
        for widget in self.window.winfo_children():
            widget.pack_forget()
    

    def toggle_inventory(self):
        #check if inventory is visible or not before execution
        if not self.inventory_visibility:
            self.show_inventory()
        else:
            self.hide_inventory()

    def show_inventory(self):
        #create a scrollable frame to show the hero inventory 
        
        #start by allocating the inventory frame, immediatly pack 
        self.inventory_frame = tkinter.Frame(self.window)
        self.inventory_frame.pack()

        #create a canvas based on the inventory frame
        canvas = tkinter.Canvas(self.inventory_frame)

        #use ttk to create a scrollbar widget and scrollable frame to display 
        scrollbar = ttk.Scrollbar(self.inventory_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tkinter.Frame(self.inventory_frame)

        #this function updates whenever the the contents of the scrollable_frame changes 
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        #draw canvas, make sure that when y-position is changed, the scrollbar moves 
        canvas.create_window((0,0), window = scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        #pack canvas + scrollbar 
        canvas.pack(side="right",  fill="both", expand=True)
        scrollbar.pack(side="left", fill="y")

        #populate using hero inventory
        for item in self.hero.inventory:
            item_label = tkinter.Label(scrollable_frame, text = str(item))
            item_label.pack()

        #update button to "hide inventory"
        self.inventory_button.config(text= "Hide Inventory")
        self.inventory_visibility = True

    def hide_inventory(self):
        #hide the inventory by removing the inventory frame 
        if self.inventory_frame:
            self.inventory_frame.destroy()
            self.inventory_button = None
        
        self.inventory_button.config(text="Show Inventory")
        self.inventory_visibility = False
    
    
    def update_map_labels(self):
        self.sprite_grid = self.map.get_map(self.x_cord,self.y_cord)
        if self.hero.check_item("Binoculars"):
            for i in range(5):
                self.map_grid_labels[i].config(text= self.sprite_grid[i][0] + " " + self.sprite_grid[i][1] + " " + self.sprite_grid[i][2] + " " + self.sprite_grid[i][3] + " " + self.sprite_grid[i][4] + " ")
            return
        else:
            #print(self.sprite_grid)
            self.map_grid_labels[0].config(text= "X X X X X")
            self.map_grid_labels[1].config(text= "X "+self.sprite_grid[1][1]+" "+self.sprite_grid[1][2]+" "+self.sprite_grid[1][3]+" X")
            self.map_grid_labels[2].config(text= "X "+self.sprite_grid[2][1]+" "+self.sprite_grid[2][2]+" "+self.sprite_grid[2][3]+" X")
            self.map_grid_labels[3].config(text= "X "+self.sprite_grid[3][1]+" "+self.sprite_grid[3][2]+" "+self.sprite_grid[3][3]+" X")
            self.map_grid_labels[4].config(text= "X X X X X")
            return
                
 
        
                
                
