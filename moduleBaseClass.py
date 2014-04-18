class ModuleBaseClass:
    def __init__(self):
        """Init file properties

        """
        self.header = None # Surcharge Me
        self.name= None # Surcharge Me

    def final_check(self, raw):
        """Check performed after the full file is generated

        """
        raise 'Not Implemented'

    def live_check(self, raw):
        """Check performed during the xor process

        """
        raise 'Not Implemented'
