
class MatchType:
    """
    Utility class performing a safe cast from generic string to a match type
    """

    TYPE_ALL = 'all'
    TYPE_HOME = 'home'
    TYPE_AWAY = 'away'

    def __init__(self, mtype):
        allowed = (self.__class__.TYPE_ALL, self.__class__.TYPE_AWAY, self.__class__.TYPE_HOME)
        if not mtype in allowed:
            raise ValueError('Unrecoginzed {}, avaiable are: {}'.format(mtype, ', '.join(allowed)))
        self.type = mtype

    def home(self):
        return self.type == self.__class__.TYPE_HOME

    def away(self):
        return self.type == self.__class__.TYPE_AWAY

    def all(self):
        return self.type == self.__class__.TYPE_ALL