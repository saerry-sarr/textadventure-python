class c_room:

    def __init__(self, name, descriptions, valid_destinations, doors):
        self.name = name
        self.doors = doors
        self.descriptions = descriptions
        self.valid_destinations = valid_destinations
        self.objects = []