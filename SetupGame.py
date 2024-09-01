import time
from CPlayer import *
from Map import *

def cls():
    '''macht die Funktion, die clear erfüllt, nutzbar auf linux-basierten Systemen, sowie Windows-Systemen'''
    #gefunden auf:
    #https://stackoverflow.com/questions/2084508/clear-terminal-in-python
    os.system('cls' if os.name=='nt' else 'clear') 

def fprint(str, t=0.05):
    """gibt Strings gestückelt nach in einzelne Buchstaben nach der Zeit t aus"""
    for character in str:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(t)

def setup_player_name():
    '''fragt den Spieler durch input nach dem Namen und gibt ihn zurück'''
    fprint("Hallo, wie soll ich dich nennen?\n")
    name = input("> ")
    while name == "":
        print("Du musst einen Namen eingeben.")
        name = setup_player_name()
    return name.title()

def setup_player_gender():
    '''fragt den Spieler durch input nach dem Geschlecht und gibt es zurück'''
    valid_f = ["f","w","weiblich","frau","feminin"]
    valid_m = ["m",u"männlich","mann","maskulin"]
    fprint("Welches Geschlecht möchtest du haben?\n")
    player_gender = input("> ")
    if player_gender.lower() in valid_f:
        gender = "w"
    elif player_gender.lower() in valid_m:
        gender = "m"
    else:
        print("Dieser Begriff ist nicht bekannt. Wähle zwischen weiblich oder männlich")
        return setup_player_gender()
    return gender

def setup_player_job(my_player):
    '''fragt den Spieler durch input nach der Rolle und gibt diese zurück'''
    fprint(u"Welche Rolle möchtest du spielen?\n")
    text = {"w" : ["(Du kannst Polizistin, Krankenpflegerin oder Chemielaborantin sein.)\n", "Du bist nun eine "],
           "m" : ["(Du kannst Polizist, Krankenpfleger oder Chemielaborant sein.)\n","Du bist nun ein "]}
    print(text[my_player.gender][0])
    job = setup_player_job_helper(my_player)
    while job == None:
        print(u"Ungültiger Jobname")
        job = setup_player_job_helper(my_player)
    fprint(text[my_player.gender][1] + job + "!\n\n")
    return job

def setup_player_job_helper(my_player):
    '''verarbeitet das Geschlecht im Bezug auf die Jobbezeichnung und gibt diese zurück'''
    player_job = input("> ").lower()
    dict_jobs = my_player.dict_valid_jobs
    #ermöglicht als Eingabe auch nur den Anfangsbuchstaben einzugeben, nicht möglich, wenn Rollen den gleichen Anfangsbuchstaben hätten und man diesen als key im Dictionary verwendet
    if player_job in dict_jobs.keys(): 
        if my_player.gender is "m":
            return dict_jobs[player_job][0].title() #hier wird die 'männliche' Rollenbezeichnung ausgegeben
        else:
            return (dict_jobs[player_job][1]).title() #hier wird die 'weibliche' Rollenbezeichnung ausgegeben
    for item in dict_jobs: #prüft ob der Input des Spielers im Dictionary vorkommt
        for job in dict_jobs[item]: 
            if player_job == job:
                return player_job.title() #gibt den Input des Spielers mit dem ersten Buchstaben groß geschrieben aus


def setup_game():
    """routine für die Charakter-Erstellung als player-Objekt
    gibt den erstellten Spieler zurück
    """
    my_player = player()

    cls()
    my_player.name = setup_player_name()
    my_player.gender = setup_player_gender()
    my_player.set_job(setup_player_job(my_player))     

    if my_player.gender is "w":
        fprint("Willkommen, " + my_player.name + " die " + my_player.job + ".\n")
    elif my_player.gender is "m":
        fprint("Willkommen, " + my_player.name + " der " + my_player.job + ".\n")

    input(u"\nDrücke Enter um fortzufahren...\n")
    fprint("""Vor kurzem war ein Brief von deiner Tante Marion in der Post.
Seltsam...von ihr hast du seit Jahren nichts mehr gehört...
Ob sie wohl überhaupt noch lebt?""")
    input(u"\nDrücke Enter um fortzufahren...\n")
    print("#"*70+'\n')
    if my_player.gender is "w":
        fprint("Liebe " + my_player.name + ",")
    elif my_player.gender is "m":
        fprint("Lieber " + my_player.name + "," )
    fprint("""\n\nwenn du diesen Brief bekommst, dann bin ich vermutlich tot.
Erinnerst du dich an die gute Zeit, die wir hatten, als du ein Kind warst?
Du hast Onkel Herbert und mich immer gern besucht. Ich denke gern daran,
wie du im Garten mit unserer Katze Cleo gespielt hast.
Du bekommst diesen Brief, weil ich dir unser Haus vermachen möchte. Ich
muss dich aber vorwarnen. Das Haus hütet ein Geheimnis.
Es gibt ein Amulett, dass in der Familie seit Jahrhunderten
vererbt wird. Vielleicht kannst du das Geheimnis ergründen?

In Liebe,
Tante Marion\n""")
    input(u"\nDrücke Enter um fortzufahren...\n")
    print("#"*70+'\n')
    fprint(u"Willkommen in der kleinen, verwunschenen Stadt namens Grünewalde!\n" , 0.03)
    fprint(u"Sieht aus, als hätte Tante Marion einen angenehmen Ort zum wohnen gewählt!\n" , 0.03)
    fprint(u"Doch irgendwas scheint merkwürdig zu sein...\n" , 0.1)
    fprint("Liegt es an diesem Geheimnis...?\n\n" , 0.2)
    print("#"*70+'\n')
    input(u"Drücke Enter um zu starten...")

    cls()
    print("#"*70)
    print(" "*10+ "##### Lass uns das Geheimnis ergründen #####"+ " "*10)
    print("#"*70)
  
    return my_player

