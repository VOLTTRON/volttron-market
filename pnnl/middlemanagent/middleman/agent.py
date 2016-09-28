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
