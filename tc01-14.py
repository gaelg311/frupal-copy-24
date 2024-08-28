import pytest
import tkinter as tk
from gamestate import game_logic

@pytest.fixture
def setup_frupal():
    root = tk.Tk()
    game = game_logic(root,file=r"map_files/#map for test plan.txt")
    game.game_start()

    yield game

    # Cleanup after test runs
    root.quit()
    root.update()

def test_case_1(setup_frupal):
    game = setup_frupal

    for i in range(11): game.click_east()
    for i in range(11): game.click_north()

    assert game.hero.energy == 478
    assert game.hero.whiffles == 1000
    assert game.x_cord == 11
    assert game.y_cord == 11 # (0,0) is (1,1) in list indexing
    assert game.diamond_cords == "(11,11)"
    assert game.hero.inventory == ["Rock"]
    assert game.game_over

def test_case_2(setup_frupal):
    game = setup_frupal

    for i in range(3): game.click_north()

    assert game.hero.energy == 495
    assert game.hero.whiffles == 1000
    assert game.x_cord == 0
    assert game.y_cord == 3
    assert game.diamond_cords == "(11,11)"
    assert game.hero.inventory == ["Rock"]

def test_case_3(setup_frupal):
    game = setup_frupal

    assert hasattr(game, "label_grid")

def test_case_4(setup_frupal):
    game = setup_frupal

    for i in range(2): game.click_east()
    for i in range(3): game.click_north()
    game.yes_button.invoke()

    assert game.hero.energy == 515
    assert game.hero.whiffles == 999
    assert game.x_cord == 2
    assert game.y_cord == 3
    assert game.diamond_cords == "(11,11)"
    assert game.hero.inventory == ["Rock"]

def test_case_5(setup_frupal):
    game = setup_frupal

    for i in range(1): game.click_east()
    for i in range(3): game.click_north()

    assert game.hero.energy == 486
    assert game.hero.whiffles == 1000
    assert game.x_cord == 1
    assert game.y_cord == 3
    assert game.diamond_cords == "(11,11)"

def test_case_6(setup_frupal):
    game = setup_frupal

    for i in range(4): game.click_east()
    for i in range(3): game.click_north()
    
    assert game.yes_button

    game.yes_button.invoke()
    game.show_inventory()

    assert game.hero.energy == 493
    assert game.hero.whiffles == 975
    assert game.x_cord == 4
    assert game.y_cord == 3
    assert game.diamond_cords == "(11,11)"
    assert game.hero.inventory == ["Rock"]

def test_case_7(setup_frupal):
    game = setup_frupal

    for i in range(1): game.click_east()
    for i in range(6): game.click_north()
    
    assert game.yes_button

    game.yes_button.invoke()

    assert game.hero.energy == 493
    assert game.hero.whiffles == 1100
    assert game.x_cord == 1
    assert game.y_cord == 6
    assert game.diamond_cords == "(11,11)"
    assert game.hero.inventory == ["Rock"]

def test_case_8(setup_frupal):
    game = setup_frupal

    for i in range(2): game.click_east()
    for i in range(6): game.click_north()
    
    assert game.yes_button

    game.yes_button.invoke()

    assert game.hero.energy == 492
    assert game.hero.whiffles == 900
    assert game.x_cord == 2
    assert game.y_cord == 6
    assert game.diamond_cords == "(11,11)"
    assert game.hero.inventory == ["Rock"]

def test_case_9(setup_frupal):
    game = setup_frupal

    for i in range(4): game.click_east()
    for i in range(6): game.click_north()
    
    assert game.hero.energy == 490
    assert game.hero.whiffles == 1000
    assert game.x_cord == 4
    assert game.y_cord == 5
    assert game.diamond_cords == "(11,11)"
    assert game.hero.inventory == ["Rock"]

def test_case_10(setup_frupal):
    game = setup_frupal
    game.hero.inventory = ["Boat"]

    for i in range(4): game.click_east()
    for i in range(8): game.click_north()
    
    assert game.hero.energy == 491
    assert game.hero.whiffles == 1000
    assert game.x_cord == 4
    assert game.y_cord == 8
    assert game.diamond_cords == "(11,11)"
    assert game.hero.inventory == ["Boat"]

def test_case_11(setup_frupal):
    game = setup_frupal
    game.hero.energy = 10

    for i in range(10): game.click_east()
    
    assert game.hero.energy == 0
    assert game.hero.whiffles == 1000
    assert game.x_cord == 10
    assert game.y_cord == 0
    assert game.diamond_cords == "(11,11)"
    assert game.hero.inventory == ["Rock"]

    assert game.game_over

def test_case_12(setup_frupal):
    game = setup_frupal
    game.hero.inventory = ["Axe"]

    for i in range(1): game.click_east()
    for i in range(3): game.click_north()

    game.use_button.invoke()
    game.show_inventory()
    
    assert game.hero.energy == 490
    assert game.hero.whiffles == 1000
    assert game.x_cord == 1
    assert game.y_cord == 3
    assert game.diamond_cords == "(11,11)"
    assert game.hero.inventory == []

def test_case_13(setup_frupal):
    game = setup_frupal
    game.hero.inventory = ["Axe"]

    for i in range(3): game.click_east()
    for i in range(3): game.click_north()

    game.yes_button.invoke()
    game.show_inventory()
    
    assert game.hero.energy == 494
    assert game.hero.whiffles == 965
    assert game.x_cord == 3
    assert game.y_cord == 3
    assert game.diamond_cords == "(11,11)"
    assert game.hero.inventory == ["Axe", "Shears"]

def test_case_14(setup_frupal):
    game = setup_frupal
    game.hero.inventory = ["Axe","Boat","Chisel"]

    game.show_inventory()
    
    assert game.hero.energy == 500
    assert game.hero.whiffles == 1000
    assert game.x_cord == 0
    assert game.y_cord == 0
    assert game.diamond_cords == "(11,11)"
    assert game.hero.inventory == ["Axe", "Boat", "Chisel"]

    assert game.inventory_visibility
    assert game.inventory_frame

    game.window.update_idletasks()
    items = game.inventory_frame.winfo_children()[0].winfo_children()#[0].winfo_children()
    assert game.inventory_button.cget("text") == "Hide Inventory"