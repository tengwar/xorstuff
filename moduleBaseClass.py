class ModuleBaseClass:

    def __init__(self):
        """Init file properties

        """
        self.header = None  # Surcharge Me
        self.name = None  # Surcharge Me

    def final_check(self, raw):
        """Check performed after the full file is generated

        """
        return True

    def live_check(self, byte):
        """Check performed during the xor process

        """
        return True
