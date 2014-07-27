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

_NETWORK_IO = 'phy_network_io'

class networkIO (plugin.PhyServerPollster):
    def get_samples(self, cache):
        LOG.info('polling network IO of the physical server')
        resource_id = 'server_'+cache['host_name']+'_nic_'
        sample_list = []
        
        name = _NETWORK_IO
        network_io = psutil.net_io_counters(pernic=True)
        for nic in network_io:
            resource_id = resource_id + nic
            sample_list.append(make_sample(name+'_bytes_sent', sample.TYPE_CUMULATIVE, 'bytes', network_io[nic].bytes_sent, resource_id))
            sample_list.append(make_sample(name+'_bytes_recv', sample.TYPE_CUMULATIVE, 'bytes', network_io[nic].bytes_recv, resource_id))
            sample_list.append(make_sample(name+'_packets_sent', sample.TYPE_CUMULATIVE, 'packets', network_io[nic].packets_sent, resource_id))
            sample_list.append(make_sample(name+'_packets_recv', sample.TYPE_CUMULATIVE, 'packets', network_io[nic].packets_recv, resource_id))
            sample_list.append(make_sample(name+'_input_error', sample.TYPE_CUMULATIVE, 'errors', network_io[nic].errin, resource_id))
            sample_list.append(make_sample(name+'_output_error', sample.TYPE_CUMULATIVE, 'errors', network_io[nic].errout, resource_id))
            sample_list.append(make_sample(name+'_input_dropped', sample.TYPE_CUMULATIVE, 'packets', network_io[nic].dropin, resource_id))
            sample_list.append(make_sample(name+'_output_dropped', sample.TYPE_CUMULATIVE, 'packets', network_io[nic].dropout, resource_id))
        
        return sample_list
    
