from moduleBaseClass import ModuleBaseClass
import string

class Module(ModuleBaseClass):
    def __init__(self):
        self.header = ''
        self.name = 'text'

    def check(self, raw):
        if not [c for c in raw if c not in string.printable]:
            return True
        else:
            return False
