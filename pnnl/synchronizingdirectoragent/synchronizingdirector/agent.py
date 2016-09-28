from __future__ import absolute_import

import logging
import sys
from volttron.platform.agent import utils
from volttron.platform.vip.agent import Core
from pnnl.pubsubagent.pubsub.agent import PubSubAgent, SynchronizingPubSubAgent

utils.setup_logging()
log = logging.getLogger(__name__)


class SynchronizingDirectorAgent(SynchronizingPubSubAgent):
    

    def __init__(self, config_path, **kwargs):
        super(SynchronizingDirectorAgent, self).__init__(config_path, **kwargs)
        
        
    @Core.receiver('onsetup')  
    def setup(self, sender, **kwargs):
        #super(SynchronizingDirectorAgent, self).setup(sender, **kwargs)
        PubSubAgent.setup(self, sender, **kwargs)
        
        
#     def updateTopic(self, peer, sender, bus, topic, headers, message):
#         obj = self.getInputFromTopic(topic)
#         if obj is not None:
#             if not obj.has_key('messageCount'):
#                 obj['messageCount'] = 0
#             obj['messageCount'] = obj['messageCount'] + 1
#         SynchronizingPubSubAgent.updateTopic(self, peer, sender, bus, topic, headers, message)
        
        
    def updateTopic(self, peer, sender, bus, topic, headers, message):
        objs = self.getInputsFromTopic(topic)
        for obj in objs:
            increment = False
            if obj is not None:
                if not obj.has_key('field'): # input does not have a topic
                    increment = True
                elif obj.get('field', None): # input has a topic that is not None
                    if type(message[0]) is dict and message[0].get('field', None) is obj.get('field', None): # got a dict and its field matches the input's
                        increment = True   
                if increment:
                    if not obj.has_key('messageCount'):
                        obj['messageCount'] = 0
                    obj['messageCount'] = obj['messageCount'] + 1
            SynchronizingPubSubAgent.updateTopic(self, peer, sender, bus, topic, headers, message)
        
        
    def clearLastUpdate(self):
        for obj in self.input().itervalues():
            if obj.has_key('messageCount'):
                obj['messageCount'] = 0
        SynchronizingPubSubAgent.clearLastUpdate(self)
        
        
    def allTopicsUpdated(self):
        for obj in self.input().itervalues():
            if obj.has_key('messageCount') and obj.has_key('number'):
                if obj['number'] > obj['messageCount']:
                    return False
        return SynchronizingPubSubAgent.allTopicsUpdated(self)


def main(argv=sys.argv):
    '''Main method called by the eggsecutable.'''
    try:
        utils.vip_main(SynchronizingDirectorAgent)
    except Exception as e:
        log.exception(e)


if __name__ == '__main__':
    # Entry point for script
    sys.exit(main())
