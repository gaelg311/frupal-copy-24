# === HEADER ===
# @name     pn.py
# @author   Pouya Nouri
# @date     07/24/2024
# @version  07/27/2024
# === HEADER ===

import random

def manhattan_distance(src:int,trg:int) -> int:
    '''Calculates the shortest manhattan route between two points.
    
    param:
        @src: coordinate of the source of comparison.
        @trg: coordinate of the target of comparison.
        
    returns
        shortest route length
    
    example usage:
        >>> manhattan_distance((0,0),(1,2))
        3
    '''
    return abs(src[0]-trg[0]) + abs(src[1]-trg[1])

def random_map_generator(terr_weights:dict={0:.35,1:.25,2:.2,3:.05,4:.1,5:.1},x_size:int=25,y_size=25,file=None) -> list:
    '''Generates a terrain, sprite, and visibility starting map for the FRUPAL project. Includes the starting placement of the Hero and the Diamonds. Writes the information to a file.
    
    param:
        @terr_weights: probability weights of different terrains being generated
        @x_size: the x-axis length of the map
        @y_size: the y-axis length of the map
        @file: the file to write the maps to
        
    returns
        @terr_map: generated terrain map
        @sprt_map: generated sprite map
        @vsib_map: generated visibility map
    
    example usage:
        >>> random_map_generator(x_size=4,y_size=4,file=foo.txt)
        >>> cat foo.txt
            """TERRAIN=
            4212
            1300
            0412
            2001
            SPRITE=
            ....
            @...
            ....
            ..*.
            VISIBILITY=
            1000
            1100
            1000
            0000
            """
    '''

    prob_dens:float = 0
    for key in terr_weights.keys():
        if prob_dens > terr_weights[key]: terr_weights[key] += prob_dens
        prob_dens = terr_weights[key]

    terr_map:str = ""
    sprt_map:str = ""
    vsib_map:str = ""

    for row in range(y_size):
        for col in range(x_size):

            # Terrain Generation
            rand_tile = random.random()
            for key in terr_weights.keys():
                if rand_tile < terr_weights[key]: 
                    terr_map += str(key)
                    break

            # Sprite Generation
            sprt_map += "."

            # Visibility Generation
            vsib_map += "0"

        terr_map += "\n"
        sprt_map += "\n"
        vsib_map += "\n"

    # Determine Hero Starting Point
    hero_loc:set = (-1,-1)
    while hero_loc == (-1,-1):
        x, y = random.randint(0,x_size-1), random.randint(0,y_size-1)
        #print((x,y),x+y*x_size,len(sprt_map))
        if terr_map[x + y * (x_size+1)] not in ["2","3","\n"]:
            hero_loc = (y,x)
            sprt_map = sprt_map[:x + y * (x_size+1)] + "@" + sprt_map[x + y * (x_size+1) + 1:]

    # Update Visibility Layer
    y, x = hero_loc[0], hero_loc[1]
    vsib_map = vsib_map[:x + y * (x_size+1)] + "1" + vsib_map[x + y * (x_size+1) + 1:]
    if x > 0: vsib_map = vsib_map[:x-1 + y * (x_size+1)] + "1" + vsib_map[x-1 + y * (x_size+1) + 1:]
    if x < x_size-1: vsib_map = vsib_map[:x+1 + y * (x_size+1)] + "1" + vsib_map[x+1 + y * (x_size+1) + 1:]
    if y > 0: vsib_map = vsib_map[:x + (y-1) * (x_size+1)] + "1" + vsib_map[x + (y-1) * (x_size+1) + 1:]
    if y < y_size-1: vsib_map = vsib_map[:x + (y+1) * (x_size+1)] + "1" + vsib_map[x + (y+1) * (x_size+1) + 1:]
    
    # Determine Diamonds Point
    dmnd_loc:set = (-1,-1)
    while dmnd_loc == (-1,-1):
        x, y = random.randint(0,x_size-1), random.randint(0,y_size-1)
        #print(manhattan_distance(hero_loc,(y,x)))
        if x >= 0 and x < x_size and y >= 0 and y < y_size and manhattan_distance(hero_loc,(y,x)) > max(x_size,y_size)//2+1:
            dmnd_loc = (y,x)
            sprt_map = sprt_map[:x + y * (x_size+1)] + "*" + sprt_map[x + y * (x_size+1) + 1:]

    # Write To File, if applicable
    if file:
        with open(file, 'w') as f:
            f.write("# KEY: (0=meadow, 1=forest, 2=water,3=wall, 4=bog, 5=swamp)\n")
            f.write("TERRAIN=\n"+terr_map)
            f.write("\n# KEY: (.=none, @=hero)\n")
            f.write("SPRITE=\n"+sprt_map)
            f.write("\n# KEY: (0=not visible, 1=visible)\n")
            f.write("VISIBILITY=\n"+vsib_map)
            f.close()
    
    return terr_map, sprt_map, vsib_map

def setup_config(energy:int,whiff:int,file,*args) -> bool:
    '''Writes FRUPAL setup configurations into a setup file.
    
    param:
        @energy: the starting energy for the hero
        @whiff: the starting whiff for the hero
        *args: items meant to be carried by the hero
        
    returns
        true if file was written, otherwise false
    
    example usage:
        >>> setup_config(100,1000,foo.txt,item1,item2,item3)
        True
        >>> cat foo.txt
            """START_ENERGY=100
            START_WHIFF=1000
            INVENTORY=Item 1, Item 2, Item 3
            """
    '''
    if not file or energy < 0 or whiff < 0:
        return False
    
    with open(file,"w") as f:
        f.write(f"START_ENERGY={energy}\n")
        f.write(f"START_WHIFF={whiff}\n")
        f.write(f"INVENTORY=" + ", ".join(args)+"\n")

    return True

# Example usage
random_map_generator(x_size=20,y_size=20,file="MAP.txt")
setup_config(100,1000,"SETUP.txt","Item 1","Item 2","Item 3")

# Next order of business will be to create the load_map function!