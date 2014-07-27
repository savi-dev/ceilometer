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

_VIRTUAL_MEM = 'phy_virtual_memory'
_SWAP_MEM = 'phy_swap_memory'


class virtualMemory (plugin.PhyServerPollster):
    def get_samples(self, cache):
        LOG.info('polling virtual memory usage of the physical server')
        resource_id = 'server_'+cache['host_name']
        sample_list = []
        
        #get virtual memory information 
        vir_mem = psutil.virtual_memory()
        name = _VIRTUAL_MEM
        #total virtual memory
        sample_list.append(make_sample(name+'_total', sample.TYPE_GAUGE, 'bytes', vir_mem.total, resource_id))
        #available virtual memory
        sample_list.append(make_sample(name+'_available', sample.TYPE_GAUGE, 'bytes', vir_mem.available, resource_id))
        #percent virtual memory used
        sample_list.append(make_sample(name+'_percent_used', sample.TYPE_GAUGE, 'percent', vir_mem.percent, resource_id))
        #used virtual memory
        sample_list.append(make_sample(name+'_used', sample.TYPE_GAUGE, 'bytes', vir_mem.used, resource_id))
        #free virtual memory
        sample_list.append(make_sample(name+'_free', sample.TYPE_GAUGE, 'bytes', vir_mem.free, resource_id))
        #active virtual memory
        sample_list.append(make_sample(name+'_active', sample.TYPE_GAUGE, 'bytes', vir_mem.active, resource_id))
        #inactive virtual memory
        sample_list.append(make_sample(name+'_inactive', sample.TYPE_GAUGE, 'bytes', vir_mem.inactive, resource_id))
        #buffers virtual memory
        sample_list.append(make_sample(name+'_buffers', sample.TYPE_GAUGE, 'bytes', vir_mem.buffers, resource_id))
        #cached virtual memory
        sample_list.append(make_sample(name+'_cached', sample.TYPE_GAUGE, 'bytes', vir_mem.cached, resource_id))
        
        return sample_list
    
class swapMemory (plugin.PhyServerPollster):
    def get_samples(self, cache):
        LOG.info('polling swap memory usage of the physical server')
        resource_id = 'server_'+cache['host_name']
        sample_list = []

        #get swap memory information
        swap_mem = psutil.swap_memory()
        name = _SWAP_MEM
        
        #total swap memory information
        sample_list.append(make_sample(name+'_total', sample.TYPE_GAUGE, 'bytes', swap_mem.total, resource_id))
        #used swap memory information
        sample_list.append(make_sample(name+'_used', sample.TYPE_GAUGE, 'bytes', swap_mem.used, resource_id))
        #free swap memory information
        sample_list.append(make_sample(name+'_free', sample.TYPE_GAUGE, 'bytes', swap_mem.free, resource_id))
        #percent swap memory information
        sample_list.append(make_sample(name+'_percent', sample.TYPE_GAUGE, 'percent', swap_mem.percent, resource_id))
        #sin swap memory information
        sample_list.append(make_sample(name+'_sin', sample.TYPE_GAUGE, 'bytes', swap_mem.sin, resource_id))
        #sout swap memory information
        sample_list.append(make_sample(name+'_sout', sample.TYPE_GAUGE, 'bytes', swap_mem.sout, resource_id))
        
        return sample_list