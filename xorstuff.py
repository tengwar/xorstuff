import itertools
from itertools import izip, cycle, product
import os
import string
import glob
from moduleBaseClass import ModuleBaseClass
from operator import itemgetter

class XorStuff:

    def __init__(self, filepath=None):
        """Constructor : set xored file (optional)

        """
        self.file_type = None
        self.list_types = self.load_files_types('modules/')
        if filepath is not None:
            self.file_content = set_file_content(filepath)

    def load_files_types(self, path):
        """Load all modules from modules/ and make them available

        """
        list_types = {}
        files = glob.glob(path + "*")
        for file in files:
            file_name, file_extension = os.path.splitext(file)
            if not file_name.endswith("__init__") and file_extension == ".py":
                module_name = file_name.replace("/", ".")
                mod = __import__(module_name)
                modules = module_name.split('.')
                for module in modules[1:]:
                    mod = getattr(mod, module)
                    if issubclass(mod.Module, ModuleBaseClass):
                        instance = mod.Module()
                        list_types[instance.name] = instance
        return list_types

    def xor(self, data, key, file_type=None):
        """Perform a simple xor with data and key
           file_type is an instance of modules and provide file checking

        """
        result = []
        for data, char_key in izip(data, cycle(key)):
            byte = chr(ord(data) ^ ord(char_key))
            if file_type is not None:
                if not file_type.live_check(byte):
                    return None
            result.append(byte)
        return ''.join(result)

    def set_file_content(self, filepath, length=None):
        """Open xored file and store content
           Optional : can store n bytes only
        """
        bin_file = ''
        with open(filepath, "rb") as f:
            byte = f.read(1)
            index = 0
            while byte != "":
                bin_file = bin_file + byte
                byte = f.read(1)
                if length is not None:
                    if index == length:
                        break
                    index = index + 1
        self.file_content =  bin_file

    def get_pass(self, key_length, grep=None):
        """Try to recover key(s) for a given length and yield them
           Optional : can grep bytes in result
        """
        # Padding of header with %s if key length > header length
        if int(key_length) > len(self.file_type.header):
            self.file_type.header = "%s%s" % (self.file_type.header, '%s' * (int(key_length) - len(self.file_type.header.replace('%s', '?'))))

        bf_length = self.file_type.header.count('%s')
        bin_header = self.file_content[:-len(self.file_type.header.replace('%s', '?'))]

        charset = ''.join([chr(i) for i in range(128)])
        key_charset = string.ascii_letters + string.digits + string.punctuation

        # generate keys
        for char in itertools.product(charset, repeat=bf_length):
            generated_header = self.file_type.header % char
            output = self.xor(bin_header, generated_header)
            key = output[0: key_length]
            if not [c for c in key if c not in key_charset]:
                raw = self.xor(self.file_content, key, self.file_type)
                if raw is not None:
                    if self.file_type.final_check(raw):
                        if grep is not None:
                            if grep in raw:
                                yield key
                        else:
                            yield key

    def set_file_type(self, file_type):
        """Load correct file type module according to file extension name

        """
        self.file_type = self.list_types[file_type]
