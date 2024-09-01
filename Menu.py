import sys
from Map import *
from Textadventure import *

def title_screen_selections():
    '''verarbeitet die validen Optionen im Titelbild'''
    option = input("> ")
    if option.lower() not in ['spielen','tutorial','beenden']:
        print(u"Bitte gib einen gültigen Befehl ein.")  
    elif option.lower() == ("spielen"):
        return False
    elif option.lower() == ("tutorial"):
        help_menu()
    elif option.lower() == ("beenden"):
        sys.exit()
    return True

def title_screen():
    """gibt das Titelbild aus"""
    cls()
    print("#############################################################################")
    print("""
   _____          .__  __                  _________       .__                
  /  _  \   _____ |__|/  |______    ____   \_   ___ \ __ __|  | ___________   
 /  /_\  \ /     \|  \   __\__  \ _/ __ \  /    \  \/|  |  \  | \____ \__  \  
/    |    \  Y Y  \  ||  |  / __ \\  ___/  \     \___|  |  /  |_|  |_> > __ \_
\____|__  /__|_|  /__||__| (____  /\___  >  \______  /____/|____/   __(____  /
        \/      \/              \/     \/          \/           |__|       \/
""")
    print("#########################  DAS AMULETT DER LEERE  ###########################")
    print("#############################################################################")
    print("                                -Spielen-                                    ")
    print("                                -Tutorial-                                   ")
    print("                                -Beenden-                                    ")

def help_menu():
    """gibt das Hilfe-Menü aus"""
    print("###################################################")
    print("################## AMITAE CULPA ###################")
    print("############## Das Amulett der Leere ##############")
    print("###################################################")
    print("""\nSchreibe deine Kommandos, um sie auszuführen\n
Schreibe bewegen, gehen, schlendern und die jeweilige Richtungsangabe 
(hoch/nördlich, runter/südlich, links/westlich, rechts/östlich),
um zwischen den Räumen zu navigieren.\n
Schreibe den Namen eines Objekts und die jeweilige Aktion, 
die du ausführen möchtest, um mit Objekten zu interagieren.\n
Schreibe umsehen, um die Objekte im aktuellen Raum angezeigt zu bekommen.\n
Schreibe inventar, um dein Inventar einzusehen.
Schreibe beenden, um das Spiel zu beenden.""")

