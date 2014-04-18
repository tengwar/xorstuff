from moduleBaseClass import ModuleBaseClass
import string

class Module(ModuleBaseClass):
    def __init__(self):
        self.header = ''
        self.name = 'text'

    def final_check(self, raw):
        if not [c for c in raw if c not in string.printable]:
            return True
        else:
            return False

    def live_check(self, byte):
        return (byte in string.printable)
