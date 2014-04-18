class ModuleBaseClass:
    def __init__(self):
        self.header = None # Surcharge Me
        self.name= None # Surcharge Me

    def check(self, raw):
        raise 'Not Implemented'
