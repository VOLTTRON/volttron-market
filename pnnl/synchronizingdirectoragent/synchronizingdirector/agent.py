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
