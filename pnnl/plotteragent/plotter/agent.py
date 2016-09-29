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

from pnnl.pubsubagent.pubsub.agent import SynchronizingPubSubAgent

import numpy as np
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt

utils.setup_logging()
log = logging.getLogger(__name__)


class PlotterAgent(SynchronizingPubSubAgent):
    

    def __init__(self, config_path, **kwargs):
        super(PlotterAgent, self).__init__(config_path, **kwargs)
        self.plot = DynamicPlot()
        self.topics = {}
        

    @Core.receiver('onsetup')
    def setup(self, sender, **kwargs):
        super(PlotterAgent, self).setup(sender, **kwargs)
        counter = 0
        for topic in sorted(self.INPUTS):
            self.topics[topic] = counter
            counter = counter + 1
        self.plot.labels = sorted(self.INPUTS.keys())     
        
    def updateComplete(self):
        if self.allTopicsUpdated():
            self.plotData()
            self.clearLastUpdate()
            self.onUpdateComplete()
            
            
    def onUpdateComplete(self):
        pass
            
            
    def plotData(self):
        data = [float('nan')] * len(self.INPUTS)
        for topic in self.INPUTS:
            value = self.input(topic, 'value') if self.input(topic) else None
            data[self.topics[topic]] = float(value) if value is not None else float('nan')
        self.plot.update(data)


class DynamicPlot():


    def __init__(self):
        self.plt = plt
        self.fig = plt.figure()
        self.plt.ion()
        self.data = None
        self.lines = None
        self.window = None
        self.labels = None
        self.lgnd = None
        self.ax = None
        
        
    def update(self, points):
        ymin = np.nan
        ymax = np.nan
        if self.data == None:
            self.data = []
            self.lines = []
            ax = self.plt.subplot(111)
            ax.autoscale_view('tight')
            for p in range(0, len(points)):
                ymin = np.nanmin([ymin, np.nanmin(points[p])])
                ymax = np.nanmax([ymax, np.nanmin(points[p])])
                d = [points[p]]
                self.data.append(d)
                l, = self.plt.plot(d, label=self.labels[p])
                self.lines.append(l)
            lgnd = self.plt.legend(loc=2, bbox_to_anchor=(1.02, 1), borderaxespad=0, fontsize = 'x-small')
            self.plt.margins(0)
            self.plt.tight_layout()
            self.plt.draw()
            self.plt.pause(0.001)
            box = ax.get_position()
            ext1 = ax.get_window_extent()
            ext2 = lgnd.get_window_extent()
            r = (ext1.width - ext2.width)/ext1.width
            ax.set_position([box.x0, box.y0, box.width*r, box.height])
        else:
            for p in range(0, len(points)):
                self.data[p].append(points[p])
                if self.window is not None and len(self.data[p]) > self.window:
                    del self.data[p][0]
                self.lines[p].set_xdata(np.arange(len(self.data[p])))
                self.lines[p].set_ydata(self.data[p])
                ymin = np.nanmin([ymin, np.nanmin(self.data[p])])
                ymax = np.nanmax([ymax, np.nanmax(self.data[p])])
        if ymin is not np.nan and ymax is not np.nan:
            if ymin == ymax:
                ymin = ymin*0.9
                ymax = ymax*1.1
            self.plt.ylim([ymin, ymax])
        self.plt.xlim([0,len(self.data[0])])
        self.plt.draw()
        #ext2 = self.lgnd.get_window_extent()
        #print ext2.x0, ext2.y0, ext2.width, ext2.height
        self.plt.pause(0.001)
        return True
                   

def main(argv=sys.argv):
    '''Main method called by the eggsecutable.'''
    try:
        utils.vip_main(PlotterAgent)
    except Exception as e:
        log.exception(e)


if __name__ == '__main__':
    # Entry point for script
    sys.exit(main())
