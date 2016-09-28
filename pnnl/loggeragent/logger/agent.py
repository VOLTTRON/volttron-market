from __future__ import absolute_import

import logging
import sys
from volttron.platform.agent import utils
from volttron.platform.vip.agent import Core

from pnnl.pubsubagent.pubsub.agent import PubSubAgent


utils.setup_logging()
log = logging.getLogger(__name__)


class LoggerAgent(PubSubAgent):
    

    def __init__(self, config_path, **kwargs):
        super(LoggerAgent, self).__init__(config_path, **kwargs)
        

    @Core.receiver('onsetup')
    def setup(self, sender, **kwargs):
        super(LoggerAgent, self).setup(sender, **kwargs)
                   

def main(argv=sys.argv):
    '''Main method called by the eggsecutable.'''
    try:
        utils.vip_main(LoggerAgent)
    except Exception as e:
        log.exception(e)


if __name__ == '__main__':
    # Entry point for script
    sys.exit(main())
