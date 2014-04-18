from moduleBaseClass import ModuleBaseClass

class Module(ModuleBaseClass):
    def __init__(self):
        self.header = '\x52\x49\x46\x46'
        self.name = 'wav'

    def final_check(self, raw):
        return True
