import cv2
import os
import mss
import json
import re
import numpy as np
import pytesseract as pyt
import pyautogui as pyg
from item import Item
from PIL import Image
from datetime import datetime, timedelta

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
            'width': 250,
            'height':81
        },
        'trade_private': {
            'left': 54,
            'top': 213,
            'width': 390,
            'height':60
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
        },
        'at_trade_post':{
            'left': 896,
            'top': 12,
            'width': 126,
            'height':56
        }

        }
buttons = {
    'start_trade':[864,620],
    'accept_trade1':[1121,684],
    'accept_trade2':[1122,624],
    'verify_items': [709,335],
    'marketplace': [1187,251],
    'my_listings': [1062,92],
    'stash_slot_1': [1314,242],
    'selling_price': [989, 623],
    'create_listing':[972,970],
    'like_to_list':[861,618],
    'transfer_all_items':[951,668],
    'trade_post': [1187,365]
}
item_list = {'Swords':["Arming Sword","Falchion","Longsword","Rapier","Short Sword","Viking Sword","Zweihander","Blade of Righteousness","Demon's Glee", "Divine Blade", "Divine Short Sword","Falchion Of Honor","Golden Viking Sword","Short Sword of Righteousness","Sterlin Blade","Sterling Short Sword","Void Blade"], 
                          'Maces': ["Club","Flanged Mace","Lute","Morning Star","Quarterstaff","Torch","War Hammer","War Maul","Boneshaper","Divine Rod","Divine Staff","Light Bringer","Rod of Righteousness","Staff of Righteousness","Sterling Rod","Sterling Staff","Troll's Bane"], 
                          'Daggers':["Castillon Dagger","Kris Dagger","Rondel Dagger","Stiletto Dagger","Dagger of Righteousness","Divine Dagger","Sterling Dagger","Throwing Knife",],
                          'Polearms':["Frostlight Spear","Bardiche","Halberd","Spear","Spear of Rot"],
                          'Axes': ["Battle Axe","Double Axe","Felling Axe","Hatchet","Horseman's Axe","Axe of Righteousness","Divine Axe","Francisca Axe","Golden Felling Axe", "Sterling Axe"],
                          'Bows':["Madness","Longbow","Recurve Bow","Survival Bow","Bow of Righteousness","Centaur's Madness","Divine Bow","Sterling Bow"],
                          'Crossbows':["Hand Crossbow","Windlass Crossbow","Crossbow"],
                          'Magic Stuff':["Frostlight Crystal Sword","Ceremonial Staff","Crystal Ball","Crystal Ball","Crystal Sword","Magic Staff","Spellbook","Cyclops Vision Crystal","Mana Sphere"],
                          'Shields':["Frostlight Lantern Shield","Buckler","Heater Shield","Lantern Shield","Pavise","Round Shield"],
                          'Head':["Frostlight Wizard Hat","Frostlight Norman Nasal Helm","Frostlight Hood","Frostlight Feathered Hat","Frostlight Crusader Helm","Armet","Barbuta Helm","Chapel De Fer","Chaperon","Crusader Helm","Darkgrove Hood","Elkwood Crown","Feathered Hat","Forest Hood","Gjermundbu","Great Helm","Hounskull","Kettle Hat","Leather Bonnet","Leather Cap","Norman Nasal Helm","Occultist Hood","Open Sallet","Ranger Hood","Rogue Cowl","Sallet","Shadow Hood","Shadow Mask","Spangenhelm","Straw Hat","Topfhelm","Viking Helm","Visored Barbuta Helm","Visored Sallet","Wizard Hat","Cobalt Chapel De Fer","Cobalt Hat","Cobalt Hood","Cobalt Viking Helm","Copperlight Kettle Hat","Copperlight Shadow Hood","Copperlight Straw Hat","Cowl of Darkness","Dread Hood","Golden Armet","Golden Gjermundbu","Golden Hounskull","Golden Leaf Hood","Golden Scarf","Rubysilver Barbuta Helm","Rubysilver Cap","Rubysilver Hood"],
                          'Chest':["Frostlight Warden Outfit","Frostlight Aketon","Frostlight Oracle Robe","Frostlight Abyss Plate Armor","Adventurer Tunic","Champion Armor","Crusader Armor", "Dark Cuirass","Dark Plate Armor","Darkgrove Robe","Doublet","Fine Cuirass","Frock","Grand Brigandine","Heavy Gambeson","Light Aketon","Marauder Outfit","Mystic Vestments","Northern Full Tunic","Occultist Robe","Occultist Tunic","Oracle Robe","Ornate Jazerant","Padded Tunic","Pourpoint","Regal Gambeson","Ritual Robe","Studded Leather","Templar Armor","Troubadour Outfit","Wanderer Attire","Warden Outfit","Cobalt Frock","Cobalt Regal Gambeson","Cobalt Templar Armor","Copperlight Attire","Copperlight Outfit","Copperlight Sanctum Plate Armor","Copperlight Tunic","Golden Padded Tunic","Golden Plate","Golden Robe","Robe of Darkness","Rubysilver Cuirass","Rubysilver Doublet","Rubysilver Vestments","Tri-Pelt Doublet","Tri-Pelt Northern Full Tunic"],
                          'Legs':["Frostlight Trousers","Frostlight Plate Pants","Frostlight Leather Leggings","Trolls Bane","Brave Hunter","Bardic Pants","Cloth Pants","Copperlight Leggings","Dark Leather Leggings","Heavy Leather Leggings","Leather Chausses","Leather Leggings","Loose Trousers","Occultist Pants","Padded Leggings","Plate Pants","Brave Hunter's Pants","Cobalt Plate Pants","Cobalt Trousers","Copperlight Plate Pants","Demonclad Leggings","Golden Chausses","Golden Leggings","Golden Plate Pants","Rubysilver Leggings","Rubysilver Plate Pants","Wolf Hunter Leggings"],
                          'Hands':["Frostlight Riveted Gloves","Frostlight Runestone Gloves","Frostlight Mystic Gloves","Frostlight Gauntlets","Elkwood Gloves","Gloves of Utility","Heavy Gauntlets","Leather Gloves","Light Gauntlets","Mystic Gloves","Rawhide Gloves","Reinforced Gloves","Riveted Gloves","Runestone Gloves","Cobalt Heavy Gauntlet","Cobalt Leather Gloves","Copperlight Gauntlets","Copperlight Riveted Gloves","Demon Grip Gloves","Golden Gauntlets","Golden Gloves","Gravewolf Gloves","Rubysilver Gauntlets","Rubysilver Rawhide Gloves"],
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
attribute_list = ["True Magical Damage","True Physical Damage","Magical Healing","Move Speed Bonus","Magical Damage Bonus","Additional Move Speed","Additional Magical Damage","Additional Physical Damage","Physical Power","Magical Power","Knowledge","Strength","Agility","Vigor","Dexterity","Max Health", "Max Health Bonus"]
crafted_list = ["Cobalt","Copperlight","Frostlight", "Rubysilver", "Golden"]
item_history =  'src/item_history'
item_listings = []
sold_items = []
debuggin = True
debuggin_price_only = False
testing_trade = True
#pytess location, will need to add better pathing for moving program to different PC
pyt.pytesseract.tesseract_cmd = "C:/Users/ryanx/Desktop/Projects/PythonGoblinTools/src/Tesseract-OCR/tesseract.exe"

# save items to JSON
def save_items(items,filename):
    with open(filename, 'w') as f:
        json.dump([item.to_json() for item in items], f, indent=2)

# load items from json
def load_items(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return [Item.from_json(item_data) for item_data in data]

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
            h += 520
            w += 30
        # ADJUST THIS NUMBER FOR TESTING
        thresh = .81

        # generate locations using numpy and check against threshold
        yloc,xloc = np.where(result >= thresh)
        


        # use a grouping function to eliminate the duplicate coords
        for (x,y) in zip(xloc, yloc):
            if(extracting_item_panel):
                rectangles.append([int(x-15), int(y-340), int(w), int(h)])
                rectangles.append([int(x-15), int(y-340), int(w), int(h)])
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

# find the crafting buffer in the view market tab
def find_craft_buffer(name,variants):
    sorted_variants = sorted(variants, key=str.lower)
    print(f"HERE IS THE SORTED LIST:  {sorted_variants}")
    return sorted_variants.index(name)

# find the items, extract their information and store it in ITEM object
def extract_item(image):
    crafted_variants_of_item = []
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
    item_text = ' ' + extract_menu_text(cropped_image)
    alternate_text = ' ' + extract_menu_text(image)

    extracted_item = Item()
    if(debuggin):
        cv2.imshow('cum',cropped_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        print(item_text)
    
    # Find item name
    for key,items in item_list.items():
        for name in items:
            if ' ' + name.lower() + ' ' in item_text.lower():
                extracted_item.name = name
                print(f"HERE IS THE {name}")
                crafted_variants_of_item.append(extracted_item.name)
                break
                
    
    # Find Item name backup if the first one fails
    if extracted_item.name == None:
        for key,items in item_list.items():
            for name in items:
                if name.lower() in alternate_text.lower():
                    extracted_item.name = name
                    crafted_variants_of_item.append(extracted_item.name)
                    break
    
    if extracted_item.name == None:
        return None
    # Find item crafted variants
    for key,items in item_list.items():
        for item in items:
            for material in crafted_list:
                if item.lower() == (f"{material.lower()} {extracted_item.name.lower()}"):
                    extracted_item.crafted_variants += 1
                    crafted_variants_of_item.append(f'{material.lower()} {extracted_item.name.lower()}')
    
    if extracted_item.name == 'Ox Pendant':
        crafted_variants_of_item.append('Fox Pendant')
    elif extracted_item.name =='Turnshoe':
        crafted_variants_of_item.append('Stitched Turnshoe')
        crafted_variants_of_item.append('Laced Turnshoe')
    extracted_item.craft_buffer = find_craft_buffer(extracted_item.name,crafted_variants_of_item)
    
   


    # extract the attributes by blue
    attribute_text = extract_attributes(cropped_image,(93,66,0))

     # Find rarity
    for rarity in rarity_list:
        if rarity.lower() in attribute_text.lower():
            extracted_item.rarity = rarity
    
    # Find rarity BACKUP
    if extracted_item.rarity == None:
        for rarity in rarity_list:
            if rarity.lower() in alternate_text.lower():
                extracted_item.rarity = rarity
    
    if debuggin:
        print(f"printing extracted blue text:    {attribute_text}")

    # Find attributes
    extracted_item.attributes = match_attributes(attribute_text, attribute_list)
    print(extracted_item.attributes)
    return  extracted_item

# ding price of item
def price_check(item):
    buttons = {
            'view_market': [866,92],
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
            copy[1] += craft_buffer * item.craft_buffer
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
                enter_attributes(item.attributes)
                pass
    
    pyg.sleep(1)
    price_image = capture_area(areas["gold_price_4"])          
    price_text = extract_attributes(price_image,(0,212,255),is_price=True)
    if(debuggin or debuggin_price_only):
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
    start_time = datetime.now()
    try:
        # wait for trade request to come in
        while 'trade' not in text:
            image = capture_area(areas['trade_request'])
            text = extract_menu_text(image)
            if debuggin:
                print(text)
            end_time = datetime.now()
            time_difference = end_time - start_time
            if time_difference >= timedelta(minutes=1):
                return '0'
            try:
                token_text = text.split(' ')
                username = token_text[0]
            except: 
                continue
            
            pyg.sleep(1)
        # start trading
        print("TRADE STARTING")
        pyg.sleep(5)
        pyg.moveTo(buttons['start_trade'])
        pyg.click()
        # wait for user to put in items and type in 'done'
        trade_screen_validation('done','trade_private',start_time)
        # done is entered and now we are going to trade phase 2
        print("ITEMS CONFIRMED")
        pyg.moveTo(buttons['accept_trade1'])
        pyg.click()
        # check if we are on the phase 2 screen
        trade_screen_validation('final','trade_private2',start_time)
        # now we click all items in the trade menu so we can finish trade
        x = buttons['verify_items'][0]
        y = buttons['verify_items'][1]
        for i in range(5):
            for j in range(5):
                pyg.moveTo(x + (i * 44),y + (j * 44),.1)
                pyg.click()

        pyg.moveTo(buttons['accept_trade2'])
        pyg.click()
        pyg.sleep(12)
        print("add a trade screen validation that works? Trade not working as validator")
    except TimeoutError as e:
        print(f"Trade Failed due to {e}")
        raise ValueError
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
    
    
    print("NOW EXECUTE LISTING FUNCTION")
    return(username)

# clear out completed listings
def clear_listings():
    global item_listings
    global sold_items
    image = capture_area(areas['listings'])
    coords = get_item_coords(image,checking_listings=True)
    if len(coords) == 0:
        print("no listings found to clear from 'my listings'")

    for coordinate in coords[::-1]:
        x,y,w,h = coordinate
        slot = round(y / 50)
        print(f'SLOT {slot}')
        try:
            removed_item = item_listings.pop(slot-1)
            removed_item.is_sold = True
            removed_item.is_listed = False
            sold_items.append(removed_item)
            update_listing_order()
        except:
            print("No items in items.json")

        print(f" Clearing the listing at slot {slot} ")
        pyg.moveTo(x+29,y+490)
        pyg.click()
        pyg.moveTo(buttons["transfer_all_items"])
        pyg.click()
    
    save_items(sold_items,'sell_history.json')     

# ITEMS ARE IN THE STASH, WE MUST PRICE CHECK AND LIST THEM       
def list_items(username):
    global item_listings
    image = capture_area(areas['stash'])
    coords = get_item_coords(image)
    if debuggin:
        print(coords)
    for (x,y,w,h) in coords:
        if len(item_listings) > 9:
            return
        pyg.moveTo((x + 20) + areas['stash']['left'],(y + 20) + areas['stash']['top'])
        image = capture_area(areas['stash'])
        item = extract_item(image)
        if item != None:
            if debuggin:
                print(item.name)
            clear_listings()
            item.owner = username
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

                item.is_listed = True
                item.in_stash = False
                item.slot = len(item_listings)
                item_listings.append(item)
                print(f"Printing item listing inside list item function: {item_listings}")

            else:
                print("price was not detected :(")
                pyg.moveTo(buttons["my_listings"])
                pyg.click()
                pyg.sleep(2)
        else:
            print("Item skipped due to non-detection")

# Update the listing order when an item sells
def update_listing_order():
    global item_listings

    for index,item in enumerate(item_listings):
        item.slot = index

# used for entering attributes, every attribute added the bot have to click lower
def enter_attributes(attributes):
    attribute_buttons = {
            'attribute_entry':[1513,245],
            'attribute_selection':[1513,283]

        }
      
    if len(attributes) == 0:
        print("ERROR: NO ATTRIBUTES FOUND")
        return

    for i, attribute in enumerate(attributes):
        for location in attribute_buttons.keys():
            if location == 'attribute_selection':
                # Create a copy of the original coordinates
                current_coords = attribute_buttons[location].copy()
                # Modify the y-coordinate based on the attribute index
                current_coords[1] += i * 25
                pyg.moveTo(current_coords[0], current_coords[1], duration=0.1)
            else:
                pyg.moveTo(attribute_buttons[location][0], attribute_buttons[location][1], duration=0.1)
            
            pyg.sleep(0.3)
            pyg.click()
            
            if location == 'attribute_entry':
                pyg.write(attribute)

# TAKE THE RAW ITEM TEXT, FIND ATTRIBUTES FROM ATTRIBUTE LIST
def extract_attributes(image,target_color,tolerance=20, is_price=False):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    target_hsv = cv2.cvtColor(np.uint8([[target_color]]), cv2.COLOR_BGR2HSV)[0][0]

    lower_bound = np.array([max(0, target_hsv[0] - tolerance), 50, 50])
    upper_bound = np.array([min(179, target_hsv[0] + tolerance), 255, 255])

    mask = cv2.inRange(hsv_image, lower_bound, upper_bound)

    result = cv2.bitwise_and(image, image, mask=mask)

    gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)

    custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789.%abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    if is_price:
        raw_text = pyt.image_to_string(gray, config=custom_config)
        text = post_process_text(raw_text)
    else:
        text = pyt.image_to_string(gray)
    
    if debuggin_price_only or debuggin:
        print(text)
    
    return text

# Match the attributes
def match_attributes(text, attributes):
    # Sort attributes by length, longest first
    sorted_attributes = sorted(attributes, key=len, reverse=True)
    matched_attributes = []
    remaining_text = text

    for attr in sorted_attributes:
        # Create a pattern that allows for a prefix but requires the full attribute name
        pattern = r'(?:^|\s)(?:\S+\s+)?(' + re.escape(attr) + r')(?:\s|$)'
        match = re.search(pattern, remaining_text, re.IGNORECASE)
        if match:
            # Extract the exact matched text
            matched_text = match.group(1)
            matched_attributes.append(matched_text)
            # Remove the matched portion from the remaining text
            start, end = match.span(1)
            remaining_text = remaining_text[:start] + remaining_text[end:]

    return matched_attributes

# EXTRA PROCESSESING FOR NUMBERS, gold values, modifier names
def post_process_text(text):
    # Replace common misrecognitions
    replacements = {
        'n': '11',
        'ii': '11',
        'il': '11',
        'ns': '115',
        # Add more replacements as needed
    }
    
    for wrong, correct in replacements.items():
        text = re.sub(r'\b' + wrong + r'\b', correct, text)
    
    # Correct percentage format
    text = re.sub(r'(\d+)o/o', r'\1%', text)
    text = text.replace('.','')
    
    return text

# VALIDATE TRADE SCREEN IS READY TO GO
def trade_screen_validation(key,area,start):
    text = ''
    while key not in text.lower():
        image = capture_area(areas[area])
        text = extract_menu_text(image)
        if debuggin:
            print(text)
        end = datetime.now()
        time_diff = end - start
        if time_diff >= timedelta(minutes=2):
            raise TimeoutError("Trade Screen Timeout")
        pyg.sleep(1)

# ADD LISTING AND TRADE FILES TO MEMORY
def init_bot():
    global item_listings
    global sold_items
    try:
        item_listings = load_items('items.json')
        sold_items = load_items('sell_history.json')
    except:
        print("Loading my listings into memory FAILED, no items availabe in items.json or sell_history.json")

# SAVE YOUR TRADES TO TRADE HISTORY
def save_trades():
    global item_listings
    global sold_items

    save_items(item_listings,'items.json')
    save_items(sold_items, 'sell_history.json')

# GO TO THE TRADE TAB
def go_to_trade_post():

    pyg.keyDown('esc')
    pyg.keyUp('esc')

    pyg.moveTo(buttons['start_trade'])
    pyg.sleep(1)
    pyg.click()

    pyg.moveTo(buttons['trade_post'])
    pyg.sleep(1)
    pyg.click()
    
    pyg.moveTo(buttons['my_listings'])
    pyg.sleep(1)
    pyg.click()
    
# GO TO THE LISTINGS TAB
def go_to_listings():
    pyg.keyDown('esc')
    pyg.keyUp('esc')
    
    pyg.moveTo(buttons['start_trade'])
    pyg.sleep(1)
    pyg.click()

    pyg.moveTo(buttons['marketplace'])
    pyg.sleep(1)
    pyg.click()
    
    pyg.moveTo(buttons['my_listings'])
    pyg.sleep(1)
    pyg.click()

    
    pyg.moveTo(buttons['stash_slot_1'])
    pyg.sleep(1)
    pyg.click()

#CLEAR THE INVENTORY RIGHT AFTER TRADE
def clear_inventory():
    trade_inventory_coord = (1142,642)
    x = trade_inventory_coord[0]
    y = trade_inventory_coord[1]
    for i in range(10):
        for j in range(5):
            pyg.keyDown('shiftleft')
            pyg.keyDown('shiftright')
            pyg.moveTo(x + (i * 42), y + (j * 44), .1)
            pyg.rightClick()

    pyg.keyUp('shiftleft')
    pyg.keyUp('shiftright')

# MAIN PROGRAM LOGIC, start init at trade post
def main():
    init_bot()
    
    while(True):
        if(testing_trade):
            try:
                user = trade()
            except ValueError as e:
                user = 'None'
                print("Trade failed or completed")
        
            go_to_listings()
        
        clear_listings()
        list_items('user') 

        # clear_inventory()
        save_trades()
        if(testing_trade):
            go_to_trade_post()
    


    
# RUN
main()

# important bugs to fix:
    # verification for end of trade completed screen
    # items to add
    # change the 'done' area in trade. Cause if the user changes the items it screws up
    # 'additional weapon damage is often screwed up as a modifier causing a ton of price loss
    # navigating to marketplace is still kinda buggy, doesnt go automatically sometimes
 
#  features to finish:
    # Player object that holds a players username and money