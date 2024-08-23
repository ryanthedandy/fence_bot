import cv2
import os
import mss
import numpy as np
import pytesseract as pyt
import pyautogui as pyg
from item import Item
from PIL import Image
# areas for image grabbing and button xy for clicking
areas = {
        'inventory': {
            'left': 687,
            'top': 615,
            'width': 413,
            'height':207
        }
        ,
        'stash': {
            'left': 1322,
            'top': 2,
            'width': 598,
            'height':986
        },
        'trade_inventory1': {
            'left': 674,
            'top': 335,
            'width': 253,
            'height':279
        },
        'trade_inventory2':{
            'left': 682,
            'top': 304,
            'width': 237,
            'height':238
        },
        'trade_request': {
            'left': 839,
            'top': 465,
            'width': 237,
            'height':81
        },
        'trade_private': {
            'left': 45,
            'top': 221,
            'width': 192,
            'height':33
        },
        'trade_private2': {
            'left': 924,
            'top': 211,
            'width': 73,
            'height':27
        },
        'trade_post_inventory':{
            'left': 1132,
            'top': 623,
            'width': 416,
            'height':216
        },
        'gold_price_4':{
            'left': 1488,
            'top': 336,
            'width': 57,
            'height':43
        },
        'listings':{
            'left': 2,
            'top': 491,
            'width': 604,
            'height':583
        }

        }
