from CPlayer import *
from CRoom import *
from CObject import *
import xml.etree.ElementTree as ET
import os, sys

"""
### player starts at a2
----------
|00|a2|00|
----------
|00|b2|00|
----------
|00|c2|00|
----------
|d1|d2|d3|
----------
|00|e2|00|
----------
"""
class Map:

    up = "hoch",u"nördlich","n"
    down = "runter",u"südlich","s"
    left = "links","westlich","w"
    right ="rechts",u"östlich","o"
    my_player = None

    dict_rooms = {}
    dict_doors = {}
    dict_objects = {}

    #die unten stehende Zeile hab ich gefunden auf:
    #https://stackoverflow.com/questions/1296501/find-path-to-currently-running-file
    path = os.path.split(os.path.abspath(os.path.realpath(sys.argv[0])))[0] #stellt den Pfad bereit, in dem die Datei, die gerade ausgeführt wird, liegt
    xml_rooms = path + "/Rooms.xml"

    def create_rooms(self):
        '''erstellt alle Instanzen von c_room aus der XML-Datei und speichert sie im Dictionary dict_rooms'''
        for room in ET.parse(self.xml_rooms).findall("room"): #geht durch den erstellen Baum und sucht alle Elemente 'room'
            dict_valid_directions = {} 
            doors = []
            for direction in room.findall("valid_directions/*"): #sucht in allen Elementen 'room' nach allen Kindknoten des Elements 'valid_directions'
                directiondoor = direction.get("door") #sammelt aus den Attributen der Kindknoten die ID's der Türen
                if directiondoor != 'None': #alle Richtungen die nicht zu einem weiteren Raum führen, werden ausgesiebt
                    doors.append(directiondoor)
                dict_valid_directions[direction.tag] = (direction.text,directiondoor)
            self.dict_rooms[room.find("location").text] = c_room(room.find("name").text, room.find("descriptions").text, dict_valid_directions,doors)

    def create_doors(self):
        '''erstellt alle Instanzen von c_object für die Struktur 'door' aus der XML-Datei und speichert sie im Dictionary dict_doors'''
        for door in ET.parse(self.xml_rooms).findall("doors/door"): #geht durch den erstellten Baum und sucht alle Elemente 'door' in 'doors'
            solved = True #True, da gelöst, wenn kein State
            inputs = []
            outputs = []
            name = ""
            key = ""
            id_ = door.get("id")
            if door.find("name") != None:
                name = door.find("name").text
            for state in door.findall("state"): #geht durch alle Elemente 'door' und sucht darin alle Elemente 'state'
                s = int(state.get("s"))
                solved = False   #wenn es einen State gibt, wird solved auf False gesetzt
                inputs.append([])
                outputs.append([])
                for pos,output in enumerate(state.findall("output")): #geht durch alle Elemente 'state' und sucht darin alle Elemente 'output' 
                    key = output.get("key")
                    outputs[s].append([pos,output.get("change_s") == "True",key,output.text]) #speichert die Position des Outputs, den Trigger für den State-Change, den für das Objekt benötigten Schlüssel und den Output-Text in einer Instanz von c_object im Attribut output
                    inputs[s].append(self.input_option_chooser(output.get("input"), name))
            self.lower_inputs(inputs) #ruft eine Funktion auf, die durch alle Inputs geht und diese mit lower() in Kleinschreibung umsetzt
            self.dict_doors[id_] = c_object(id_, int(door.get("ini_state")), key, inputs, outputs, name, solved)

    def create_objects(self):
        '''erstellt alle Instanzen von c_object für die Struktur 'object' aus der XML-Datei und speichert sie im Dictionary dict_objects'''
        for object_ in ET.parse(self.xml_rooms).findall("objects/object"):
            id_ = object_.get("id")
            if id_ not in self.dict_objects: #da mehrere Objekte in einem Raum (id) sein können, wird zunächst überprüft, ob es die id im Dictionary bereits gibt
                self.dict_objects[id_] = {} #sonst wird diese Stelle des Dictionaries neu angelegt
            name = object_.find("name").text
            inputs = []
            outputs = []
            solved = True   #True, da gelöst, wenn kein oder ein State
            hidden = False
            for state in object_.findall("state"): #geht durch alle Elemente 'object' und sucht darin alle Elemente 'state'
                s = int(state.get("s"))
                inputs.append([])
                outputs.append([])
                if s > 0:
                    solved = False #wenn es mehr als einen State gibt, wird solved auf False gesetzt
                if object_[1].text == None:
                    hidden = True
                for pos,output in enumerate(state.findall("output")): #geht durch alle Elemente 'state' und sucht darin alle Elemente 'output'
                    trigger_i = output.get("trigger_i")
                    trigger_o = output.get("trigger_o")
                    change_s = output.get("change_s") == "True"
                    change_r = output.get("change_r")
                    key = output.get("key")
                    solution = output.get("solution")
                    outputs[s].append([pos,trigger_i,change_s,key,output.text,trigger_o,solution,change_r]) #speichert die Position des Outputs, den Trigger für den State-Change, den für das Objekt benötigten Schlüssel, den Output-Text, den Trigger für ein anderes Objekt, eine mögliche Lösung für das Objekt und den Trigger für einen möglichen Raumwechsel des Objekt in einer Instanz von c_object im Attribut output
                    input_ = output.get("input")
                    if input_ != None:
                        inputs[s].append(self.input_option_chooser(input_, name))
            self.lower_inputs(inputs) #ruft eine Funktion auf, die durch alle Inputs geht und diese mit lower() in Kleinschreibung umsetzt
            self.dict_objects[id_][name] = c_object(id_, 0, key, inputs, outputs, name, solved, hidden)

    def lower_inputs(self, inputs):
        '''Funktion, die durch alle Inputs geht und diese mit lower() in Kleinschreibung umsetzt'''
        for x,a in enumerate(inputs):
            for y,b in enumerate(a):
                for z,i in enumerate(b):
                    inputs[x][y][z]=i.lower()

    def input_option_chooser(self, input_, name):
        '''geht durch alle möglichen Input-Typen und setzt dafür mögliche Variationen für den tatsächlich validen Input des Spielers'''
        if input_ == "examine":
            return [name + " untersuchen", name + " ansehen", name + " anschauen", name + " angucken"]
        elif input_ == "open":
            return [name + " aufmachen", name + " öffnen"]
        elif input_ == "unlock":
            return [name + " aufschließen", name + " aufsperren"]
        elif input_ == "solve":
            return [name + " lösen", name + " knacken", name + " sortieren", name + " anordnen", name + " ordnen"]
        elif input_ == "move":
            return [name + " bewegen"]
        elif input_ == "feed":
            return [name + " füttern", name + " ablenken"]
        elif input_ == "pet":
            return [name + " streicheln"]
        elif input_ == "read":
            return [name + " lesen"]
        elif input_ == "force":
            return [name + " aufstemmen", name + " aufbrechen", name + " aufdrücken"]

    def get_location_text(self):
        '''gibt einen String mit vier Zeilen, bestehend aus Trennzeile, aktuellem Raumnamen, aktuelle Raumbeschreibung und einer weiteren Trennzeile zurück'''
        return "\n" + "#"*70 + "\n" + " "*25 + self.get_current_room().name + "\n\n" + self.get_current_room().descriptions + "\n\n" + "#"*70

    def validate_destination(self, action):
        '''prüft die vom Spieler eingegebene Richtung auf Validität und ruft die Funktion player_move auf oder gibt einen String zurück, falls die Richtung nicht valide ist'''
        destination = None
        if len(action) == 1:
            ask = "Wohin willst du dich bewegen?\n"
            dest = input(ask)
        else:
            dest = action[1]
        direction = ''
        if dest in self.up:
            direction = 'up'
        elif dest in self.down:
            direction = 'down'
        elif dest in self.left:
            direction = 'left'
        elif dest in self.right:
            direction = 'right'
        else:
            return "Keine valide Richtungsangabe"
        return self.player_move(direction)

    def player_move(self, direction):
        '''verarbeitet die Richtungsangabe des Spielers und prüft, ob eventuell eine Tür den Weg versperrt. Wenn nicht, so wird der Standort des Spielers aktualisiert und der dazugehörige Text ausgegeben. Die Funktion gibt einen String zurück.'''
        door_id = self.get_current_room().valid_destinations[direction][1]
        if door_id == "None":
            return "Hier kannst du nicht hingehen."
        
        door = self.dict_doors[door_id]
        str_txt = "Die "+ door.name + " ist verschlossen."
        if door.state != 0:
            self.my_player.location = self.get_current_room().valid_destinations[direction][0]
            str_txt = "\n"+ "Du hast dich nach '"+ self.dict_rooms[self.my_player.location].name + "' bewegt." + "\n" + self.get_location_text()
        return str_txt

    def player_examine(self, action):
        '''behandelt den Input des Spielers und ruft die weiterführenden Funktionen auf'''
        if len(action) == 1:
            ask = "Was möchtest du genau tun?\n"
            cur_action = "".join(action) + " " + input(ask)
        else:
            #setzt den Input des Spielers wieder zu einem String zusammen, falls dieser als eine Liste an die Funktion übergeben wird
            cur_action = action[0] + " " + action[1] 
        
        str_out = self.player_examine_doors(cur_action)
        if str_out == None:  
            #wenn player_examine_doors() None zurück gibt, dann wird player_examine_objects() aufgerufen
            str_out = self.player_examine_objects(cur_action)
        if str_out == None:  
            #wenn player_examine_objects() None zurück gibt, dann wird die Meldung geprintet
            print("In diesem Raum ist die Aktion nicht möglich.")
        else:
            print(str_out)

    def player_examine_doors(self, cur_action):
        '''behandelt den Input des Spielers, falls dieser ein Tür-Objekt betrifft'''
        str_ret = None
        for door in self.get_current_room().doors: #geht durch alle Türen im aktuellen Raum, in dem sich der Spieler befindet
            d = self.dict_doors[door]
            if d.inputs != [] and d.inputs != None:
                for pos, v_action in enumerate(d.inputs[d.state]):
                    state_changer = d.outputs[d.state][pos][1]
                    key = d.outputs[d.state][pos][2]
                    output_text = d.outputs[d.state][pos][3]
                    if cur_action in v_action: #ist der Input Teil der validen Aktionen?
                        if key != None: #wird ein Schlüssel benötigt?
                            selected_key = input("Was möchtest du dafür benutzen?\n")
                            if selected_key.lower() == key.lower():
                                if key in self.my_player.inventory: #ist der Schlüssel im Inventar des Spielers?
                                    self.my_player.remove_from_inventory(key) #entfernt Strings aus dem Inventar des Spielers
                                    self.handle_state_change(d, state_changer) #behandelt den optionalen State-Wechsel
                                    return output_text
                                return "Das Objekt scheint nicht in deinem Inventar zu sein. Benutze 'i' oder 'inventar', um dein Inventar einzusehen."
                            return "Das Objekt '" + d.name + "' bekommst du damit nicht auf."
                        elif key == None: #wird ein kein Schlüssel benötigt?
                            return output_text
        return str_ret #falls keine der Bedingungen zutrifft, wird None zurückgegeben

    def player_examine_objects(self, cur_action):
        '''behandelt den Input des Spielers, falls dieser ein Objekt/einen Gegenstand betrifft'''
        str_ret = None
        obj = self.dict_objects[self.my_player.location]
        for o in obj: #geht durch alle Objekte im aktuellen Raum, in dem sich der Spieler befindet
            for pos, v_action in enumerate(obj[o].inputs[obj[o].state]): #geht durch alle möglichen Inputs
                #die folgenden Variablen speichern die jeweiligen Informationen aus dem Output zwischen
                inventory_obj = obj[o].outputs[obj[o].state][pos][1]        
                state_changer = obj[o].outputs[obj[o].state][pos][2]
                key = obj[o].outputs[obj[o].state][pos][3]
                output_text = obj[o].outputs[obj[o].state][pos][4]
                trigger_o = obj[o].outputs[obj[o].state][pos][5]
                solution = obj[o].outputs[obj[o].state][pos][6]
                room_changer = obj[o].outputs[obj[o].state][pos][7]
                if cur_action in v_action: #ist der Input Teil der validen Aktionen?
                    if key != None: #wird ein Schlüssel benötigt?
                        selected_key = input("Was möchtest du dafür benutzen?\n")
                        if selected_key.lower() == key.lower():
                            if key in self.my_player.inventory: #ist der Schlüssel im Inventar des Spielers?
                                self.my_player.remove_from_inventory(key) #entfernt Strings aus dem Inventar des Spielers
                                if inventory_obj != None: #gibt es ein Objekt, dass ins Inventar (als String) aufgenommen werden soll?
                                    self.my_player.add_to_inventory(inventory_obj) #fügt Strings zum Inventar hinzu
                                #nimmt optional Änderungen am eigentlichen Objekt vor
                                self.handle_change_obj(obj[o], state_changer, trigger_o, room_changer) 
                                return output_text
                            return "Das Objekt scheint nicht in deinem Inventar zu sein. Benutze 'i' oder 'inventar', um dein Inventar einzusehen."
                        return "Das Objekt '" + obj[o].name + "' bekommst du damit nicht auf."
                    if solution != None: #wird eine Lösung benötigt?
                        selected_solution = input("Was möchtest du dafür eingeben?\n")
                        if selected_solution.lower() == solution.lower():
                            if inventory_obj != None: #gibt es ein Objekt, dass ins Inventar (als String) aufgenommen werden soll?
                                    self.my_player.add_to_inventory(inventory_obj) #fügt Strings zum Inventar hinzu
                            #nimmt optional Änderungen am eigentlichen Objekt vor
                            self.handle_change_obj(obj[o], state_changer, trigger_o, room_changer) 
                            return output_text
                        return "Das scheint nicht die richtige Lösung zu sein."
                    elif key == None and solution == None: #wird ein Schlüssel benötigt?
                        if inventory_obj != None: #gibt es ein Objekt, dass ins Inventar (als String) aufgenommen werden soll?
                            self.my_player.add_to_inventory(inventory_obj)
                        self.handle_change_obj(obj[o], state_changer, trigger_o, room_changer)
                        return output_text
                    return 
        return str_ret    

    def handle_change_obj(self, o, state_changer, trigger_o, room_changer):
        '''behandelt die Teile des Outputs, die eine Änderung am eigentlichen Objekt hervorrufen'''
        if state_changer == True: #wird ein State-Wechsel ausgelöst?
            o.state += 1
        if trigger_o != None: #wird ein anderes Objekt angesprochen?
            for element in self.dict_objects:
                if trigger_o in self.dict_objects[element].keys(): #ist das angesprochene Objekt Teil des Dictionaries, in dem alle Objekte gespeichert sind?
                    self.dict_objects[element][trigger_o].hidden = False #Objekt wird sichtbar gemacht
                    self.dict_objects[element][trigger_o].state += 1 #Output wird durch den State-Wechsel zugänglich
        if room_changer != None: #wird ein Raumwechsel ausgelöst?
            for element in self.dict_objects:
                if o.id == element: 
                    #nimmt das Objekt, dass den Raum wechseln soll, aus der Stelle des Dictionaries raus:
                    e = self.dict_objects[element].pop(o.name)
                    #setzt das Objekt an die durch den room_changer vorgegebene Stelle im neuen Dictionary:
                    self.dict_objects[room_changer][o.name] = e 
                    #aktualisiert die Raumbeschreibung:
                    self.dict_rooms[room_changer].descriptions += " Die Katze sitzt miauend und scharrend auf dem Teppich." 
        if o.state == len(o.outputs)-1: #ist der aktuelle State der letzte?
            o.solved = True

    def handle_state_change(self, o, state_changer):
        '''behandelt den State-Wechsel und prüft, ob das betreffende Objekt gelöst ist'''
        if state_changer == True: #wird ein State-Wechsel ausgelöst?
            o.state += 1
        if o.state == len(o.outputs)-1: #ist der aktuelle State der letzte?
            o.solved = True

    def get_current_room(self):
        '''gibt den aktuellen Raum zurück, in dem sich der Spieler befindet'''
        return self.dict_rooms[self.my_player.location]