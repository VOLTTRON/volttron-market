from __future__ import absolute_import

import logging
import sys
from volttron.platform.agent import utils
from volttron.platform.vip.agent import Core
from pnnl.offer import Offer
from pnnl.polyline import PolyLine, Point
from pnnl.pubsubagent.pubsub.agent import PubSubAgent


utils.setup_logging()
log = logging.getLogger(__name__)


class BuyerAgent(PubSubAgent):
    

    def __init__(self, config_path, **kwargs):
        super(BuyerAgent, self).__init__(config_path, **kwargs)


    @Core.receiver('onsetup')
    def setup(self, sender, **kwargs):
        super(BuyerAgent, self).setup(sender, **kwargs)
        
        
    def onMatchReservationRequest(self, peer, sender, bus, topic, headers, message):
        log.info('Received: ' + topic + ' ' + str(message[0]))
        # supposed to make a reservation in the bidding system
        commodity = self.output('reservationResponse', 'commodity')
        self.output('reservationResponse', 'value', {'type': Offer.BUY, 'commodity': commodity, 'curve': None})
        self.publish(self.output('reservationResponse'))
        
        
    def onMatchBidRequest(self, peer, sender, bus, topic, headers, message):
        log.info('Received: ' + topic + ' ' + str(message[0]))
        curve = PolyLine()
        curve.add(Point(0,100))
        curve.add(Point(100,0))
        commodity = self.output('bidResponse', 'commodity')
        self.output('bidResponse', 'value', {'type': Offer.BUY, 'commodity': commodity, 'curve': curve.tuppleize()})
        self.publish(self.output('bidResponse'))
        
    
    def onMatchClearRequest(self, peer, sender, bus, topic, headers, message):
        self.output('shadeSchedule', 'value', 1)
        self.output('extLightSchedule', 'value', 1)
        self.publish(self.output('shadeSchedule'))
        self.publish(self.output('extLightSchedule'))
        

def main(argv=sys.argv):
    '''Main method called by the eggsecutable.'''
    try:
        utils.vip_main(BuyerAgent)
    except Exception as e:
        log.exception(e)


if __name__ == '__main__':
    # Entry point for script
    sys.exit(main())