buttons = {
    'start_trade':[864,620],
    'accept_trade1':[1121,684],
    'accept_trade2':[1122,624],
    'verify_items': [709,335],
    'marketplace': [1187,251],
    'my_listings': [1062,124],
    'stash_slot_1': [1314,242],
    'selling_price': [989, 623],
    'create_listing':[972,970],
    'like_to_list':[861,618],
    'transfer_all_items':[951,668]
}
item_list = {'Swords':["Arming Sword","Falchion","Longsword","Rapier","Short Sword","Viking Sword","Zweihander","Blade of Righteousness","Demon's Glee", "Divine Blade", "Divine Short Sword","Falchion Of Honor","Golden Viking Sword","Short Sword of Righteousness","Sterlin Blade","Sterling Short Sword","Void Blade"], 
                          'Maces': ["Club","Flanged Mace","Lute","Morning Star","Quarterstaff","Torch","War Hammer","War Maul","Boneshaper","Divine Rod","Divine Staff","Light Bringer","Rod of Righteousness","Staff of Righteousness","Sterling Rod","Sterling Staff","Troll's Bane"], 
                          'Daggers':["Castillon Dagger","Kris Dagger","Rondel Dagger","Stiletto Dagger","Dagger of Righteousness","Divine Dagger","Sterling Dagger","Throwing Knife",],
                          'Polearms':["Frostlight Spear","Bardiche","Halberd","Spear","Spear of Rot"],
                          'Axes': ["Battle Axe","Double Axe","Felling Axe","Hatchet","Horseman's Axe","Axe of Righteousness","Divine Axe","Francisca Axe","Golden Felling Axe", "Sterling Axe"],
                          'Bows':["Madness","Longbow","Recurve Bow","Survival Bow","Bow of Righteousness","Centaur's Madness","Divine Bow","Sterling Bow"],
                          'Crossbows':["Crossbow","Hand Crossbow","Windlass Crossbow"],
                          'Magic Stuff':["Frostlight Crystal Sword","Ceremonial Staff","Crystal Ball","Crystal Ball","Crystal Sword","Magic Staff","Spellbook","Cyclops Vision Crystal","Mana Sphere"],
                          'Shields':["Frostlight Lantern Shield","Buckler","Heater Shield","Lantern Shield","Pavise","Round Shield"],
                          'Head':["Frostlight Wizard Hat","Frostlight Norman Nasal Helm","Frostlight Hood","Frostlight Feathered Hat","Frostlight Crusader Helm","Armet","Barbuta Helm","Chapel De Fer","Chaperon","Crusader Helm","Darkgrove Hood","Elkwood Crown","Feathered Hat","Forest Hood","Gjermundbu","Great Helm","Hounskull","Kettle Hat","Leather Bonnet","Leather Cap","Norman Nasal Helm","Occultist Hood","Open Sallet","Ranger Hood","Rogue Cowl","Sallet","Shadow Hood","Shadow Mask","Spangenhelm","Straw Hat","Topfhelm","Viking Helm","Visored Barbuta Helm","Visored Sallet","Wizard Hat","Cobalt Chapel De Fer","Cobalt Hat","Cobalt Hood","Cobalt Viking Helm","Copperlight Kettle Hat","Copperlight Shadow Hood","Copperlight Straw Hat","Cowl of Darkness","Dread Hood","Golden Armet","Golden Gjermundbu","Golden Hounskull","Golden Leaf Hood","Golden Scarf","Rubysilver Barbuta Helm","Rubysilver Cap","Rubysilver Hood"],
                          'Chest':["Frostlight Warden Outfit","Frostlight Aketon","Frostlight Oracle Robe","Frostlight Abyss Plate Armor","Adventurer Tunic","Champion Armor","Crusader Armor", "Dark Cuirass","Dark Plate Armor","Darkgrove Robe","Doublet","Fine Cuirass","Frock","Grand Brigandine","Heavy Gambeson","Light Aketon","Marauder Outfit","Mystic Vestments","Northern Full Tunic","Occultist Robe","Occultist Tunic","Oracle Robe","Ornate Jazerant","Padded Tunic","Pourpoint","Regal Gambeson","Ritual Robe","Studded Leather","Templar Armor","Troubadour Outfit","Wanderer Attire","Warden Outfit","Cobalt Frock","Cobalt Regal Gambeson","Cobalt Templar Armor","Copperlight Attire","Copperlight Outfit","Copperlight Sanctum Plate Armor","Copperlight Tunic","Golden Padded Tunic","Golden Plate","Golden Robe","Robe of Darkness","Rubysilver Cuirass","Rubysilver Doublet","Rubysilver Vestments","Tri-Pelt Doublet","Tri-Pelt Northern Full Tunic"],
                          'Legs':["Frostlight Trousers","Frostlight Plate Pants","Frostlight Leather Leggings","Trolls Bane","Brave Hunter","Bardic Pants","Cloth Pants","Copperlight Leggings","Dark Leather Leggings","Heavy Leather Leggings","Leather Chausses","Leather Leggings","Loose Trousers","Occultist Pants","Padded Leggings","Plate Pants","Brave Hunter's Pants","Cobalt Plate Pants","Cobalt Trousers","Copperlight Plate Pants","Demonclad Leggings","Golden Chausses","Golden Leggings","Golden Plate Pants","Rubysilver Leggings","Rubysilver Plate Pants","Wolf Hunter Leggings"],
                          'Hands':["Frostlight Runestone Gloves","Frostlight Mystic Gloves","Frostlight Gauntlets","Elkwood Gloves","Gloves of Utility","Heavy Gauntlets","Leather Gloves","Light Gauntlets","Mystic Gloves","Rawhide Gloves","Reinforced Gloves","Riveted Gloves","Runestone Gloves","Cobalt Heavy Gauntlet","Cobalt Leather Gloves","Copperlight Gauntlets","Copperlight Riveted Gloves","Demon Grip Gloves","Golden Gauntlets","Golden Gloves","Gravewolf Gloves","Rubysilver Gauntlets","Rubysilver Rawhide Gloves"],
                          'Foot':["Darkleaf Boots","Frostlight Rugged Boots","Frostlight Plate Boots","Frostlight Lightfoot Boots","Adventurer Boots","Buckled Boots","Darkleaf Boots","Dashing Boots","Forest Boots","Heavy Boots","Laced Turnshoe","Lightfoot Boots","Low Boots","Occultist Boots","Old Shoes","Plate Boots","Rugged Boots","Stitched Turnshoe","Turnshoe","Wizard Shoes","Cobalt Lightfoot Boots","Cobalt Plate Boots","Copperlight Lightfoot Boots","Copperlight Plate Boots","Foul Boots","Golden Boots","Golden Plate Boots","Rubysilver Adventurer Boots","Rubysilver Plate Boots","Shoes of Darkness"],
                          'Back':["Frostlight Cloak","Adventurer Cloak","Mercurial Cloak","Radiant Cloak","Splendid Cloak","Tattered Cloak","Vigilant Cloak","Watchman Cloak", "Cloak of Darkness","Golden Cloak"],
                          'Pendant':["Badger Pendant","Bear Pendant","Fangs of Death Necklace","Fox Pendant","Frost Amulet","Monkey Pendant","Necklace of Peace","Owl Pendant","Ox Pendant","Phoenix Choker","Rat Pendant","Torq of Soul","Wind Locket"],
                          'Ring':["Grimsmile Ring","Ring of Courage","Ring of Finesse","Ring of Quickness","Ring of Resolve","Ring of Survival","Ring of Vitality","Ring of Wisdom"],
                          'Drink':["Troll's Blood"],
                          'Consumable':["Frozen Iron Key","Golden Key","Mystical Gem","Old Rusty Key","Skull Key","Surgical Kit"],
                          'Mining':["Pickaxe"],
                          'Hunting Loot':["Wolf Pelt","Beetle Wings","Blue Eyeballs","Bug Shell","Captured Mana Flakes","Centaur Hoof","Centaur Tail","Centaur Horn","Cockatrice's Lucky Feather","Cursed Crown","Cyclops Eye","Cyclops's Club","Cyclops Rags","Dark Matter","Demon Blood","Demon Dog Thorn","Dog Collar","Enchanted Dark Fabric","Extra Thick Pelts","Firefly's Abdomen","Frost Wyvern Egg","Frost Wyvern's Claws","Frozen Heart","Ghostly Essence","Giant Toe","Glowing Blue Ice Eyes","Token Of Honor","Spider Silk","Troll Pelt","Torn Bat Wing","Troll's Club","Volcanic Ash","Warlord's Broken Sword Blade","Yeti's Teeth"],
                          'Ore':["Cobalt Ore","Copper Ore","Froststone Ore","Gold Ore","Iron Ore","Rubysilver Ore"],
                          'Ingots':["Cobalt Ingot","Copper Ingot","Froststone Ingot","Gold Ingot","Iron Ingot","Rubysilver Ingot","Silver Ingot"],
                          'Powder':["Cobalt Powder","Copper Powder","Froststone Powder","Gold Powder","Iron Powder","Rubysilver Powder","Silver Powder"],
                          'Containers':["Gold Coin Bag","Gold Coin Chest"],
                          'Herb':["Lifeleaf","Phantom Flower","Wardweed"]}
