from pymongo import MongoClient

class Persistance:
    class __Persistance:
        def __init__(self, arg):
            self.val = arg
        def __str__(self):
            return repr(self) + self.val

    instance = None
    
    def __init__(self, arg):
        if not Persistance.instance:
            Persistance.instance = Persistance.__Persistance(arg)
        else:
            Persistance.instance.val = arg
    def __getattr__(self, name):
        return getattr(self.instance, name)