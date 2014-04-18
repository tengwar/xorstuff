from moduleBaseClass import ModuleBaseClass
from StringIO import StringIO
from PIL import Image

class Module(ModuleBaseClass):
    def __init__(self):
        self.header = 'x42\x4d'
        self.name = 'bmp'

    def final_check(self, raw):
        try:
            Image.open(StringIO(raw))
            return True
        except:
            return False