rarity_list = ["Uncommon", "Rare", "Epic", "Legendary"]
attribute_list = ["True Magical Damage","True Physical Damage","Magical Healing","Move Speed Bonus","Magical Damage Bonus","Additional Movement Speed","Additional Magical Damage","Additional Physical Damage","Physical Power","Magical Power"]
crafted_list = ["Cobalt","Copperlight","Frostlight","Golden","Rubysilver"]
item_history =  'src/item_history'
items_we_own = []
debuggin = False
#pytess location, will need to add better pathing for moving program to different PC
pyt.pytesseract.tesseract_cmd = "C:/Users/ryanx/Desktop/Projects/PythonGoblinTools/src/Tesseract-OCR/tesseract.exe"

# FIND COORDS OF ITEMS INSIDE OF IMAGE
def get_item_coords(image, extracting_item_panel=False, checking_listings=False):
    # this is the path of the item images. Will need to adjust in the future to move to a different PC
    if extracting_item_panel:
        folder_path = 'src/item_panel'
    elif checking_listings:
        folder_path = 'src/trade_alert'
    else:
        folder_path = 'src/items'
    inventory_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    rectangles = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path,filename)
        # Load inventory image and item template
        template = cv2.imread(file_path, cv2.IMREAD_COLOR)
        template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

        # heatmap of match
        try:
            result = cv2.matchTemplate(inventory_gray, template_gray, cv2.TM_CCOEFF_NORMED)
        except cv2.error as e:
            print(f"Error matching template for {filename}: {str(e)}")
            continue

        # height and width of the template item
        h = template_gray.shape[0]
        w = template_gray.shape[1]
        if(extracting_item_panel):
            h += 470
            w += 30
        # ADJUST THIS NUMBER FOR TESTING
        thresh = .81

        # generate locations using numpy and check against threshold
        yloc,xloc = np.where(result >= thresh)
        


        # use a grouping function to eliminate the duplicate coords
        for (x,y) in zip(xloc, yloc):
            if(extracting_item_panel):
                rectangles.append([int(x-15), int(y-290), int(w), int(h)])
                rectangles.append([int(x-15), int(y-290), int(w), int(h)])
            elif(checking_listings):
                rectangles.append([int(x), int(y), int(w+400), int(h)])
                rectangles.append([int(x), int(y), int(w+400), int(h)])
            else:
                rectangles.append([int(x), int(y), int(w), int(h)])
                rectangles.append([int(x), int(y), int(w), int(h)])
        
    
    grouped_rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)

    # Draw rectangles on the inventory image for testing
    for (x, y, w, h) in grouped_rectangles:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # uncomment for more testing
    if(debuggin):
        cv2.imshow('Detected Items', image) 
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return grouped_rectangles

