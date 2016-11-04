# -*- coding: utf-8 -*- {{{
# vim: set fenc=utf-8 ft=python sw=4 ts=4 sts=4 et:
#
# Copyright (c) 2016, Battelle Memorial Institute
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# The views and conclusions contained in the software and documentation are those
# of the authors and should not be interpreted as representing official policies,
# either expressed or implied, of the FreeBSD Project.
#

# This material was prepared as an account of work sponsored by an
# agency of the United States Government.  Neither the United States
# Government nor the United States Department of Energy, nor Battelle,
# nor any of their employees, nor any jurisdiction or organization
# that has cooperated in the development of these materials, makes
# any warranty, express or implied, or assumes any legal liability
# or responsibility for the accuracy, completeness, or usefulness or
# any information, apparatus, product, software, or process disclosed,
# or represents that its use would not infringe privately owned rights.
#
# Reference herein to any specific commercial product, process, or
# service by trade name, trademark, manufacturer, or otherwise does
# not necessarily constitute or imply its endorsement, recommendation,
# r favoring by the United States Government or any agency thereof,
# or Battelle Memorial Institute. The views and opinions of authors
# expressed herein do not necessarily state or reflect those of the
# United States Government or any agency thereof.
#
# PACIFIC NORTHWEST NATIONAL LABORATORY
# operated by BATTELLE for the UNITED STATES DEPARTMENT OF ENERGY
# under Contract DE-AC05-76RL01830

#}}}

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
    