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

_DISK_USAGE = 'phy_disk_usage'
_DISK_IO = 'phy_disk_io'

class diskUsage (plugin.PhyServerPollster):
    def get_samples(self, cache):
        LOG.info('polling disk usage of the physical server')
        resource_id = 'server_'+cache['host_name']+'_disk_'
        sample_list = []
        
        disk_partitions = psutil.disk_partitions()
        name = _DISK_USAGE
        for dp in disk_partitions:
            partition_name = dp.device.split('/')[-1]
            curr_resource_id = resource_id + partition_name
            disk_usage = psutil.disk_usage(dp.mountpoint)
            sample_list.append(make_sample(name+'_total', sample.TYPE_GAUGE, 'bytes', disk_usage.total, curr_resource_id))
            sample_list.append(make_sample(name+'_used', sample.TYPE_GAUGE, 'bytes', disk_usage.used, curr_resource_id))
            sample_list.append(make_sample(name+'_free', sample.TYPE_GAUGE, 'bytes', disk_usage.free, curr_resource_id))
            sample_list.append(make_sample(name+'_percent_used', sample.TYPE_GAUGE, 'bytes', disk_usage.percent, curr_resource_id))

        return sample_list
    
class diskIO (plugin.PhyServerPollster):
    def get_samples(self, cache):
        LOG.info('polling disk IO of the physical server')
        resource_id = 'server_'+cache['host_name']+'_disk_'
        sample_list = []
        
        disk_io = psutil.disk_io_counters(perdisk=True)
        name = _DISK_IO
        for disk in disk_io:
            if disk != 'loop0':
                curr_resource_id = resource_id + disk
                sample_list.append(make_sample(name+'_read_count', sample.TYPE_CUMULATIVE, 'numbers', disk_io[disk].read_count, curr_resource_id))
                sample_list.append(make_sample(name+'_write_count', sample.TYPE_CUMULATIVE, 'numbers', disk_io[disk].write_count, curr_resource_id))
                sample_list.append(make_sample(name+'_read_bytes', sample.TYPE_CUMULATIVE, 'bytes', disk_io[disk].read_bytes, curr_resource_id))
                sample_list.append(make_sample(name+'_write_bytes', sample.TYPE_CUMULATIVE, 'bytes', disk_io[disk].write_bytes, curr_resource_id))
                sample_list.append(make_sample(name+'_read_time', sample.TYPE_CUMULATIVE, 'seconds', disk_io[disk].read_time, curr_resource_id))
                sample_list.append(make_sample(name+'_write_time', sample.TYPE_CUMULATIVE, 'seconds', disk_io[disk].write_time, curr_resource_id))
                
        return sample_list