def debug_setup_game_settings():
    '''setzt Charakterattribute, damit die Charakter-Erstellung übersprungen werden kann und gibt diese zurück'''
    my_player = player()

    my_player.name = "Demo"
    my_player.set_job("Chemielaborantin") 
    my_player.gender = "weiblich"
    print("Du befindest dich im Debug-Modus. Dein Name ist " + my_player.name + ", deine Rolle " + my_player.job + " und dein Geschlecht " + my_player.gender + ".\n Deine aktuellen Werte sind HP = " + str(my_player.hp) + " und MP = " + str(my_player.mp) + ".\n")
    return my_player

def final_credits(my_player):
    """gibt den Abspann je nach Bedingung aus"""
    print("""                        
                  `;   '                   
                   +   +                   
                   .:  +                   
                    ' ,,                   
                    ' '                    
                    `:'                    
                    ;'+`                   
                   `#@@@                   
                   ##+'@`                  
                  .,:+':,`                 
                `::::+;:,,,`               
               .,:,,:+':,,,,.              
              `:::::;#+:,,,,:.             
              ::::::;#+:,,,,,,             
             `::::::;##:,,,:,:`            
             '::::::;#@::::,,::            
             '::::::#@;`:::,,::            
             '::::::    ::::,:;            
             +::::::,  ,::::,:;            
             ;:::::::::,::::,:;            
              ;:::::::::::::::             
              +,:::::::::::,:#             
               +::::`...::::+              
               `+:,:,:,::::#               
              `  #',,,:,,'+                
                   '####;                                                              
    """)
    txt_jobspec = """Das muss das Amulett sein, dass Tante Marion in ihrem Brief erwähnte. 
Als du das Amulett anfasst, kommt ein Geist daraus hervor und greift dich an. 
Du hast nichts im Inventar, womit du dir helfen könntest. Also versuchst du 
den Geist in einem wilden Faustkampf zu überwältigen."""

    if (my_player.job is "Polizistin" or "Polizist") and "Messer" in my_player.inventory:
        txt_jobspec = """Das muss das Amulett sein, dass Tante Marion in ihrem Brief erwähnte. 
Als du das Amulett anfasst, kommt ein Geist daraus hervor und greift dich an. 
Ganz deinem Instinkt nach, greifst du zu dem Messer in deinem Inventar und überwältigst den Geist."""

    elif (my_player.job is "Chemielaborantin" or "Chemielaborant") and "Säure" in my_player.inventory:
        txt_jobspec = """Das muss das Amulett sein, dass Tante Marion in ihrem Brief erwähnte. 
Als du das Amulett anfasst, kommt ein Geist daraus hervor und greift dich an. 
Ganz deinem Instinkt nach, greifst du zu der Säure in deinem Inventar und 
schüttest sie dem Geist ins Gesicht. Die Säure bewirkt, was du dir erhofft hast. """
        
    elif (my_player.job is "Krankenpflegerin" or "Krankenpfleger") and "Desinfektionsmittel" in my_player.inventory:
        txt_jobspec = """Das muss das Amulett sein, dass Tante Marion in ihrem Brief erwähnte. 
Als du das Amulett anfasst, kommt ein Geist daraus hervor und greift dich an. 
Ganz deinem Instinkt nach, greifst du zu dem Desinfektionsmittel in deinem Inventar 
und schüttest es dem Geist ins Gesicht."""
        
    fprint(txt_jobspec + """ Du kannst den Geist besiegen und er löst sich auf. 
Eine große Nebelwolke entsteht und du versuchst durch den Nebel etwas zu sehen. 
Als er sich verflüchtigt, siehst du Onkel Herbert! 
Er erzählt dir, dass der Fluch des Amuletts schon seit Jahren auf der Familie 
lastet. Doch Tante Marion und er haben den Geist so verärgert, dass er Tante
Marion in den Wahnsinn getrieben hat und ihn schlussendlich im Amulett 
eingeschlossen und das Haus besetzt hat. Jetzt endlich ist der Fluch gebrochen!\n""")
    input(u"\nDrücke Enter um zurück zum Hauptmenü zu kommen...")