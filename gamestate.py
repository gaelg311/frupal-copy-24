import tkinter
from tkinter import ttk 
from hero_object import hero 
from pn import coord_to_string
from map import Map


class game_logic: 
    def __init__(self, window, file:str=None):
        self.window = window
        self.map = Map(file)
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
        self.map_grid_labels = None
        self.map_window = tkinter.Toplevel(self.window)
        self.map_window.title("Map Grid")
        window.title("Frupal Test")
        window.geometry("400x400")

        self.update_map_labels()
        self.update_map_labels()

    def game_start(self):
        self.update_labels()
        self.create_buttons()

    def update_labels(self):
        if not self.game_over:
            self.cord_header.config(text="Current Position: ("+str(self.x_cord+1)+","+str(self.y_cord+1)+")")
            self.energy_header.config(text="Energy: "+str(self.hero.energy))
            self.whiffel_header.config(text="Whiffels: "+ str(self.hero.whiffles))
            self.update_map_labels()

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
        self.y_cord += self.validate_movement(0,1)
        self.update_energy()
             
        self.check_map_edge()     
        self.update_map_labels()
        self.check_end()
        self.update_labels()
        self.obstacle_check()
        self.item_check()
        if(self.inventory_visibility == True):
            self.hide_inventory()
        return
    
    def click_east(self):
        self.x_cord += self.validate_movement(1,0)
        self.update_energy()

        self.check_map_edge()  
        self.check_end()
        self.update_map_labels()
        self.update_labels()
        self.obstacle_check()
        self.item_check()
        if(self.inventory_visibility == True):
            self.hide_inventory()
        return
    
    def click_west(self):
        self.x_cord -= self.validate_movement(-1,0)
        self.update_energy()

        self.check_map_edge()  
        self.check_end()
        self.update_map_labels()
        self.update_labels()
        self.obstacle_check()
        self.item_check()
        if(self.inventory_visibility == True):
            self.hide_inventory()
        return
    
    def click_south(self):
        self.y_cord -= self.validate_movement(0,-1)
        self.update_energy()
    
        self.check_map_edge()  
        self.check_end()
        self.update_map_labels()
        self.update_labels()
        self.obstacle_check()
        self.item_check()
        if(self.inventory_visibility == True):
            self.hide_inventory()
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
        try:
            cell = self.map.fetch(self.x_cord, self.y_cord)["T"]

            if cell == 0 or cell == 1:
                self.hero.energy -= 1

            if cell == 4 or cell == 5:
                self.hero.energy -= 2
        except: pass
        
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
        self.itemUse = False

    def validate_movement(self,dx:int,dy:int) -> int:
        x = 0 if self.x_cord + dx == self.map_size_x else self.map_size_x-1 if self.x_cord + dx < 0 else self.x_cord + dx
        y = 0 if self.y_cord + dy == self.map_size_y else self.map_size_y-1 if self.y_cord + dy < 0 else self.y_cord + dy
        terrain = self.map.fetch(x, y)["T"]
        if terrain == 3 or terrain == 2 and not self.hero.check_item("Boat"):
            return 0
        else:
            return 1


    def obstacle_check(self):
        obstacle = self.map.fetch(self.x_cord, self.y_cord)["S"]
        print(self.hero.inventory)
        self.current_item_index = 0
        self.itemUse = False

        if obstacle.upper() == "TREE":
            self.items_to_check = [("Hatchet", 8), ("Axe", 6), ("Chainsaw", 2)]
            self.obstacle_removal(10)
            self.map.fetch(self.x_cord, self.y_cord)["S"] = "None"
        
        elif obstacle.upper() == "BOULDER":
            self.items_to_check = [("Chisel", 15), ("Sledge", 12), ("Jackhammer", 4)]
            self.obstacle_removal(16)
            self.map.fetch(self.x_cord, self.y_cord)["S"] = "None"
        
        elif obstacle.upper() == "BLACKBERRY_BUSHES":
            self.items_to_check = [("Machete", 2), ("Shears", 2)]
            self.obstacle_removal(4)
            self.map.fetch(self.x_cord, self.y_cord)["S"] = "None"


    def obstacle_removal(self, default):
        if self.current_item_index < len(self.items_to_check):
            item, cost = self.items_to_check[self.current_item_index]
            if self.hero.check_item(item) and not self.itemUse:
                self.ask_use_item(item, cost, default)
            else:
                self.current_item_index += 1
                self.obstacle_removal(default)
        else:
            self.hero.energy -= default
            self.update_labels()


    
    def ask_use_item(self, item, cost, default):
        self.ques_label = tkinter.Label(text="You have a " + item + ". Would you like to use it?", wraplength=400)
        self.use_button = tkinter.Button(self.window, text = "Yes", command=lambda: self.yes_item(item,cost))
        self.dont_button = tkinter.Button(self.window, text = "No", command=lambda: self.no_item(default))
        self.ques_label.pack()
        self.use_button.pack(side="right",padx=60)
        self.dont_button.pack(side="left",padx=60)

    def yes_item(self, item, cost):
        self.dont_use_item()
        self.hero.use_item(item)
        self.hero.energy -= cost
        self.itemUse = True
        self.update_labels()

    def no_item(self, default):
        self.dont_use_item()
        self.current_item_index += 1
        self.obstacle_removal(default)

    def dont_use_item(self):
        self.ques_label.destroy(), self.use_button.destroy(), self.dont_button.destroy()
        self.ques_label, self.use_button, self.dont_button = None, None, None
        self.itemUse = False        


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
            try: widget.pack_forget()
            except: pass
    

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
        self.inventory_frame.pack(side="bottom")

        #create a canvas based on the inventory frame
        canvas = tkinter.Canvas(self.inventory_frame, width=350, height=200)

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
            item_label.pack(anchor="center", pady=2)
        canvas.update_idletasks()


        #update button to "hide inventory"
        self.inventory_button.config(text= "Hide Inventory")
        self.inventory_visibility = True


    def hide_inventory(self):
        #hide the inventory by removing the inventory frame 
        if self.inventory_frame:
            self.inventory_frame.destroy()
            self.inventory_frame = None
        
        if self.inventory_button: 
            self.inventory_button.config(text="Show Inventory")
            self.inventory_visibility = False
    
    def create_map_labels(self):
        self.sprite_grid = self.map.get_map(self.x_cord, self.y_cord, self.hero.check_item("Binoculars"))
    
    def update_map_labels(self):
        if not hasattr(self, 'label_grid'):
            self.label_grid = []

        else:
            for i in range(len(self.label_grid)):
                for j in range(len(self.label_grid[0])):
                    if self.label_grid[i][j].cget("text") != "#": 
                        self.label_grid[i][j].config(text="#", bg="gray")

        self.sprite_grid = self.map.get_map(self.x_cord, self.y_cord, self.hero.check_item("Binoculars"))

        for r in range(len(self.sprite_grid)):
            if len(self.label_grid) <= r:
                self.label_grid.append([])

            for c in range(len(self.sprite_grid[r])):
                cell = self.sprite_grid[r][c]
                cell_text = ("&" if cell[0] in ["Tree", "Blackberry_Bushes", "Boulder"] else "!" if cell[0] == "PowerBar" else "s" if cell[0] == "Shears" else "c" if cell[0] == "Chisel" else "S" if cell[0] == "Sledge" else "M" if cell[0] == "Machete" else
                             "a" if cell[0] == "Axe" else "C" if cell[0] == "Chainsaw" else "b" if cell[0] == "Boat" else "B" if cell[0] == "Binoculars" else "h" if cell[0] == "Hatchet" else "j" if cell[0] == "Jackhammer" else
                             "#" if cell[0] == "BORDER" else "@" if cell[0] == "Player" else ".")
                cell_bg = "#008800" if cell[1] == 0 else "#006600" if cell[1] == 0 else "#00aa00" if cell[1] == 1 else "#7777ff" if cell[1] == 2 else "#aaaaaa" if cell[1] == 3 else "#22ff22" if cell[1] == 4 else "#11ff33" if cell[1] == 5 else "gray"
                if len(self.label_grid[r]) <= c:
                    label = tkinter.Label(self.map_window, text=cell_text, borderwidth=1, font=("Courier", 12), bg=cell_bg)
                    label.grid(row=r, column=c, padx=1, pady=1, sticky="nsew")
                    self.label_grid[r].append(label)
                else:
                    label = self.label_grid[r][c]
                    label.config(text=cell_text, bg=cell_bg)

                if f"({cell[3][0]},{cell[3][1]})" == self.diamond_cords and cell_text != "#": label.config(text="*")
                if cell[3] == (self.x_cord, self.y_cord): label.config(text="@")

        for r in range(len(self.sprite_grid)):
            self.map_window.grid_rowconfigure(r, weight=1)
            self.map_window.grid_columnconfigure(r, weight=1)