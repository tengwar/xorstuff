from moduleBaseClass import ModuleBaseClass


class Module(ModuleBaseClass):

    def __init__(self):
        self.header = '\x45\x6C\x66\x46\x69\x6C\x65\x00'
        self.name = 'elf'

    def final_check(self, raw):
        return True
