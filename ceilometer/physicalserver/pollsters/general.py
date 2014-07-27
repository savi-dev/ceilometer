#
# Copyright (C) 2014, The SAVI Project.
#
# @author: Jieyu Lin <Jieyu.lin@savinetwork.ca>

from ceilometer.physicalserver import plugin
from ceilometer.openstack.common import log
from ceilometer import sample
from ceilometer.physicalserver.utils import make_sample
import psutil

LOG = log.getLogger(__name__)

_BOOT_TIME = 'running_time'

class generalBoottime (plugin.PhyServerPollster):
    def get_samples(self, cache):
        LOG.info('polling running time of the physical server')
        resource_id = 'server_'+cache['host_name']
        sample_list = []
        
        name = _BOOT_TIME
        boot_time = psutil.get_boot_time()
        
        sample_list.append(make_sample(name, sample.TYPE_CUMULATIVE, 'seconds', boot_time, resource_id))
        
        return sample_list
    