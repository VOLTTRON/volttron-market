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