# GRAB SCREENSHOT OF AREA
def capture_area(area):
    with mss.mss() as screenshot:
        return np.array(screenshot.grab(area))

# FIND TEXT OF IMAGE
def extract_menu_text(image, number_text=False):
    if number_text:
        text = pyt.image_to_string(image,config="--psm 6 digits")
    else:
        text = pyt.image_to_string(image)
    if(number_text):
        print(text)
        cleaned_text = ''.join(c for c in text if c.isdigit())
        return cleaned_text

    lines = text.split('\n')
    return ' '.join(lines)

# read the item list into memory
def read_file_to_memory(file_path):
    with open(file_path) as file:
        content = file.read()
    return content

# find the items, extract their information and store it in ITEM object
def extract_item(image):
    #bro we going to take the image of 
    coords = get_item_coords(image,extracting_item_panel=True)
    try:
        x,y,w,h = coords[0]
    except:
        print("No coordinates available, item panel probably not detected")
        return
    
    # Convert OpenCV image (BGR) to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Convert to PIL Image and crop that hoe
    image_pil = Image.fromarray(image_rgb)
    cropped = image_pil.crop((x, y, x+w, y+h))
    
    # convert back to cv cause why not add more complexity to this bs
    cropped_image = cv2.cvtColor(np.array(cropped), cv2.COLOR_RGB2BGR)
    item_text = extract_menu_text(cropped_image)
    alternate_text = extract_menu_text(image)

    extracted_item = Item()
    if(debuggin):
        cv2.imshow('cum',cropped_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        print(item_text)
    # Find item name
    for key,items in item_list.items():
        for name in items:
            if name.lower() in item_text.lower():
                extracted_item.name = name
    # Find Item name 2
    if extracted_item.name == None:
        for key,items in item_list.items():
            for name in items:
                if name.lower() in alternate_text.lower():
                    extracted_item.name = name

    # Find item crafted variants
    for key,items in item_list.items():
        for item in items:
            for material in crafted_list:
                if item.lower() == (material.lower() + " " + extracted_item.name.lower()):
                    extracted_item.crafted_variants += 1
              
    # Find rarity
    for rarity in rarity_list:
        if rarity.lower() in item_text.lower():
            extracted_item.rarity = rarity
    
    # Find rarity 2
    if extracted_item.rarity == None:
        for rarity in rarity_list:
            if rarity.lower() in alternate_text.lower():
                extracted_item.rarity = rarity


    # Find attributes
    for attribute in attribute_list:
        if attribute.lower() in item_text.lower() and attribute not in extracted_item.attributes:
            extracted_item.attributes.append(attribute)
    
    return  extracted_item

# ding price of item
def price_check(item):
    buttons = {
            'market': [866,120],
            'reset':[1794,206],
            'item': [133,207],
            'item_entry':[113,240],
            'item_selection':[109,277],
            'rarity':[368,205],
            'rarity_entry':[319,244],
            'rarity_selection':[299,286],
            'attribute':[1532,208],
            'search':[1791,278],

        }
    craft_buffer = 30

    if(item == None):
        print("no item to check")
        return
    # check if item is in the inventory area, then check if nothing was detected.
    if item.name == None and item.rarity == None:
        print("ERROR: Item Name and Rarity Not Detected")
        return
        
    if item.name == None:
        print("NAME NOT DETECTED, if this persists ask Ryan for help")
        return   
        
    # I ordered the buttons in the order that the bot should click, then write when the location is appropriate
    for location in buttons.keys():
        if location == 'item_selection':
            copy = buttons[location].copy()
            copy[1] += craft_buffer * item.crafted_variants
            pyg.moveTo(copy, duration=.1)
  
        else:
            pyg.moveTo(buttons[location], duration=.1)
        pyg.sleep(.3)
        pyg.click()
        match location:
            case 'item_entry':
                try:
                    pyg.write(item.name)
                except:
                    break
            case 'rarity_entry':
                try:
                    pyg.write(item.rarity)
                except:
                    pyg.write("epic")
                    continue
            case 'attribute':
                # enter_attributes(item.attributes)
                pass
    
    pyg.sleep(1)
    price_image = capture_area(areas["gold_price_4"])          
    price_text = extract_menu_text(price_image, number_text=True)
    if(debuggin):
        print(price_text)
        cv2.imshow('hello', price_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    try:
        price = int(price_text)
    except:
        print("price failed")
        price = 0
    return price - 1
# AWAIT AND DETECT TRADE, THEN COMPLETE TRADE IN TRADING POST
def trade():
    text = ''

    # wait for trade request to come in
    while 'trade' not in text:
        image = capture_area(areas['trade_request'])
        text = extract_menu_text(image)
        pyg.sleep(1)
    # start trading
    print("TRADE STARTING")
    pyg.moveTo(buttons['start_trade'])
    pyg.click()
    # wait for user to put in items and type in 'done'
    while 'done' not in text:
        image = capture_area(areas['trade_private'])
        text = extract_menu_text(image)
        pyg.sleep(1)
    # done is entered and now we are going to trade phase 2
    print("ITEMS CONFIRMED")
    pyg.moveTo(buttons['accept_trade1'])
    pyg.click()
    # check if we are on the phase 2 screen
    while 'final' not in text:
        image = capture_area(areas['trade_private2'])
        text = extract_menu_text(image)
        pyg.sleep(1)
    # now we click all items in the trade menu so we can finish trade
    x = buttons['verify_items'][0]
    y = buttons['verify_items'][1]
    for i in range(5):
        for j in range(5):
            pyg.moveTo(x + (i * 44),y + (j * 44),.1)
            pyg.click()

    pyg.moveTo(buttons['accept_trade2'])
    pyg.click()
    pyg.sleep(5)
    print("TRADE SUCCESS")
    # trade completed, now we find coords of items in inventory and move them into stash
    image = capture_area(areas['trade_post_inventory'])
    coords = get_item_coords(image)


    for (x, y, w, h) in coords:
        pyg.moveTo(x + areas['trade_post_inventory']['left'] + 20, y + areas['trade_post_inventory']['top'] + 20)
        pyg.keyDown('shiftleft')
        pyg.keyDown('shiftright')
        pyg.rightClick()
        pyg.keyUp('shiftleft')
        pyg.keyUp('shiftright')
    
    #navigate to marketplace
    pyg.keyDown('esc')
    pyg.keyUp('esc')
    pyg.moveTo(buttons['start_trade'])
    pyg.click()
    pyg.moveTo(buttons['marketplace'])
    pyg.click()
    pyg.moveTo(buttons['my_listings'])
    pyg.click()
    pyg.moveTo(buttons['stash_slot_1'])
    pyg.click()

    print("NOW EXECUTE LISTING FUNCTION")

def check_listings():
    image = capture_area(areas['listings'])
    coords = get_item_coords(image,checking_listings=True)
    if len(coords) == 0:
        print("no listings found")
        return 
    for coordinate in coords[::-1]:
        x,y,w,h = coordinate
        slot = round(y / 50)
        print(f" Clearing the listing at slot {slot} ")
        pyg.moveTo(x+29,y+490)
        pyg.click()
        pyg.moveTo(buttons["transfer_all_items"])
        pyg.click()
        
# ITEMS ARE IN THE STASH, WE MUST PRICE CHECK AND LIST THEM       
def list_items():
    image = capture_area(areas['stash'])
    coords = get_item_coords(image)
    print(coords)

    for (x,y,w,h) in coords:
        print('we moving')
        pyg.moveTo((x + 20) + areas['stash']['left'],(y + 20) + areas['stash']['top'])
        image = capture_area(areas['stash'])
        item = extract_item(image)
        if item != None:
            item.price = price_check(item)
            if item.price > 1:
                pyg.moveTo(buttons["my_listings"])
                pyg.click()
                pyg.sleep(1)
                pyg.moveTo(x + areas['stash']['left'] + 15,y + areas['stash']['top'] + 16)
                pyg.click()
                pyg.moveTo(buttons['selling_price'])
                pyg.click()
                pyg.write(str(item.price))
                pyg.moveTo(buttons["create_listing"])
                pyg.click()
                if debuggin:
                    cv2.waitKey()
                pyg.moveTo(buttons['like_to_list'])
                pyg.click()

            else:
                print("price was not detected :(")
        else:
            print("Item skipped due to non-detection")
# MAIN PROGRAM LOGIC YO
def main():
    trade()
    list_items()
    check_listings()
# RUN
main()


# important bugs to fix:
        # Dex rings lmao?? not detecting panel
# 