from __future__ import absolute_import

import logging
import sys
from volttron.platform.agent import utils
from volttron.platform.vip.agent import Core
from pnnl.pubsubagent.pubsub.agent import PubSubAgent
from pnnl.offer import Offer
from pnnl.polyline import PolyLine, Point


utils.setup_logging()
log = logging.getLogger(__name__)


class SellerAgent(PubSubAgent):
    

    def __init__(self, config_path, **kwargs):
        super(SellerAgent, self).__init__(config_path, **kwargs)


    @Core.receiver('onsetup')
    def setup(self, sender, **kwargs):
        super(SellerAgent, self).setup(sender, **kwargs)


    def onMatchReservationRequest(self, peer, sender, bus, topic, headers, message):
        log.info('Received: ' + topic + ' ' + str(message[0]))
        # supposed to make a reservation in the bidding system
        commodity = self.output('reservationResponse', 'commodity')
        self.output('reservationResponse', 'value', {'type': Offer.SELL, 'commodity': commodity, 'curve': None})
        self.publish(self.output('reservationResponse'))
    
        
    def onMatchBidRequest(self, peer, sender, bus, topic, headers, message):
        log.info('Received: ' + topic + ' ' + str(message[0]))
        curve = PolyLine()
        curve.add(Point(0,0))
        curve.add(Point(100,100))
        commodity = self.output('bidResponse', 'commodity')
        self.output('bidResponse', 'value', {'type': Offer.SELL, 'commodity': commodity, 'curve': curve.tuppleize()})
        self.publish(self.output('bidResponse'))
                   

def main(argv=sys.argv):
    '''Main method called by the eggsecutable.'''
    try:
        utils.vip_main(SellerAgent)
    except Exception as e:
        log.exception(e)


if __name__ == '__main__':
    # Entry point for script
    sys.exit(main())
