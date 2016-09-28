from __future__ import absolute_import

import logging
import sys
from volttron.platform.agent import utils
from volttron.platform.vip.agent import Core
from pnnl.pubsubagent.pubsub.agent import PubSubAgent
import gevent


utils.setup_logging()
log = logging.getLogger(__name__)


class DirectorAgent(PubSubAgent):
    

    def __init__(self, config_path, **kwargs):
        self.marketPeriod = 5
        self.reservationDelay = 0
        self.offerDelay = 2
        self.clearDelay = 2
        super(DirectorAgent, self).__init__(config_path, **kwargs)


    @Core.receiver('onsetup')
    def setup(self, sender, **kwargs):
        super(DirectorAgent, self).setup(sender, **kwargs)
        self.core.periodic(self.marketPeriod, self.trigger)
    

    def trigger(self):
        gevent.sleep(self.reservationDelay)
        self.sendCollectReservationsRequest()
        gevent.sleep(self.offerDelay)
        self.sendCollectOffersRequest()
        gevent.sleep(self.clearDelay)
        self.sendClearRequest()
   
   
    def sendCollectReservationsRequest(self):
        self.output('collectReservationsRequest', 'value', {'collectReservations' : True})
        self.publish(self.output('collectReservationsRequest')) 
    
    
    def sendCollectOffersRequest(self):
        self.output('collectOfferRequest', 'value', {'collectOffers' : True})
        self.publish(self.output('collectOfferRequest'))
        
        
    def sendClearRequest(self):
        self.output('clearRequest', 'value', {'clear' : True})
        self.publish(self.output('clearRequest'))
                   

def main(argv=sys.argv):
    '''Main method called by the eggsecutable.'''
    try:
        utils.vip_main(DirectorAgent)
    except Exception as e:
        log.exception(e)


if __name__ == '__main__':
    # Entry point for script
    sys.exit(main())
