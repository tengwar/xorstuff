from moduleBaseClass import ModuleBaseClass
from PIL import Image
from StringIO import StringIO

class Module(ModuleBaseClass):
    def __init__(self):
        self.header = '\x89\x50\x4E\x47\x0D\x0A\x1A\x0A'
        self.name = 'png'

    def check(self, raw):
        try:
            Image.open(StringIO(raw))
            return True
        except:
            return False
