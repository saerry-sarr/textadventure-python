import sys, os
from Menu import *
from Map import *
from SetupGame import *
from CPlayer import *
from CRoom import *

#die unten stehende Zeile hab ich gefunden auf:
#https://stackoverflow.com/questions/9458870/automatically-resize-command-line-window
os.system("mode con cols=80 lines=40") #nur für das Betriebssystem Windows
debug = False #gesetzt für den Debug-Modus
map = Map()

def main():
    '''Erstellt alle benötigten Objekte im Spiel und ruft das Titelbild auf. Wenn debug auf True gesetzt ist, wird die Funktion für die debug-Einstellungen aufgerufen, sonst die Charaktererstellung. Danach wird die Spiel-Schleife aufgerufen.'''
    map.create_rooms() #erstellt alle Räume aus der XML-Datei
    map.create_doors() #erstellt alle Türen aus der XML-Datei
    map.create_objects() #erstellt alle Objekte aus der XML-Datei
    title_screen() #ruft das Titelbild auf

    while title_screen_selections(): 
        None

    if debug:
        map.my_player = debug_setup_game_settings()
        #map.dict_doors['b2c2'].state = 1
        #map.dict_doors['c1c2'].state = 1
        #map.dict_doors['d2e2'].state = 1
        #map.my_player.add_to_inventory('augenförmiger Rubin')
    else:
        map.my_player = setup_game()
    main_game_loop() #startet die Spiel-Schleife, die läuft, bis das Spiel beendet ist

def prompt():
    '''Teilt den Spieler-Input und prüft die Einzelteile, sodass weitere Funktionen aufgerufen werden können'''
    print ("\n"+ "=======================")
    print(u"Was möchtest du tun?")
    action = input("> ").lower().split(" ") 
    door_obj_list = create_door_obj_list()
    for object in door_obj_list: #geht die Liste von Objekten und Türen durch und schaut, ob der String auch im Input des Spielers vorkommt
        if object.lower() in action:
            map.player_examine(action)
            return
    action_move = ["bewegen","gehen","reisen","spazieren","schlendern","bummeln"]
    action_inventory = ["inventar", "i"]
    action_lookaround = ["umsehen"]
    acceptable_actions = action_move + action_lookaround + action_inventory + ["beenden","hilfe"] #legt alle akzeptierten Inputs fest

    if action[0] == "beenden":
        sys.exit()
    elif action[0] == "hilfe":
        help_menu()
    elif action[0] in action_lookaround:
        print("Die Objekte mit denen du interagieren kannst sind: " + ", ".join(door_obj_list) + ".")
    elif action[0] in action_move:
        print(map.validate_destination(action))
    elif action[0] in action_inventory:
        if map.my_player.get_inventory() == []:
            print("Dein Inventar ist zur Zeit leer.")
        else:
            print(map.my_player.get_inventory())
    else:
        print("Unbekannte Aktion, versuchs's nochmal. Nutze die Hilfe, um zu sehen was du machen kannst.\n")

    if debug == True:     #diese Aktionen sind nur gültig, wenn sich das Spiel im Debug-Modus befindet 
        acceptable_actions += ["debug","solved"]
        if action[0] == "debug":        #debug für den Abspann
            final_credits(map.my_player)
            main()
        if action[0] == "solved":                #debug für das game_over-Attribut, wenn die Einleitung des Abspanns auf das solved-Attribut zurückzuführen ist
            for key in map.dict_doors.keys():
                map.dict_doors[key].solved = True
            for key in map.dict_objects.keys():
                for obj in map.dict_objects[key]:
                    obj.solved = True

def create_door_obj_list():
    '''erstellt eine Liste mit allen Türen und Objekten im aktuellen Raum und gibt diese zurück'''
    door_obj_list = []
    for item in map.dict_objects[map.my_player.location]: #speichert für jeden Raum die darin existierenden Objekte
        if map.dict_objects[map.my_player.location][item].hidden == False:
            door_obj_list.append(item)
    for door in map.dict_rooms[map.my_player.location].doors: #speichert für jeden Raum die darin existierenden Türen
        if map.dict_doors[door].name != "":
            door_obj_list.append(map.dict_doors[door].name)
    return door_obj_list

def main_game_loop():
    '''Spiel-Schleife, die läuft, bis das Spiel beendet ist'''
    print(map.get_location_text())

    while not map.my_player.game_over:
        prompt()
        #map.my_player.game_over = all_doors_solved() and all_objects_solved()      #wieder einkommentieren, um die Einleitung des Abspanns wieder auf das solved-Attribut zurückzuführen
        if 'Amulett der Leere' in map.my_player.inventory: #derzeitige Bedingung für das Ende des Spiels
            map.my_player.game_over = True    
    final_credits(map.my_player)
    main()

if __name__ == "__main__":
    '''behandelt einen übergebenen Parameter, der zum Setzen des Debug-Modus verwendet wird und startet dann das Spiel'''
    print(sys.argv) #sys.argv ist die Liste der Komandozeilen-Argumente
    if len(sys.argv) >= 2:
        if 'True' in sys.argv:
            debug = True
    main()

    #def all_doors_solved():                #wieder einkommentieren, um die Einleitung des Abspanns wieder auf das solved-Attribut zurückzuführen
#    for key in map.dict_doors.keys():
#        if not map.dict_doors[key].solved:
#            return False
#    return True

#def all_objects_solved():              #wieder einkommentieren, um die Einleitung des Abspanns wieder auf das solved-Attribut zurückzuführen
#    for room in map.dict_objects.keys():
#        for obj in map.dict_objects[room].values():
#            if not obj.solved:
#                return False
#    return True