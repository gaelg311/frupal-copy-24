import tkinter
from hero_object import hero 
import pn as map_loader

class game_logic: 
    def __init__(self, window):
        self.window = window
        self.x_cord = 0
        self.y_cord = 0
        self.hero = Hero()
        self.diamond_cords = "(1,2)"
        self.game_over = False 
        self.map_size_x = 5 
        self.map_size_y = 5

        self.cord_header = tkinter.Label(text="Current Position: ("+str(self.x_cord)+","+str(self.y_cord)+")")
        self.energy_header = tkinter.Label(text="Energy: "+str(self.hero.energy))                
        self.whiffel_header = tkinter.Label(text="Whiffels: "+ str(self.hero.whiffels))

        self.north_button = tkinter.Button(self.window, text = "NORTH", command=lambda: self.click_north())
        self.east_button = tkinter.Button(self.window, text = "EAST", command=lambda: self.click_east())
        self.west_button = tkinter.Button(self.window, text = "WEST", command=lambda: self.click_west())
        self.south_button = tkinter.Button(self.window, text = "SOUTH", command=lambda: self.click_south())


        window.title("Frupal Test")
        window.geometry("400x300")

    def game_start(self):
        self.create_buttons()
        self.update_labels()

    def update_labels(self):
        if not self.game_over:
            self.cord_header.config(text="Current Position: ("+str(self.x_cord)+","+str(self.y_cord)+")")
            self.energy_header.config(text="Energy: "+str(self.hero.energy))
            self.whiffel_header.config(text="Whiffels: "+ str(self.hero.whiffels))

            self.cord_header.pack()
            self.energy_header.pack()
            self.whiffel_header.pack()

    def create_buttons(self):
        self.north_button.pack()
        self.east_button.pack()
        self.west_button.pack()
        self.south_button.pack()

    def click_north(self):
        self.y_cord += 1
        self.hero.energy -= 1
             
        self.check_map_edge()     
        self.check_end()
        self.update_labels()
        return
    
    def click_east(self):
        self.x_cord += 1
        self.hero.energy -= 1

        self.check_map_edge()  
        self.check_end()
        self.update_labels()
        return
    
    def click_west(self):
        self.x_cord -= 1
        self.hero.energy -= 1

        self.check_map_edge()  
        self.check_end()
        self.update_labels()
        return
    
    def click_south(self):
        self.y_cord -= 1
        self.hero.energy -= 1
    
        self.check_map_edge()  
        self.check_end()
        self.update_labels()
        return
    
    def check_map_edge(self):
        if(self.x_cord >= self.map_size_x):
            self.x_cord = self.map_size_x

        if(self.x_cord <= 0):
            self.x_cord = 0
        
        if(self.y_cord >= self.map_size_y):
            self.y_cord = self.map_size_y
        
        if(self.y_cord <= 0):
            self.y_cord = 0
        return

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


