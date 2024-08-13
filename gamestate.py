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

        self.hero = hero(self.map.data["ENERGY"],self.map.data["WHIFFLE"],self.map.data["INVENTORY"])
        for item in self.map.hero_inv:
            self.hero.update_inventory(item)
            
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

        window.title("Frupal Test")
        window.geometry("400x300")

    def game_start(self):
        self.create_buttons()
        self.update_labels()

    def update_labels(self):
        if not self.game_over:
            self.cord_header.config(text="Current Position: ("+str(self.x_cord)+","+str(self.y_cord)+")")
            self.energy_header.config(text="Energy: "+str(self.hero.energy))
            self.whiffel_header.config(text="Whiffels: "+ str(self.hero.whiffles))

            self.cord_header.pack()
            self.energy_header.pack()
            self.whiffel_header.pack()
            self.inventory_button.pack()

    def create_buttons(self):
        self.north_button.pack()
        self.east_button.pack()
        self.west_button.pack()
        self.south_button.pack()

    def click_north(self):
        self.y_cord += 1
        self.update_energy()
             
        self.check_map_edge()     
        self.check_end()
        self.update_labels()
        return
    
    def click_east(self):
        self.x_cord += 1
        self.update_energy()

        self.check_map_edge()  
        self.check_end()
        self.update_labels()
        return
    
    def click_west(self):
        self.x_cord -= 1
        self.update_energy()

        self.check_map_edge()  
        self.check_end()
        self.update_labels()
        return
    
    def click_south(self):
        self.y_cord -= 1
        self.update_energy()
    
        self.check_map_edge()  
        self.check_end()
        self.update_labels()
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

    
    def check_end(self):
        if(self.hero.energy == 0):
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
