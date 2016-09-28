from __future__ import absolute_import

import logging
import sys
from volttron.platform.agent import utils
from volttron.platform.vip.agent import Core
from pnnl.pubsubagent.pubsub.agent import PubSubAgent, Event
from pnnl.offer import Offer
from pnnl.polyline import PolyLineFactory, PolyLine, Point


utils.setup_logging()
log = logging.getLogger(__name__)


class MiddlemanAgent(PubSubAgent):
    

    def __init__(self, config_path, **kwargs):
        super(MiddlemanAgent, self).__init__(config_path, **kwargs)


    @Core.receiver('onsetup')
    def setup(self, sender, **kwargs):
        super(MiddlemanAgent, self).setup(sender, **kwargs)
        Event.post(self.onMatchSellBidRequest, self.sendDemandCurveRequest, self.readySendDemandCurveRequest)
        Event.post(self.onMatchBuyBidRequest, self.sendDemandCurveRequest, self.readySendDemandCurveRequest)
        Event.post(self.onMatchDemandCurveResponse, self.sendBuyBidResponse, self.readySendBuyBidResponse)
        Event.post(self.onMatchBuyClearRequest, self.sendSellBidResponse, self.readySendSellBidResponse)
        self.reset()
        
    
    def reset(self):
        self.activeSellBidResponse = False
        self.activeBuyBidResponse = False
        self.activeDemandCurveRequest = False
        self.demandCurve = None
        self.buyBidCurve = None
        self.sellBidCurve = None
        
        
    def onMatchSellBidRequest(self, peer, sender, bus, topic, headers, message):
        log.info('Received Sell Bid Request: ' + topic + ' ' + str(message[0]))
        # state stuff needs work
        self.activeSellBidResponse = True
        

    def onMatchSellReservationRequest(self, peer, sender, bus, topic, headers, message):
        self.reset()
        log.info('Received Sell Reservation Request: ' + topic + ' ' + str(message[0]))
        commodity = self.output('sellReservationResponse', 'commodity')
        self.output('sellReservationResponse', 'value', {
            'type': Offer.SELL,
            'commodity': commodity,
            'curve': None})
        self.publish(self.output('sellReservationResponse'))
        
        
    def onMatchBuyBidRequest(self, peer, sender, bus, topic, headers, message):
        log.info('Received Buy Bid Request: ' + topic + ' ' + str(message[0]))
        # state stuff needs work
        self.activeBuyBidResponse = True
        
        
    def onMatchBuyReservationRequest(self, peer, sender, bus, topic, headers, message):
        log.info('Received Buy Reservation Request: ' + topic + ' ' + str(message[0]))
        commodity = self.output('buyReservationResponse', 'commodity')
        self.output('buyReservationResponse', 'value', {
            'type': Offer.BUY,
            'commodity': commodity,
            'curve': None})
        self.publish(self.output('buyReservationResponse'))
        

    def onMatchBuyClearRequest(self, peer, sender, bus, topic, headers, message):
        # this is getting caught by the event above!
        log.info('Received Buy Clear Request: ' + topic + ' ' + str(message[0]))
        self.updateTopic(peer, sender, bus, topic, headers, message)
        
    
    def onMatchSellClearRequest(self, peer, sender, bus, topic, headers, message):
        # drop it on the floor b/c we don't really care what happened
        log.info('Received Sell Clear Request: ' + topic + ' ' + str(message[0]))
        self.updateTopic(peer, sender, bus, topic, headers, message)
    
        
    def onMatchDemandCurveResponse(self, peer, sender, bus, topic, headers, message):
        log.info('Received Demand Curve Response: ' + topic + ' ' + str(message[0]))
        self.updateTopic(peer, sender, bus, topic, headers, message)
        self.activeDemandCurveRequest = False
        self.updateDemandCurve()
        
    # the assumption here is that prices flow down through the market without
    # modification. this could change at some point if prices are decoupled from
    # the markets above
    def sendSellBidResponse(self):
        self.activeSellBidResponse = False
        self.updateSellBidCurve()
        self.output('sellBidResponse', 'value', {
            'type': Offer.SELL,
            'commodity': self.output('sellBidResponse', 'commodity'),
            'curve': self.sellBidCurve.tuppleize()})
        self.publish(self.output('sellBidResponse'))


    def sendBuyBidResponse(self):
        self.activeBuyBidResponse = False
        self.updateBuyBidCurve()
        self.output('buyBidResponse', 'value', {
            'type': Offer.BUY,
            'commodity': self.output('buyBidResponse', 'commodity'),
            'curve': self.buyBidCurve.tuppleize()})
        self.publish(self.output('buyBidResponse'))

        
    def sendDemandCurveRequest(self):        
        self.activeDemandCurveRequest = True
        commodity = self.output('demandCurveRequest', 'commodity')
        self.output('demandCurveRequest', 'value', {
            'commodity': commodity})
        self.publish(self.output('demandCurveRequest'))
        
        
    def readySendDemandCurveRequest(self):
        return not self.demandCurve and not self.activeDemandCurveRequest
    
    
    def readySendSellBidResponse(self):
        return self.activeSellBidResponse
    
    
    def readySendBuyBidResponse(self):
        return self.activeBuyBidResponse and self.demandCurve
    
    
    def updateDemandCurve(self):
        arry = self.input('demandCurveResponse', 'value')['curve']
        self.demandCurve = PolyLineFactory.fromTupples(arry)
    
    
    def updateBuyBidCurve(self):
        self.buyBidCurve = self.demandCurve
    
        
    def updateSellBidCurve(self):
        price = self.input('buyClearRequest', 'value')['price']
        curve = PolyLine()
        if price is not None:
            curve.add(Point(self.demandCurve.min_x(), price))
            curve.add(Point(self.demandCurve.max_x(), price))
        else:
            curve.add(Point(None, None))
        self.sellBidCurve = curve


def main(argv=sys.argv):
    '''Main method called by the eggsecutable.'''
    try:
        utils.vip_main(MiddlemanAgent)
    except Exception as e:
        log.exception(e)


if __name__ == '__main__':
    # Entry point for script
    sys.exit(main())
