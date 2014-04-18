from moduleBaseClass import ModuleBaseClass
from PIL import Image
from StringIO import StringIO

class Module(ModuleBaseClass):
    def __init__(self):
        self.header = '\xFF\xD8\xFF\xE1'
        self.name = 'jpg'

    def final_check(self, raw):
        try:
            Image.open(StringIO(raw))
            return True
        except:
            return False
