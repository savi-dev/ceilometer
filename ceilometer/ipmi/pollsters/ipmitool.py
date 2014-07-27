#
# Copyright (C) 2014, The SAVI Project.
#
# @author: Jieyu Lin <Jieyu.lin@savinetwork.ca>

from ceilometer.ipmi import plugin
from ceilometer.openstack.common import log
from ceilometer import sample

LOG = log.getLogger(__name__)




class cpuTime (plugin.ImpiPollster):
    def get_samples(self, cache):
        LOG.info('polling IPMI information for server: %s', cache['host_ip'])
        host = cache['host_ip']
        username = cache['username']
        password = cache['password']
        
        sample_list = []
        
        #get a list of cpu times
        

        return sample_list

