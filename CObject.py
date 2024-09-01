class c_object:

    def __init__(self, id, state, key, inputs = None, outputs = None, name = None, solved = False, hidden = False):
        self.name = name
        self.id = id
        self.state = state
        self.key = key
        self.inputs = inputs
        self.outputs = outputs
        self.solved = solved
        self.hidden = hidden