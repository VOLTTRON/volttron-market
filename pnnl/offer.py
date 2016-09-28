'''
'''


class Offer(object):

    HUGE = 1E6
    HUGEPOS = HUGE
    HUGENEG = -HUGE
    BUY = 'BUY'
    SELL = 'SELL'

    def __init__(self, offer_type, commodity, curve):
        self.__type = offer_type
        self.__commodity = commodity
        self.__curve = curve

    def type(self):
        return self.__type

    def commodity(self):
        return self.__commodity

    def curve(self):
        return self.__curve