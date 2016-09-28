from __future__ import absolute_import

import logging
import sys
from volttron.platform.agent import utils
from volttron.platform.vip.agent import Core
from pnnl.pubsubagent.pubsub.agent import PubSubAgent, Event
from pnnl.market import Market, Offer
from pnnl.polyline import PolyLineFactory


utils.setup_logging()
log = logging.getLogger(__name__)


class MarketAgent(PubSubAgent):
    

    def __init__(self, config_path, **kwargs):
        super(MarketAgent, self).__init__(config_path, **kwargs)
        self.market = Market()
        self.offers = {}
        self.reservations = {}
        self.activeDemandCurveRequest = False
        self.activeSupplyCurveRequest = False
        self.activeClearRequest = False
        self.settled = False
        self.quantity = None
        self.price = None
        

    @Core.receiver('onsetup')
    def setup(self, sender, **kwargs):
        super(MarketAgent, self).setup(sender, **kwargs)
        if 'commodity' in self.input('bidResponse'):
            self.market.commodity = self.input('bidResponse', 'commodity')
        if 'properties' in self.config:
            self.market.__dict__.update(self.config['properties'])
        Event.post(self.settle, self.sendClearRequest, self.readySendClearRequest)
        Event.post(self.onMatchBidResponse, self.settle)
        Event.post(self.onMatchBidResponse, self.sendDemandCurveResponse, self.readySendDemandCurveResponse)
        Event.post(self.onMatchBidResponse, self.sendSupplyCurveResponse, self.readySendSupplyCurveResponse)
        Event.post(self.onMatchDemandCurveRequest, self.sendDemandCurveResponse, self.readySendDemandCurveResponse)
        Event.post(self.onMatchSupplyCurveRequest, self.sendSupplyCurveResponse, self.readySendSupplyCurveResponse)
        Event.post(self.onMatchClearRequest, self.sendClearRequest, self.readySendClearRequest)
        
        
        
    def collectOffers(self):
        commodity = self.output('bidRequest', 'commodity')
        self.output('bidRequest', 'value', {'commodity' : commodity})
        self.publish(self.output('bidRequest'))
        
        
    def collectReservations(self):
        self.reset()
        commodity = self.output('reservationRequest', 'commodity')
        self.output('reservationRequest', 'value', {'commodity' : commodity})
        self.publish(self.output('reservationRequest'))
        
        
    def settle(self):
        self.quantity, self.price = self.market.settle()
        #self.settled = (self.quantity is not None and self.price is not None) or (self.quantity is None and self.price is None and self.market.enoughBuys and self.market.enoughSells)
        self.settled = self.market.enoughBuys and self.market.enoughSells
        #print 'settle SETTLED:', self.settled
        #print 'settle ACTIVE:', self.activeClearRequest
        #if self.readySendClearRequest():
            #self.sendClearRequest()
        
        
    def reset(self):
        self.offers = {}
        self.reservations = {}
        self.activeDemandCurveRequest = False
        self.activeSupplyCurveRequest = False
        self.settled = False
        self.quantity = None
        self.price = None
        self.market.reset()
  
  
    def onMatchClearRequest(self, peer, sender, bus, topic, headers, message):
        self.activeClearRequest = True
        log.info('Received clear request from ' + sender)
        #print 'onMatchClearRequest SETTLED:', self.settled
        #print 'onMatchClearRequest ACTIVE:', self.activeClearRequest
        #if self.readySendClearRequest():
        #    self.sendClearRequest()
  
  
    def onMatchCollectReservationsRequest(self, peer, sender, bus, topic, headers, message):
        log.info('Received collect reservations request')
        self.collectReservations()
        

    def onMatchReservationResponse(self, peer, sender, bus, topic, headers, message):
        '''
        might need to do something with timestamps
        '''
        log.info('Received Reservation: ' + sender + ' ' + str(message[0]))
        offer = self.offerFromMessage(message[0])
        self.reservations[sender] = offer
              
        
    def onMatchCollectOffersRequest(self, peer, sender, bus, topic, headers, message):
        self.offers = self.reservations
        self.collectOffers()
        

    def onMatchBidResponse(self, peer, sender, bus, topic, headers, message):
        '''
        might need to do something with timestamps, or making sure that None never overwrites a valid curve
        '''
        log.info('Received Offer: ' + sender + ' ' + str(message[0]))
        offer = self.offerFromMessage(message[0])
        if sender in self.offers: self.offers[sender] = offer
        self.market.offers = self.offers.values()
        
        
    def onMatchDemandCurveRequest(self, peer, sender, bus, topic, headers, message):
        log.info('Received request for demand curve from : ' + sender + ' ' + str(message[0]))
        self.activeDemandCurveRequest = True         
            
            
    def sendDemandCurveResponse(self):
        self.activeDemandCurveRequest = False
        curve = self.market.getDemandCurve().tuppleize()
        commodity = self.output('demandCurveResponse', 'commodity')
        self.output('demandCurveResponse', 'value', {'commodity' : commodity, 'curve':curve})
        self.publish(self.output('demandCurveResponse'))
        
        
    def onMatchSupplyCurveRequest(self, peer, sender, bus, topic, headers, message):
        log.info('Received request for supply curve from : ' + sender + ' ' + str(message[0]))
        self.activeSupplyCurveRequest = True         
            
            
    def sendSupplyCurveResponse(self):
        self.activeSupplyCurveRequest = False
        curve = self.market.getSupplyCurve().tuppleize()
        commodity = self.output('supplyCurveResponse', 'commodity')
        self.output('supplyCurveResponse', 'value', {'commodity' : commodity, 'curve':curve})
        self.publish(self.output('supplyCurveResponse'))
                
    
    def sendClearRequest(self):
        self.activeClearRequest = False
        commodity = self.output('clearRequest', 'commodity')
        self.output('clearRequest', 'value', {"quantity":self.market.quantity, "price":self.market.price, "commodity":commodity})
        self.publish(self.output('clearRequest'))
    
    
    def offerFromMessage(self, message):
        curve = PolyLineFactory.fromTupples(message['curve']) if message['curve'] else None
        return Offer(message['type'], message['commodity'], curve)
        
        
    def readySendDemandCurveResponse(self):
        return self.market.getDemandCurve() and self.activeDemandCurveRequest
    
    
    def readySendSupplyCurveResponse(self):
        return self.market.getSupplyCurve() and self.activeSupplyCurveRequest
    
    
    def readySendClearRequest(self):
        return self.settled and self.activeClearRequest


def main(argv=sys.argv):
    '''Main method called by the eggsecutable.'''
    try:
        utils.vip_main(MarketAgent)
    except Exception as e:
        log.exception(e)


if __name__ == '__main__':
    # Entry point for script
    sys.exit(main())
