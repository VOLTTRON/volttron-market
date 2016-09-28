from __future__ import absolute_import

import logging
import sys
from volttron.platform.agent import utils
from volttron.platform.vip.agent import Core

from pnnl.pubsubagent.pubsub.agent import SynchronizingPubSubAgent

import numpy as np
import matplotlib
matplotlib.use('Qt4Agg')
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
#             if self.INPUTS[topic].has_key('field'):
#                 value = self.input(topic)['value'][self.INPUTS[topic]['field']]
#             else:
            value = self.input(topic)['value'] 
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
