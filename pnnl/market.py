import collections
from polyline import PolyLineFactory as PolyLineFactory, PolyLine as PolyLine
from offer import Offer


class Market(object):
    
    NONE = "NONE"
    AVERAGE = "AVERAGE"
    SUPPLY = "SUPPLY"
    DEMAND = "DEMAND"
    DEMANDHIGH = "DEMANDHIGH"
    
    def __init__(self):
        self.price = None
        self.quantity = None
        self.increment = 100
        self.demandCurve = None
        self.supplyCurve = None
        self.name = None
        self.commodity = None
        self.enoughBuys = False
        self.enoughSells = False
        self.forceSettle = Market.NONE
        self.offers = []

     
    def getDemandCurve(self):
        return self.demandCurve

        
    def getSupplyCurve(self):
        return self.supplyCurve
    

    def settle(self):
        validBuys = []
        validSells = []
        numBuys = 0
        numSells = 0
        # we check to see if we have all of our buys
        for offer in self.offers:
            # is the offer a buy and the correct commodity?
            if offer.type() == Offer.BUY and offer.commodity() == self.commodity:
                numBuys += 1
                if offer.curve() != None:
                    validBuys.append(offer.curve())
    
        # OK, we have all of our buys, now what about the sells?
        # In this type of market, we need to pass the buys to the sellers, so they know how to construct their curves.
        # But I wonder if the price of this market needs to be coupled directly to the market above?                
        for offer in self.offers:
            # is the offer a sell and the correct commodity?
            if offer.type() == Offer.SELL and offer.commodity() == self.commodity:
                numSells += 1
                if offer.curve() != None:
                    validSells.append(offer.curve())

        # do we have enough buys and sells?
        self.enoughBuys = True if (numBuys > 0 and (len(validBuys) == numBuys)) else False
        self.enoughSells = True if (numSells > 0 and (len(validSells) == numSells)) else False
        # we bail because we can't construct the demand curve
        if not self.enoughBuys:
            print self.name, 'does not have enough', Offer.BUY, 'offers.'
            #self.demandCurve = PolyLine()
        else:
            self.demandCurve = PolyLineFactory.combine(validBuys, self.increment)
            #self.demandCurve.add(Point(0.0, self.demandCurve.max_y()))
        # we bail because we can't construct the supply curve
        if not self.enoughSells:
            print self.name, 'does not have enough', Offer.SELL, 'offers.'
            #self.supplyCurve = PolyLine()
        else:
            self.supplyCurve = PolyLineFactory.combine(validSells, self.increment)                                
        # OK, so now we need to find the clearing price
        self.price = None
        self.quantity = None
        if self.enoughBuys and self.enoughSells:
            print self.name, 'has enough', Offer.BUY, 'and', Offer.SELL, 'offers.'
            # make a geometry object from demand curve
            dmnd = self.geomFromCurve(self.demandCurve)
            # make a geometry object from supply curve
            sply = self.geomFromCurve(self.supplyCurve)
            # did the two objects intersect?
            intersection = PolyLine.intersection(dmnd, sply)
            if intersection:
                self.price = intersection[1]
                self.quantity = intersection[0]
            if self.price is not None:
                print self.name, 'clears', offer.commodity(), 'at', str(round(self.price,2))
            else:
                print "Force Settlement Type:", self.forceSettle
                if self.forceSettle == Market.AVERAGE:
                    if sply[-1][1] is not None and dmnd[-1][1] is not None:
                        self.price = (sply[-1][1] + dmnd[-1][1])/2.0
                    elif sply[-1][1] is not None:
                        self.price = sply[-1][1]
                    elif dmnd[-1][1] is not None:
                        self.price = dmnd[-1][1]
                elif self.forceSettle == Market.SUPPLY:
                    if sply[-1][1] is not None:
                        self.price = sply[-1][1]
                elif self.forceSettle == Market.DEMAND:
                    if dmnd[-1][1] is not None:
                        self.price = dmnd[-1][1]
                elif self.forceSettle == Market.DEMANDHIGH:
                    if dmnd[0][0] is not None and dmnd[0][1] is not None and sply[-1][0] is not None and dmnd[0][0] > sply[-1][0]:
                        self.price = dmnd[0][1]
                        print 'demand is right of supply. forcing settlement at', str(self.price)
                if self.price is not None:
                    print self.name, 'forced to settle', offer.commodity(), 'at', str(round(self.price,2))
                else:
                    print self.name, 'did not clear', offer.commodity()
        return self.quantity, self.price
 
        
    def geomFromCurve(self, curve):
        c = curve.tuppleize()
        # Sort by quantity. Should already be sorted, but just in case...
        c.sort(key=lambda t: t[0])
#         first = c[0]
#         if first[0] > 0:
#             c.insert(0, [0,first[1]])
#         last = c[-1]
#         if xVal > 0 and last[1] < xVal:
#             c.append([last[0],xVal])
#         elif xVal < 0 and last[1] > xVal:
#             c.append([last[0],xVal])
        return c


    def clear(self, clearPrice):
        # this updates the clearing price
        self.price = clearPrice
        if clearPrice is not None:
            self.quantity = self.demandCurve.x(clearPrice)
        else:
            self.quantity = None
  
            
    def reset(self):
        # this resets the market
        self.demandCurve = None
        self.supplyCurve = None
        self.price = None
        self.quantity = None
        self.enoughBuys = None
        self.enoughSells = None
        self.offers = []

    
class Participant(object):
    '''
    Very simple market buyer/seller that does nothing.
    '''
    
    def __init__(self):
        self.commodities = collections.OrderedDict()
        self.prices = collections.OrderedDict()

    
    def offer(self):
        offers = []
        for commodity in self.commodities:
            offer = Offer(Offer.BUY, commodity, None)
            offers.append(offer)
        return offers
   
    
    def clear(self, commodity, clearPrice):
        self.prices[commodity] = clearPrice
  
        
    def reset(self):
        for commodity in self.commodities:
            self.prices[commodity] = None
    