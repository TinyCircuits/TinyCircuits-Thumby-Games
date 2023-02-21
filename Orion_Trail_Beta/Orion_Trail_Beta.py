#inititalize Game

import random, thumby, time, json
running = True
emulator = True
try:
    import emulator
    # It worked, we're running in the emulator
except ImportError:
    emulator = False
    
def main(emulator):
 # Core Engine Functions   
 
    #Universal Menu Function
    def menu(menu_items, header=None, display_stat=None, image=None):
        #Do NOT use display_stat parameter unless menu_items is a crew object
        in_menu = True
        arrow  = bytearray([31,31,0,17,27])
        arrow_position = 0
        while in_menu:
            offset = arrow_position//5
            offset_remainder = offset % 5
            if offset_remainder > 0:
                offset = offset_remainder
            header_space = 0
            if header != None:
                thumby.display.drawText(header, 10, 0, 0)
                header_space = 1
            for i in range(len(menu_items[offset:offset+5])):
                j = i + header_space
                if display_stat != None:
                    thumby.display.drawText(menu_items[i+offset][0], 10, j*8, 0)
                    stat = get_character_stat(menu_items[i+offset], display_stat)
                    thumby.display.drawText(str(stat), 50, j*8, 0)
                else:
                    thumby.display.drawText(menu_items[i+offset], 6, j*8, 0)
                thumby.display.blit(arrow , 0, arrow_position*8+int(header_space*8), 5, 5, 1, 0, 0)
            if thumby.buttonU.pressed() and arrow_position > 0:
                arrow_position -= 1
            elif thumby.buttonD.pressed() and arrow_position < int(len(menu_items)-1):
                arrow_position += 1
            redraw_screen(1, 0.2)
            in_menu = check_escape('a')
        return menu_items[arrow_position]
        
    def config_menu():
        config_options = ['Dflt Cfg']
        chosen_option = None
        while chosen_option == None:
            chosen_option = menu(config_options)
            if chosen_option == 'Dflt Cfg':
                config = [['Start Money', 500], ['Start Food', 100], ['Start Oxygen', 100], ['Event Frequency', 3]]
        '''elif chosen_option == 'New Config':
                if emulator:
                    draw_text_blocks('Sorry, you cannot save or load config files on virutal hardware')
                    chosen_option = None
                else:
                def save_config(money, food, oxygen, event):
               with open('Games/Orion_Trail_Beta/config.json',"w") as config:
                    json.dump({"Start_Money":money,"Start Food":food, "Start Oxygen": oxygen, "Event Frequency": event},config)
                    draw_text_blocks('WARNING: Save/Load Config is currently untested and may crash')
                    draw_text_blocks('This message will be removed in a few days when I have access to physical hardware for further testing')
                    placeholder_menu = menu(['Yes', 'Go Back'], 'Proceed?')
                    if placeholder_menu == 'Yes':
                        create_config = menu()
                        with open('Games/Orion_Trail_Beta/config.json',"w") as config:
                        json.dump({"Start_Money":money,"Start Food":food, "Start Oxygen": oxygen, "Event Frequency": event},config)
            elif chosen_option == 'Load Config':
                if emulator:
                    draw_text_blocks('Sorry, you cannot save or load config files on virutal hardware')
                    chosen_option = None
                else:
                    draw_text_blocks('WARNING: Load Config is currently untested and may crash')
                    draw_text_blocks('This message will be removed in a few days when I have access to physical hardware for further testing')
                    placeholder_menu = menu(['Yes', 'Go Back'], 'Proceed?')
                    if placeholder_menu == 'Yes': '''
        return config  
 
    def initialize_core_data(crew):
        names = []
        crew=[]
        config = config_menu()
        character = create_character('You', crew)
        character_screen(character)
        day = 1
        #Remember, Event Frequency Is Inverse, so the probability that an event will occur is 1/X.
        money = config[0][1]
        ship=[['engine', 100, 500], [config[1][1], config[2][1]], [['Condition', 100] , ['Destination', 'Unknown'], ['Autopilot', False]], 100, 100, 100]
        return crew, ship, money, day

        
    def save_game(crew, ship, money, day):
               with open('Games/Orion_Trail_Beta/savestate.json',"w") as save_file:
                    json.dump({"crew":crew,"ship":ship,"money":money,"day":day},save_file)
              
    def save_state_menu(crew):
        time.sleep(1)
        menu = True
        while menu:
            thumby.display.drawText('A: Continue', 0, 12, 0)
            thumby.display.drawText('B: New Game', 0, 24, 0)
            if thumby.buttonA.pressed():
                if emulator:
                    draw_text_blocks('Sorry, you cannot save or load games on virutal hardware')
                    crew, ship, money, day = initialize_core_data()
                    menu = False
                else:
                    with open('Games/Orion/savestate.json',"r") as save_file:
                        data = json.load(save_file)
                        crew = data["crew"]
                        ship = data["ship"]
                        money = data["money"]
                        day = data["day"]
                menu = False
            elif thumby.buttonB.pressed():
                crew, ship, money, day = initialize_core_data(crew)
                menu = False
            redraw_screen(1, 1)
        return crew, ship, money, day
    
    def draw_stars(num):
        star_sprite = bytearray([18,33,12,12,33,18])
        thumby.display.fill(0)
        for i in range(num):
            thumby.display.blit(star_sprite, random.randint(0,65), random.randint(10,35), 6, 6, 0, 0 ,0)
        thumby.display.update()
        
    def redraw_screen(color, update_time):
        thumby.display.update()
        time.sleep(update_time)
        thumby.display.fill(color)
        
    def draw_text_blocks(text, dialog_face=None):
        char_width = 14
        chars = len(text)
        remaining_chars = chars
        iterator = chars // char_width
        remainder = chars % char_width
        if dialog_face != None:
                thumby.display.blit(dialog_face, 0, 10, 32, 32, 1, 0, 0)
        redraw_screen(1,1)
        for i in range(int(iterator)):
                if remaining_chars >= char_width:
                    remaining_chars -= char_width
                    for j in range(char_width):
                        thumby.display.drawText(text[j+(i*char_width)], j*5, i*8, 0)
                if remaining_chars < char_width:
                    for j in range(remaining_chars):
                        thumby.display.drawText(text[j+(chars-remainder)], j*5, int((i+1))*8, 0)
                    remaining_chars= 0
        redraw_screen(1,1)
        reading =  True
        while reading:
            reading = check_escape()
        redraw_screen(1,1)
                    
    
    
                
    def intro():
        a_visible = False
        a_button = bytearray([195,189,70,106,106,70,189,195])
        for i in range(10):
            time.sleep(0.2)
            draw_stars(i)
        thumby.display.drawText('Welcome to', 0, 0, 1)
        thumby.display.drawText('Orion Trail', 0, 10, 1)
        thumby.display.update()
        while thumby.buttonA.pressed() == False:
            if a_visible == True:
                thumby.display.blit(a_button, 10, 20, 8, 8, 0, 0, 0)
                a_visible = False
            else:    
                a_visible = True
            thumby.display.update()
            time.sleep(0.1)
        random.seed(time.ticks_us())
        
    def check_escape(button='b'):
        running = True
        if thumby.buttonB.pressed() and button == 'b':
            running = False
        elif thumby.buttonA.pressed() and button == 'a':
            running = False
        return running
        
        
    #Menu Functions                        
                        
    def stat_comparison_menu(crew, stat):
        stat_text = str(stat + ' stat')
        chosen = menu(crew, stat_text, stat)
        return chosen
     
    #character functions 
       
    def create_character(name, crew):
        character = [name, [['hearing', 100],['sight', 100], ['movement', 100], ['resilience', 100]], [['shooting', 5], ['melee', 5], ['pilot', 5], ['social', 5], ['repair', 5]], [], [], [], [['Pistol', 1, 75, 'An old style weapon that fires metal projectiles'], ['Jumpsuit', 1, 50, 'A simple suit to protect the wearer during space travel']], ['Weight', 100], ['Consumption', 1]]
        traits = ['Ace', 'Handyman', 'Ugly', 'Attractive', 'Clumsy', 'Resilient', 'Sickly', 'Obese']
        for i in range(2):
            trait = random.choice(traits)
            if trait not in character[5]:
                while trait == 'Ugly' and 'Attractive' in character[5] or trait == 'Attractive' and 'Ugly' in character[5]:
                    trait = random.choice(traits)
                while trait == 'Handyman' and 'Clumsy' in character[5] or trait == 'Clumsy' and 'Handyman' in character[5]:
                    trait = random.choice(traits)
                while trait == 'Sickly' and 'Resilient' in character[5] or trait == 'Sickly' and 'Resilient' in character[5]:
                    trait = random.choice(traits)
                character[5].append(trait)
                
        if 'Sickly' in character[5]:
            character[1][3][1] -= 25
        if 'Resilient' in character[5]:
            character[1][3][1] += 25
        if 'Ace' in character[5]:
            character[2][2][1] += 2
        if 'Handyman' in character[5]:
            character[2][4][1] += 2
        if 'Ugly' in character[5]:
            character[2][3][1] -= 2
        if 'Attractive' in character[5]:
            character[2][3][1] += 2
        if 'Obese' in character[5]:
            character[7][1] += 200
        crew.append(character)
        return character
    
    def character_screen(character):
        time.sleep(0.5)
        # BITMAP: width: 10, height: 20
        human_screen_image = bytearray([255,143,119,251,251,251,119,143,255,255,
           239,239,239,110,128,110,239,239,239,239,
           15,7,7,8,15,8,7,7,15,15])
        a_button = bytearray([195,189,70,106,106,70,189,195])
        running = True
        screen_position = 0
        while running:
            i = 0
            thumby.display.blit(human_screen_image, 0, 0, 10, 20, 1, 0, 0)
            if screen_position == 0:
                thumby.display.drawText('Traits:', 20, 0, 0)
                for i in range(len(character[5])):
                    j = i + 1
                    thumby.display.drawText(character[5][i], 20, j*10, 0)
            elif screen_position == 1:
                thumby.display.drawText('Phys Stats:', 20, 0, 0)
                for i in range(2):
                    j = i + 1
                    num = str(character[1][i][1])
                    thumby.display.drawText(character[1][i][0], 10, j*10, 0)
                    thumby.display.drawText(num, 50, j*10, 0)
            elif screen_position == 2:
                thumby.display.drawText('Phys Stats:', 20, 0, 0)
                for i in range(2):
                    j = i + 1
                    i += 2
                    num = str(character[1][i][1])
                    thumby.display.drawText(character[1][i][0], 10, j*10, 0)
                    thumby.display.drawText(num, 50, j*10, 0)
            elif screen_position == 3:
                thumby.display.drawText('Skills:', 20, 0, 0)
                for i in range(2):
                    j = i + 1
                    i += 2
                    num = str(character[2][i][1])
                    thumby.display.drawText(character[2][i][0], 10, j*10, 0)
                    thumby.display.drawText(num, 50, j*10, 0)
            elif screen_position == 4:
                thumby.display.drawText('Medical:', 20, 0, 0)
                for i in range(len(character[3])):
                    thumby.display.drawText(character[3][i][0], 10, (i*10)+10, 0)
            elif screen_position == 5:
                arrow  = bytearray([31,31,0,17,27])
                thumby.display.drawText('Actions:', 20, 0, 0)
                thumby.display.blit(arrow, 0, 30, 5, 5, 1, 0, 0)
                thumby.display.drawText('Execute', 10, 12, 0)
                
            if thumby.buttonR.pressed() and screen_position < 5:
                screen_position += 1
            elif thumby.buttonL.pressed() and screen_position  >= 0:
                screen_position -= 1
            thumby.display.blit(a_button, 8, 30, 8, 8, 1, 0, 0)
            thumby.display.drawText('Continue', 15, 30, 0)
            running = check_escape('a')
            thumby.display.update()
            time.sleep(0.2)
            thumby.display.fill(1)
    
    def get_character_items(character):
        items = []
        for i in range(len(character[6])):
            items.append(character[6][i][0])
        return items
        
    def get_crew_names(crew):
        names = []
        for i in range(len(crew)):
            names.append(crew[i][0])
        return names
    
    def get_crew_member_by_name(crew, name):
        for i in range(len(crew)):
            if crew[i][0] == name:
                return crew[i]
        
    def get_character_traits(character):
        return character[5]
        
    def get_character_stat(character, stat):
        modifier = 0
        items = get_character_items(character)
        for i in range(len(character[6])):
            if stat == 'pilot' or 'Plt Hlm' in character:
                modifier += 3
        for i in range(len(character[1])):
            if character[1][i][0] == stat:
                return int(character[1][i][1] + modifier)
            else:
                for j in range(len(character[2])):
                    if character[2][j][0] == stat:
                        return int(character[2][j][1] + modifier)
    def get_full_inventory(crew):
        possible_items = []
        for i in range(len(crew)):
            for j in range(len(crew[i][6])):
                possible_items.append([crew[i][6][j], crew[i]])
        return possible_items   
                
    # event piece functions
    def attempt_persuasion(character, skill, difficulty):
        num = random.randint(0,difficulty)
        items = get_character_items(character)
        for i in range(len(character[6])):
            if 'Amlt of Arnden' in character:
                skill += 10
            if 'Gmblrs Snglasses' in character:
                name = character[0]
                text = str(name + 'Tells you that the odds of persuading the robbers are approximately ' +  str(skill) + ' in ' + str(difficulty))
                draw_text_blocks(text)
        if skill > num:
            return True
        else:
            return False
            
    def get_all_items():
        items = [['Pistol', 1, 75, 'An old style weapon that fires metal projectiles'], ['Jumpsuit', 1, 50, 'A simple suit to protect the wearer during space travel'], ['Gmblrs Snglasses', 1 , 300, 'Tells the wearer the probability of chance based events'], ['Plt Hlm', 1, 200, 'A high tech helmet which contains an integrated computer to make the wearer a better pilot'], ['Amlt of Arnden', 1, 150, 'A mysterious amulet that gives its wearer a more intimidating aura']]
        return items
        
    def give_item(item, character):
        items = get_all_items()
        if item == 'r':
            item = random.choice(items)
        for i in range(len(items)):
            if item in items[i][0]:
                character[6].append([item, items[i][1]])
        return character
    
    def remove_item(item, character, crew):
        character[6].remove(item)
        for i in range(len(crew)):
            if crew[i][0] == character[0]:
                crew[i] = character
        return crew
        
    def check_for_item_by_crew(crew, item_name):
        available_items = get_all_items()
        item = None
        for i in range(len(available_items)):
            if available_items[i][0] == item_name:
                item = available_items[i]
        for i in range(len(crew)):
            character = crew[i]
            if item in character[6]:
                return True
            else:
                return False
    
    def check_for_item_by_character(character, item_name):
        available_items = get_all_items()
        item = None
        for i in range(len(available_items)):
            if available_items[i][0] == item_name:
                item = available_items[i]
        if item in character[6]:
            return True
        else:
            return False
    
    def consume_food(character, ship):
        for i in range(character[7][1]//100):
            ship[4] -= 1
            
    def progress_disease(disease, character):
        if disease in character[3]:
            num = character[3].index(disease)
            character[3][num][1][0] += character[1][3][1] // 10
            character[3][num][1][1] += character[3][num][2]
            if disease == 'bloatworms':
                 character[7][1] += 10
            
    def progress_all_diseases(character):
        if character[3] != []:
            infected = character[3]
            for disease_num in range(len(infected)):
                progress_disease(infected[disease_num], character)
    
    #the next two functions are completely useless, even for testing as of now            
    def casino(money, character):
        casino_menu = True
        arrow_position = 0
        arrow  = bytearray([31,31,0,17,27])
        games = ['']
        menu(games)
            
    def planet_locations(planet, money):
        
        def select_location(locations):
            selecting_location = menu(locations)
            
        # BITMAP: width: 72, hreight: 40
        in_transport = bytearray([255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,127,191,191,127,127,255,255,255,255,255,255,127,191,255,191,255,255,255,255,255,255,255,
           255,255,255,255,247,247,247,247,7,247,247,247,7,247,251,221,174,142,222,254,254,222,174,142,221,251,247,7,247,247,247,247,247,247,247,247,247,247,247,247,247,247,247,247,243,245,22,229,245,251,27,11,13,14,47,30,254,253,29,13,13,12,41,23,229,23,245,7,247,247,243,247,
           255,255,255,255,255,255,255,255,0,255,255,255,240,239,223,191,127,127,127,127,127,127,127,127,191,223,239,240,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,0,255,255,255,254,252,252,252,252,62,31,31,62,252,252,252,252,254,255,0,255,0,255,255,255,255,
           255,255,255,255,255,255,255,255,0,255,255,255,255,255,255,255,255,255,255,0,0,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,254,253,243,239,31,223,223,223,28,24,216,220,223,223,15,243,253,254,255,235,196,159,63,127,255,
           255,255,255,255,255,255,255,255,252,253,253,253,253,253,253,253,253,253,253,0,0,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,252,195,31,127,0,0,127,127,159,195,252,255,255,255,255,255,255,255,255,254,254])
        gidonian_face = bytearray([255,255,127,159,223,111,47,47,47,47,111,239,239,239,239,239,239,239,239,111,47,47,47,47,111,239,223,159,127,255,255,255,
           1,254,255,225,192,128,0,63,63,0,128,192,225,255,255,255,255,225,192,128,0,63,63,0,128,192,225,255,255,254,1,255,
           252,243,239,223,191,127,255,255,255,255,255,255,255,63,95,143,95,63,255,255,255,255,255,255,255,127,191,223,239,241,254,255,
           255,255,255,255,255,255,254,253,253,253,251,231,223,184,181,99,181,184,223,231,251,253,253,253,254,255,255,255,255,255,255,255])
        # BITMAP: width: 30, height: 20
        casino_small = bytearray([255,255,239,223,23,223,239,255,255,255,255,255,255,255,255,255,255,255,255,239,223,23,223,239,255,255,255,255,255,255,
           254,242,242,254,0,251,203,251,203,251,19,235,109,109,235,19,251,251,251,251,251,0,254,242,242,254,0,255,255,255,
           1,1,1,1,0,1,1,1,1,1,0,1,0,0,1,0,1,1,1,1,1,0,1,1,1,1,0,1,1,1])
        if planet == 'Gidone':
            locations = ['Casino', 'Ship Repair', 'Mall']
            draw_text_blocks('Now Where would you like to go? Ive appointed Flombar as Your Guide', gidonian_face)
            draw_text_blocks('Just Say The Word and He`ll Take You There', gidonian_face)
            location = select_location(locations)
            if location == 'casino':
                draw_text_blocks('Next Stop, The Casino')
            redraw_screen(0, 4)
            thumby.display.blit(in_transport, 72, 40, 0, 0, 1, 0, 0)
            redraw_screen(0,10)
            draw_text_blocks('Were Here, Let Me Show You Around')
            casino(money)
        elif planet == 'Notera':
            locations = ['Archive', 'Reimagine Studios']
            draw_text_blocks('Now Where would you like to go?', noteran__face)
            location = select_location(locations)
            
    #Landing Sequence Functions these have no use without the planet functions being implemented other than for testing purposes
            
    def NoteraLandingSequence(crashed=False):
        player_ship = bytearray([66,129,195,195,195,195,231,231])
        # BITMAP: width: 32, height: 32
        noteran_face = bytearray([255,255,255,223,191,127,127,159,239,247,251,253,205,181,117,117,181,205,253,251,247,239,159,127,127,191,223,255,255,255,255,255,
           255,255,255,255,255,1,254,230,154,154,230,254,254,254,254,254,254,254,254,254,230,154,154,230,253,3,255,255,255,255,255,255,
           255,255,255,255,255,128,95,191,191,127,191,127,191,127,191,127,191,127,191,127,191,127,191,191,95,128,255,255,255,255,255,255,
           255,255,255,255,255,255,255,254,253,251,251,251,251,251,251,251,251,251,251,251,251,251,253,254,255,255,255,255,255,255,255,255])
        draw_text_blocks('Welcome to Notera', noteran_face)
        
    def GidoneLandingSequence(crashed=False):
        # BITMAP: width: 24, height: 24
        # BITMAP: width: 24, height: 24
        
        landing_pad = bytearray([255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,
           7,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,3,
           0,95,111,119,123,119,111,31,111,95,95,95,95,95,111,31,111,119,123,123,119,111,95,0])
        # BITMAP: width: 8, height: 20
        landing_helix_A = bytearray([255,239,85,85,85,187,255,255,
           255,238,85,85,85,187,255,255,
           15,14,5,5,5,11,15,15])
        # BITMAP: width: 8, height: 20
        landing_helix_B = bytearray([255,187,85,85,85,239,255,255,
           255,187,85,85,85,238,255,255,
           15,11,5,5,5,14,15,15])
        # BITMAP: width: 8, height: 8
        player_ship= bytearray([66,129,195,195,195,195,231,231])
        # BITMAP: width: 32, height: 32
        gidonian_face = bytearray([255,255,127,159,223,111,47,47,47,47,111,239,239,239,239,239,239,239,239,111,47,47,47,47,111,239,223,159,127,255,255,255,
           1,254,255,225,192,128,0,63,63,0,128,192,225,255,255,255,255,225,192,128,0,63,63,0,128,192,225,255,255,254,1,255,
           252,243,239,223,191,127,255,255,255,255,255,255,255,63,95,143,95,63,255,255,255,255,255,255,255,127,191,223,239,241,254,255,
           255,255,255,255,255,255,254,253,253,253,251,231,223,184,181,99,181,184,223,231,251,253,253,253,254,255,255,255,255,255,255,255])
        current_helix = landing_helix_A
        for i in range(6):
            thumby.display.blit(landing_pad, 20,15, 24, 24, 1, 0, 0)
            if current_helix == landing_helix_A:
                current_helix = landing_helix_B
            else:
                current_helix = landing_helix_A
            thumby.display.blit(current_helix, 30,16, 8, 20, 1, 0, 0)
            thumby.display.blit(player_ship, 30,(i*5), 8, 8, 1, 0, 0)
            redraw_screen(1, 2)
        draw_text_blocks('Welcome to Gidone, Your Ship is Safe With Us', gidonian_face)
        planet_locations('Gidone', money)
        #hearing, sight, movement, resilience for sense list
        #shooting, melee, piloting, social, repair for stat list
        #Diseases List
        #Injury List
        #Traits List
        #Engine, Wings, Navigator, Oxygen, Fuel, Rations
        # BITMAP: width: 8, height: 8
        b_button = bytearray([195,189,126,2,42,70,189,195])
        dead = False
        
    def main_menu(crew, ship, money):
        def dev_code_screen(crew, ship, money):
            deving = True
            test_number = 0
            while deving:
                thumby.display.drawText('Test Number:', 0,0,0)
                if thumby.buttonU.pressed() and test_number < 10:
                    test_number += 1
                elif thumby.buttonD.pressed() and test_number > 0:
                    test_number -= 1
                elif thumby.buttonA.pressed():
                    if test_number == 1:
                        raid(crew, ship)
                    elif test_number == 2:
                        end_screen('Forced')
                    elif test_number == 3:
                        GidoneLandingSequence(crashed=False)
                    elif test_number == 4:
                        charname = str('test ' +  str(int(len(crew))))
                        create_character(charname, crew)
                        character_screen(crew[-1])
                    elif test_number == 5:
                        give_disease('bloatworms', random.choice(crew))
                    elif test_number == 6:
                        robbery(crew, ship)
                    elif test_number == 7:
                        crew, ship, money = buisness_ship(crew, ship, money)
                thumby.display.drawText(str(test_number), 30,10,0)
                redraw_screen(1, 0.5)
                deving = check_escape()
            return crew, ship, money
                
        def ship_screen(ship):
            # BITMAP: width: 35, height: 20
            ship_image = bytearray([255,255,31,31,31,63,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,
        239,223,0,224,224,224,224,227,231,239,239,235,227,231,239,239,239,239,239,239,239,239,239,239,239,239,239,239,239,239,223,191,127,255,255,
       11,13,12,13,13,13,13,13,13,13,13,5,1,9,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,12,15])
            ship_image_nav_selected = bytearray([0,255,31,31,31,63,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,
       239,223,0,224,224,224,224,227,231,239,239,235,227,231,239,239,239,239,239,239,239,239,239,239,239,239,239,239,239,15,31,63,127,255,255,
       11,13,12,13,13,13,13,13,13,13,13,5,1,9,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,12,12,12,12,12,15])
            ship_image_wings_selected = bytearray([0,255,31,31,31,63,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,
       239,223,0,224,224,224,224,227,231,239,239,235,3,7,239,239,239,239,239,239,239,239,239,239,239,239,239,239,239,239,223,191,127,255,255,
       11,13,12,13,13,13,13,13,13,13,13,5,0,8,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,12,15])
        # BITMAP: width: 35, height: 20
            ship_image_engine_selected = bytearray([255,255,31,31,31,63,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,
       15,31,0,224,224,224,224,227,231,239,239,235,3,7,239,239,239,239,239,239,239,239,239,239,239,239,239,239,239,239,223,191,127,255,255,
       8,12,12,13,13,13,13,13,13,13,13,5,0,8,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,12,15])
        # BITMAP: width: 35, height: 20
            ship_image_cabin_selected = bytearray([255,255,31,31,31,63,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,
       239,223,0,224,224,224,224,227,231,239,15,11,3,7,15,15,15,15,15,15,15,15,15,15,239,239,239,239,239,239,223,191,127,255,255,
       11,13,12,13,13,13,13,13,13,13,12,4,0,8,12,12,12,12,12,12,12,12,12,12,13,13,13,13,13,13,13,13,13,12,15])
        # BITMAP: width: 5, height: 5
            ship_data = [['General View', ship_image], ['Nav View', ship_image_nav_selected], ['Wings View', ship_image_wings_selected], ['Engine View' , ship_image_engine_selected], ['Vitals View', ship_image_cabin_selected]] 
            ship_menu = True
            selected = 0
            while ship_menu:
                if thumby.buttonR.pressed() and selected < int(len(ship_data)-1):
                    selected += 1
                elif thumby.buttonL.pressed() and selected > 0:
                    selected -= 1
                if thumby.buttonA.pressed():
                    
                    if ship_data[selected][0] == 'Vitals View':
                        oxygen_view = True
                        while oxygen_view:
                            oxygen_text = str('Oxygn ' + str(ship[3]))
                            thumby.display.drawText(oxygen_text, 0, 0, 0)
                            ration_text = str('Food ' + str(ship[4]))
                            thumby.display.drawText(ration_text, 0, 10, 0)
                            food__days = str('Food ' + str(ship[4]))
                            thumby.display.update()
                            time.sleep(0.2)
                            thumby.display.fill(1)
                            oxygen_view = check_escape()
                    if ship_data[selected][0] == 'Nav View':
                            nav_view = True
                            while nav_view:
                                condition_text = str('Cndtn ' + str(ship[2][0][1]))
                                thumby.display.drawText(condition_text, 0, 0, 0)
                                thumby.display.update()
                                time.sleep(0.2)
                                thumby.display.fill(1)
                                nav_view = check_escape()
                    if ship_data[selected][0] == 'Wings View':
                            wings_view = True
                            while wings_view:
                                right_condition_text = str(ship[1][0])
                                left_condition_text = str(ship[1][1])
                                thumby.display.drawText('Rt Wng Cndtn' , 0, 0, 0)
                                thumby.display.drawText(right_condition_text, 0, 16, 0)
                                thumby.display.drawText('Lt Wng Cndtn', 0, 24, 0)
                                thumby.display.drawText(left_condition_text, 0, 32, 0)
                                thumby.display.update()
                                time.sleep(0.2)
                                thumby.display.fill(1)
                                wings_view = check_escape()
                    if ship_data[selected][0] == 'Engine View':
                            engine_view = True
                            while engine_view:
                                condition_text = str('Cndtn ' + str(ship[0][1]))
                                fuel_text = str('Fuel ' + str(ship[0][2]))
                                thumby.display.drawText(condition_text, 0, 0, 0)
                                thumby.display.drawText(fuel_text, 0, 20, 0)
                                thumby.display.update()
                                time.sleep(0.2)
                                thumby.display.fill(1)
                                engine_view = check_escape()
                ship_text = ship_data[selected][0]
                thumby.display.drawText(ship_text, 0, 30, 0)
                current_image = ship_data[selected][1]
                thumby.display.blit(current_image, 0, 0, 35, 20, 1, 0, 0)
                redraw_screen(1, 0.2)
                ship_menu = check_escape()
                
        arrow  = bytearray([31,31,0,17,27])
        arrow_position = 0        
        options = ['Inventory', 'Crew', 'Log', 'Ship', 'Dev Codes']
        selection = menu(options)
        if selection == 'Inventory':
            running_inv = True
            while running_inv:
                for i in range(len(crew)):
                    character = crew[i]
                    if character[6] != []:
                        for i in range(len(character[6])):
                            num = str(character[6][i][1])
                            j = i + 1
                            thumby.display.drawText(character[6][i][0], 0, j*10, 0)
                            thumby.display.drawText(num, 60, j*10, 0)
                redraw_screen(1, 0.2)
                running_inv = check_escape()
        elif selection == 'Crew':
            crew_inv = get_crew_names(crew)
            character = menu(crew_inv)
            for i in range(len(crew)):
                if crew[i][0] == character:
                    character_screen(crew[i])
        elif selection == 'Ship':
            ship_screen(ship)
        elif selection == 'Dev Codes':
            crew, ship, money = dev_code_screen(crew, ship, money)
        return crew, ship, money
    
    def robbery(crew, ship):
        draw_text_blocks('A voice comes over your communications system, it says;')
        draw_text_blocks('We have weapons aimed at your ship, either give us the following or die dishonorably')   
        possible_items = get_full_inventory(crew)
        requested = []
        options = ['Take it', 'Fire Away', 'Are you sure?']
        if len(possible_items) >= 2:
            amount = random.randint(1,int(len(possible_items)//2))
            for i in range(amount):
                requested.append(random.choice(possible_items))
            for i in range(len(requested)):
                thumby.display.drawText((str(str(requested[i][0][1]) + 'x '+ str(requested[i][0][0]))), 0, 10*i, 0)
            redraw_screen(1, 5)
            answer = menu(options, header='Choices:')
            if answer == 'Take it':
                draw_text_blocks('Intercom: Good Choice')
                for i in range(len(requested)):
                    crew = remove_item(requested[i][0], requested[i][1], crew)
            elif answer == 'Fire Away':
                draw_text_blocks('Intercom: Very Well, Now Die')
                boss_ship(crew, ship)
            elif answer == 'Are you sure?':
                persuader = stat_comparison_menu(crew, 'social')
                persuasion_skill = get_character_stat(persuader, 'social')
                if attempt_persuasion(persuader, persuasion_skill, 30):
                    draw_text_blocks('They fly away without another word')
                else:
                    draw_text_blocks('We dont fear you! Now Die')
                    boss_ship(crew, ship)
        else:
            draw_text_blocks('It seems you dont have anything of value that the robbers want')
        redraw_screen(1,0.1)
        
        
        
    def damage_ship_part(ship): 
        part = random.choice(['engine', 'wings', 'nav'])
        if part == 'engine':
            ship[0][1] -= random.randint(1,25)
        elif part == 'wings':
            ship[1][random.randint(0,1)] -= random.randint(1,25)
        elif part == 'nav':
            ship[2][0][1] -= random.randint(1,25)
        return ship
        
    def check_ship(ship):
        if ship[0][1] <= 0:
            end_screen('Engine Explosion')
        if ship[0][2] <= 0:
            fuel_screen = True
            draw_text_blocks('Your Fuel is Empty, Your Ship Cannot Move, The Best You Can Do Is Hope For Help')
        return ship
        
    def give_disease(disease, character, severity=1):
        draw_text_blocks(str(character[0] + ' has contracted' + disease + '!'))
        draw_text_blocks('either seek a doctor, or hope they fight off the infection on their own')
        if disease == 'bloatworms':
            draw_text_blocks('bloatworms is a parasitic disease')
            draw_text_blocks('which causes rapid growth in the host') 
            draw_text_blocks('they will continue to grow, consuming more and')
            draw_text_blocks('more food until they are cured or die from starvation')
        character[3].append([disease, [0, 0], severity])
    
    #Amogus functions is a placeholder, has no use, even in testing.    
    def amogus(crew, ship):
        if len(crew) < 2:
            thumby.display.drawText('The Nav Says "Someone here is actually an alien in disguise"')
            
    def boss_ship(crew, ship):
        # BITMAP: width: 8, height: 8
        player_ship = bytearray([189,126,60,60,60,60,24,24])
        # BITMAP: width: 30, height: 40
        boss_ship = bytearray([0,192,64,64,64,192,32,32,32,16,16,16,16,16,16,16,16,16,16,16,144,144,144,16,48,96,128,0,0,0,
       0,3,2,2,255,0,0,2,2,0,2,130,0,2,2,160,64,160,0,7,10,15,202,39,16,8,7,0,0,0,
       0,0,0,0,255,60,66,66,66,126,153,24,24,24,24,24,24,24,24,24,24,24,255,0,0,0,0,0,0,0,
       0,192,64,64,255,0,0,32,32,0,32,33,0,32,32,5,2,5,0,192,160,224,163,196,8,24,240,0,0,0,
       0,3,2,2,2,3,4,4,4,8,8,8,8,8,8,8,8,8,8,9,10,11,10,9,12,6,1,0,0,0])
       # BITMAP: width: 20, height: 20
        explosion = bytearray([0,128,0,32,64,8,0,66,34,34,34,66,0,8,64,32,0,128,0,0,
       0,16,0,64,32,7,0,16,37,34,37,16,0,7,32,64,0,16,0,0,
       0,0,0,0,0,0,1,4,4,4,4,4,1,0,0,0,0,0,0,0])
        draw_text_blocks('You have chosen to fight the robbers!')
        draw_text_blocks('You Must Choose a Pilot')
        pilot = stat_comparison_menu(crew, 'pilot')
        pilot_skill = get_character_stat(pilot, 'pilot')
        top_down_ship = True
        player_ship_axis = 20
        boss_ship_axis = 0
        boss_ship_direction = 'UP'
        to_fire = 'TOP'
        bullet_axis = 20
        bullet_timer = 0
        boss_health = 100
        boss_bullet_timer = 50
        while top_down_ship:
            thumby.display.drawLine(10, 0, boss_health, 0, 1)
            thumby.display.blit(player_ship, 20, player_ship_axis, 8, 8, 0, 0, 0)
            ship_speed_modifier = int( pilot_skill // 2)
            if thumby.buttonU.pressed():
                player_ship_axis -= ship_speed_modifier
            elif thumby.buttonD.pressed():
                player_ship_axis += ship_speed_modifier
            if thumby.buttonA.pressed() and bullet_timer == 0:
                bullet_axis = 20
                bullet_timer = 40
                bullet_y = player_ship_axis + 4
            if bullet_timer > 0:
                thumby.display.drawLine(bullet_axis, bullet_y, int(bullet_axis+3), bullet_y, 1)
                bullet_axis += 1
            if bullet_axis > 30:
                bullet_axis = 20
                boss_health -= 10
                bullet_timer = 0
            if player_ship_axis < 0:
                player_ship_axis = 0
            if player_ship_axis > 40:
                player_ship_axis = 40
            if bullet_timer > 0:
                bullet_timer -= 1
            thumby.display.blit(boss_ship, 40, boss_ship_axis, 30, 40, 0, 0, 0)
            if boss_ship_direction == 'UP':
                boss_ship_axis += 2
                if boss_ship_axis > 20:
                    boss_ship_direction = 'DOWN'
            else:
                boss_ship_axis -= 2
                if boss_ship_axis < -20:
                    boss_ship_direction = 'UP'
            if boss_bullet_timer <= 0:
                if to_fire == 'TOP':
                    thumby.display.drawLine(40, boss_ship_axis+8, 0,boss_ship_axis+8, 1)
                    to_fire = 'DOWN'
                    for i in range(8):
                        if player_ship_axis + i == boss_ship_axis+8:
                            redraw_screen(0,6)
                            end_screen('Robbed')
                else:
                    to_fire = 'TOP'
                    thumby.display.drawLine(40, boss_ship_axis+32, 0,boss_ship_axis+32, 1)
                    for i in range(8):
                        if player_ship_axis + i == boss_ship_axis+32:
                            redraw_screen(0,6)
                            end_screen('Robbed')
                boss_bullet_timer = 20
            else:
                boss_bullet_timer -= 1
            if boss_health <= 0:
                redraw_screen(0, 0.1)
                thumby.display.blit(player_ship, 20, player_ship_axis, 8, 8, 0, 0, 0)
                thumby.display.blit(explosion, 40, 15, 20, 20, 0, 0, 0)
                redraw_screen(0, 8)
                top_down_ship = False
            redraw_screen(0, 0.1)
       
    def raid(crew, ship):
        raid_types = ['Air Strike']
        raid_factions = ['Pirates']
        raid_type = random.choice(raid_types)
        raid_faction = random.choice(raid_factions)
        # BITMAP: width: 10, height: 10
        raider_ship = bytearray([240,192,240,200,196,196,200,240,192,224,
       1,0,1,1,1,1,1,1,0,1])
        ti_fighter = bytearray([255,48,48,48,72,72,48,48,48,255,
       3,0,0,0,0,0,0,0,0,3])
       # BITMAP: width: 8, height: 8
        player_ship = bytearray([189,126,60,60,60,60,24,24])
        # BITMAP: width: 8, height: 8
        ship_exploded = bytearray([129,90,36,90,90,36,90,129])
        arrow  = bytearray([31,31,0,17,27])
        if raid_type == 'Air Strike':
            if raid_faction == 'Pirates':
                enemy_ship_image = raider_ship
            time.sleep(0.3)
            raid_intro1 = True
            draw_text_blocks('Pirates are Firing Upon Your Ship')
            draw_text_blocks('You Must Choose a Pilot')
            pilot = stat_comparison_menu(crew, 'pilot')
            pilot_skill = get_character_stat(pilot, 'pilot')
            top_down_ship = True
            player_ship_axis = 20
            bullet_axis = 20
            bullet_timer = 0
            fleet_amount = random.randint(2,20)
            fleet = []
            fleet_board = []
            max_fleet_board = 2
            
            for k in range(fleet_amount):
                fleet.append([[70, random.randint(0,30)], 0, [None, None]])
            while top_down_ship:
                thumby.display.blit(player_ship, 20, player_ship_axis, 8, 8, 0, 0, 0)
                ship_speed_modifier = int( pilot_skill // 2)
                if thumby.buttonU.pressed():
                    player_ship_axis -= ship_speed_modifier
                elif thumby.buttonD.pressed():
                    player_ship_axis += ship_speed_modifier
                if thumby.buttonA.pressed() and bullet_timer == 0:
                    bullet_axis = 20
                    bullet_timer = 40
                    bullet_y = player_ship_axis + 4
                if bullet_timer > 0:
                    thumby.display.drawLine(bullet_axis, bullet_y, int(bullet_axis+3), bullet_y, 1)
                    bullet_axis += 1
                if player_ship_axis < 0:
                    player_ship_axis = 0
                if player_ship_axis > 40:
                    player_ship_axis = 40
                if bullet_timer > 0:
                    bullet_timer -= 1
                if len(fleet_board) == 0:
                    for l in range(max_fleet_board):
                        if len(fleet) > 0:
                            ship_spawn = random.choice(fleet)
                            fleet.remove(ship_spawn)
                            fleet_board.append(ship_spawn)
                
                fleet_board_remove = []
                for m in range (len(fleet_board)):
                    if len(fleet_board) > 0:
                        thumby.display.blit(enemy_ship_image, fleet_board[m][0][0], fleet_board[m][0][1], 8, 8, 0, 0, 0)
                        fleet_board[m][0][0] -= 1
                        fleet_board[m][0][1] += random.randint(-1,1)
                        if fleet_board[m][0][0]  < 0:
                            fleet_board_remove.append(fleet_board[m])
                            fleet_amount -= 1
                        if fleet_board[m][1] == 0:
                            fleet_board[m][1] = 40
                        if fleet_board[m][1] > 0:
                            fleet_board[m][1] -= 1
                    for o in range(8):
                        if player_ship_axis + o == fleet_board[m][0][1]:
                            for p in range(8):
                                if 20 + o == fleet_board[m][0][0]:
                                    ship = damage_ship_part(ship)
                                    break
                    if bullet_timer > 0:
                        for n in range(8):
                            if bullet_y + n == fleet_board[m][0][1] or bullet_y - n == fleet_board[m][0][1]:
                                for o in range(8):
                                    if bullet_axis + o == fleet_board[m][0][0] or bullet_axis - o == fleet_board[m][0][0]:
                                         fleet_board_remove.append(fleet_board[m])
                for l in range(len(fleet_board_remove)):
                    fleet_board.remove(fleet_board_remove[l])
                if fleet == [] and fleet_board == []:
                    top_down_ship = False
                    raid_end = True
                    draw_text_blocks('Attackers Defeated')
                check_ship(ship)
                redraw_screen(0, 0.1)
    
    def distress_call(crew, ship):
        if len(crew) < 6:
            draw_text_blocks('You hear a distress call from a stranded ship on your radio, the remaining crew offer to join you if rescued.')
            draw_text_blocks('What do you do?')
            yes_no = menu(['Rescue Them', 'Leave Them'])
            if yes_no == 'Rescue Them':
                betrayl_chance = random.randint(1,5)
                if betrayl_chance == 1:
                    draw_text_blocks('The distress call seems to have been a trap set by robbers')
                    robbery(crew, ship)
                else:
                    name = random.choice(['Urneveku', 'Isheveki', 'Jason', 'Laverna', 'Mason', 'Varspin', 'Alakx', 'Umeka'])
                    for i in range(len(crew)):
                        while name == crew[i][0]:
                            name = random.choice(['Urneveku', 'Isheveki', 'Jason', 'Laverna', 'Mason', 'Varspin', 'Alakx', 'Umeka'])
                    draw_text_blocks('They are grateful that you rescued them')
                    for i in range(random.randint(2,3)):
                        name = random.choice(['Urneveku', 'Isheveki', 'Jason', 'Laverna', 'Mason', 'Varspin', 'Alakx', 'Umeka'])
                        for j in range(len(crew)):
                            while name == crew[j][0]:
                                name = random.choice(['Urneveku', 'Isheveki', 'Jason', 'Laverna', 'Mason', 'Varspin', 'Alakx', 'Umeka'])
                        create_character(name, crew)

                
        else:
            draw_text_blocks('You leave them behind')
            
        return crew, ship
        
    def buisness_ship(crew, ship, money):
        draw_text_blocks('You encounter a large unarmed ship, it radios to you and says;')
        ship_names = ['Archon', 'Urnevekenes', 'Argo']
        ship_number = random.randint(1,100)
        ship_name = random.choice(ship_names)
        ship_text = str('Welcome to the trade ship ' + ship_name + ' ' + str(ship_number) + ' we are pleased to welcome you')
        draw_text_blocks(ship_text)
        draw_text_blocks('What would you like to do?')
        choice = menu(['Trade', 'Move On'])
        stock_amount = random.randint(2,4)
        in_stock = []
        items = get_all_items()
        for i in range(stock_amount):
                item = random.choice(items)
                items.remove(item)
                in_stock.append(item)
        while choice == 'Trade':
            draw_text_blocks('You must choose a trader')
            trader = stat_comparison_menu(crew, 'social')
            trader_skill = get_character_stat(trader, 'social')
            if check_for_item_by_crew(crew, 'Jumpsuit') == False:
                draw_text_blocks('they wont let you aboard the ship naked, try to find a jumpsuit')
            else:
                BuySell = menu(['Buying', 'Selling'])
                if BuySell == 'Buying':
                    shopping = True
                    while shopping:
                        menu_text = []
                        for i in range(len(in_stock)):
                            menu_text.append(str(in_stock[i][0] + ' ' + str(in_stock[i][2])))
                            menu_text_back = menu_text
                            menu_text_back.append('Back')
                            item = menu(menu_text, 'Buying:')
                            for j in range(len(in_stock)):
                                if in_stock[j][0] in item:
                                    item_description = in_stock[j][3]
                                    price = in_stock[j][2]
                                    draw_text_blocks(item_description)
                                    break
                            if item != 'Back':
                                yes_no = menu(['Yes', 'No'], 'Prchse?')
                                if yes_no == 'Yes':
                                    if price > money:
                                        draw_text_blocks('You dont have enough money')
                                    else:
                                        money -= price
                                        draw_text_blocks('Thank You for your Purchase')
                                        draw_text_blocks('Who do u want to hold/wear this item?')
                                        names = get_crew_names(crew)
                                        holder_name = menu(names)
                                        holder = get_crew_member_by_name(crew, holder_name)
                                        for l in range(len(in_stock)):
                                            if in_stock[l][0] in item:
                                                item = in_stock[l][0]
                                        holder = give_item(item, holder)
                                        for k in range(len(crew)):
                                            if crew[k][0] == holder[0]:
                                                crew[k] = holder
                                        choice = menu(['Yes', 'No'], 'Anything Else?')
                                    if choice == 'Yes':
                                        pass
                                    else:
                                        shopping = False
                                        choice == 'Done'
                                        return crew, ship, money
                                else:
                                    menu_text = []
                            else:
                                shopping = False
                                choice == 'Done'
                                return crew, ship, money
                else:
                    draw_text_blocks('What would you like to sell?')
                    shopping = True
                    while shopping:
                        your_items = get_full_inventory(crew)
                        sellable = []
                        sellable_menu = []
                        prices = []
                        for i in range(len(your_items)):
                            price = int(int(your_items[i][0][2])//2) + trader_skill
                            sellable.append(your_items[i][0])
                            sellable_menu.append(str(your_items[i][0][0]) + ' ' + str(price))
                            prices.append(price)
                        sellable_back = sellable_menu
                        sellable_back.append('Back')
                        to_sell = menu(sellable_back, 'Selling')
                        if to_sell != 'Back':
                            for i in range(len(sellable)):
                                    for j in range(len(crew)):
                                        if sellable[i][0] in to_sell:
                                            if check_for_item_by_crew(crew, sellable[i][0]):
                                                crew = remove_item(sellable[i], crew[j], crew)
                                                money += prices[i]
                                                draw_text_blocks('Item Sold')
                                        shopping = False
                                        choice == 'Done'
                                                
                        else:
                            return crew, ship, money
                        time.sleep(0.1)
        return crew, ship, money
            
        
# The next two functions are placeholder functions for the planet system, they have no use other than for testing purposes         
    def generate_planet():
        planet_names = ['Notera', 'Crynato', 'Vexianixis', 'Gatark', 'Crykador', 'Gidone', 'Falizia', 'Nexia']
        planet  = random.choice(planet_names)
        return planet
        
        
    def planet_near(crew, ship):
        planet = generate_planet()
        if planet == 'Gidone':
            GidoneLandingSequence(crashed=False)
        elif planet == 'Notera':
            NoteraLandingSequence(crashed=False)    
            
    def award_money(money):
        found_amount =  random.randint(50,300)
        money += found_amount
        draw_text_blocks(str('You find ' +  str(found_amount) + ' money on the wrecked enemy ships'))
        return money
        
    def generate_event(crew, ship, money):
        is_event = random.randint(1,3)
        if is_event == 1:
            events = ['Raid', 'Bloatworms', 'Robbery', 'Buisness Ship', 'Distress Signal']
            event = random.choice(events)
            if event == 'Raid':
                raid(crew, ship)
                money = award_money(money)
            elif event == 'Bloatworms':
                severity = random.randint(1,5)
                give_disease('bloatworms', random.choice(crew), severity)
            elif event == 'Buisness Ship':
                crew, ship, money = buisness_ship(crew, ship, money)
            elif event == 'Maintnence Port':
                port(crew, ship, money)
            elif event == 'Planet Near':
                planet_near(crew, ship)
            elif event == 'Distress Signal':
                crew, ship = distress_call(crew, ship)
            elif event == 'Robbery':
                robbery(crew, ship)
                money = award_money(money)
            elif event == 'Debris':
                debris(crew, ship)
        return crew, ship, money
            
    def warning(ship):
        # BITMAP: width: 10, height: 10
        warning_logo = bytearray([63,223,239,247,67,67,247,239,223,63,
       0,1,1,1,0,0,1,1,1,0])
        if ship[4] < 30 or ship[3] < 30:
            warn_page = True
            while warn_page:
                thumby.display.blit(warning_logo, 30, 10, 10, 10, 1, 0, 0)
                if ship[4] >= 10:
                    thumby.display.drawText('Food Lvl Low', 0, 20, 0)
                elif ship[4] < 10:
                    thumby.display.drawText('Food Lvl Crtcl', 0, 20, 0)
                if ship[3] >= 10:
                    thumby.display.drawText('Oxy Lvl Low', 0, 30, 0)
                elif ship[3] < 10:
                    thumby.display.drawText('Oxy Lvl Crtcl', 0, 20, 0)
                redraw_screen(1, 0.2)
                warn_page = check_escape()
        return ship
     
    def end_screen(cause):
        draw_text_blocks(str('Game Over, Cause Of Death ' + cause))
        redraw_screen(1, 10)
        main()
            
    def change_day(day, ship, crew):
        day += 1
        for i in range(len(crew)):
            character = crew[i]
            consume_food(character, ship)
            ship[3] -= 1
            progress_all_diseases(character)
                    
        if ship[4] < 0:
            end_screen('Starvation')
        elif ship[3] < 0:
            end_screen('Lack of Oxygen')
        if emulator == False:
            save_game(crew, ship, money, day)
        return day, ship
         
            
    #def distress_call(crew, ship):
    def playing(crew, ship, money, day):
        running = True
        day_since_event = 0
        while running:
            draw_stars(12)
            day_text = str('Day:' + str(day))
            money_text = str('Mny:' + str(money))
            thumby.display.drawText(day_text, 1, 30, 1)
            thumby.display.drawText(money_text, 30, 30, 1)
            ship_img = bytearray([136,112,126,124,120,112,112,96,96,96])
            thumby.display.blit(ship_img, 20, 20, 10, 8, 0, 0, 0)
            redraw_screen(0, 0.2)
            if thumby.buttonB.pressed():
                crew, ship, money = main_menu(crew, ship, money)
            elif thumby.buttonA.pressed():
                day, ship = change_day(day, ship, crew)
                warning(ship)
                crew, ship, money = generate_event(crew, ship, money)
    crew = []
    intro()
    crew, ship, money, day = save_state_menu(crew)
    playing(crew, ship, money, day)
while running == True:
    main(emulator)
