from CRoom import *

class player:

    dict_valid_jobs = {"c":["chemielaborant","chemielaborantin"],"k": ["krankenpfleger","krankenpflegerin"], "p": ["polizist","polizistin"]}

    def __init__(self):
        """definiert Voreinstellungen für einen Spieler"""
        self.name = ""
        self.job = ""
        self.gender = ""
        self.hp = 0
        self.mp = 0
        self.location = "a2"
        self.game_over = False
        self.inventory = []

    def set_job(self,str_):
        """setzt die hp- und mp-Werte im Bezug auf die Rolle des Spielers"""
        self.job = str_
        if self.job is "polizist" or "polizistin":
            self.hp = 120
            self.mp = 20
        elif self.job is "chemielaborant" or "chemielaborantin":
            self.hp = 40
            self.mp = 120
        elif self.job is "krankenpfleger" or "krankenpflegerin":
            self.hp = 60
            self.mp = 60

    def get_inventory(self):
        """gibt das Inventar zurück"""
        return self.inventory

    def add_to_inventory(self,str_):
        """fügt einen String zum Inventar hinzu"""
        self.inventory.append(str_)

    def remove_from_inventory(self,str_):
        """entfernt einen String aus dem Inventar"""
        self.inventory.remove(str_)