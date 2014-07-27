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

_CPU_TIME = 'phy_cpu_time'
_CPU_PERCENT = 'phy_cpu_percentage'
_CPU_TIME_PERCENT = 'phy_cpu_time_percentage'



class cpuTime (plugin.PhyServerPollster):
    def get_samples(self, cache):
        LOG.info('polling cpu time of the physical server')
        base_resource_id = 'server_'+cache['host_name']
        sample_list = []
        
        #get a list of cpu times
        cpu_times = psutil.cpu_times(percpu=True)
        count = 1
        for ct in cpu_times:
            name = _CPU_TIME
            resource_id = base_resource_id + '_core_'+str(count)
            #user time
            sample_list.append(make_sample(name+'_user_time', sample.TYPE_CUMULATIVE, 'seconds', ct.user, resource_id))
            #nice time
            sample_list.append(make_sample(name+'_nice_time', sample.TYPE_CUMULATIVE, 'seconds', ct.nice, resource_id))
            #system time
            sample_list.append(make_sample(name+'_system_time', sample.TYPE_CUMULATIVE, 'seconds', ct.system, resource_id))
            #idle time
            sample_list.append(make_sample(name+'_idle_time', sample.TYPE_CUMULATIVE, 'seconds', ct.idle, resource_id))
            #iowait time
            sample_list.append(make_sample(name+'_io_wait_time', sample.TYPE_CUMULATIVE, 'seconds', ct.iowait, resource_id))
            #interrupt request time
            sample_list.append(make_sample(name+'_interrupt_req_time', sample.TYPE_CUMULATIVE, 'seconds', ct.irq, resource_id))
            #softirq time
            sample_list.append(make_sample(name+'_soft_interrupt_req_time', sample.TYPE_CUMULATIVE, 'seconds', ct.softirq, resource_id))
            #steal time
            sample_list.append(make_sample(name+'_steal_time', sample.TYPE_CUMULATIVE, 'seconds', ct.steal, resource_id))
            #guest time
            sample_list.append(make_sample(name+'_guest_time', sample.TYPE_CUMULATIVE, 'seconds', ct.guest, resource_id))
            #guest nice time
            sample_list.append(make_sample(name+'_guest_nice_time', sample.TYPE_CUMULATIVE, 'seconds', ct.guest_nice, resource_id))

            count = count + 1
        return sample_list

class cpuPercent (plugin.PhyServerPollster):
    def get_samples(self, cache):
        LOG.info('polling cpu usage percentage of the physical server')
        base_resource_id = 'server_'+cache['host_name']
        sample_list = []
        
        #get a list of cpu percentage
        cpu_percent = psutil.cpu_percent(percpu=True)
        count = 1
        for cp in cpu_percent:
            name = _CPU_PERCENT
            resource_id = base_resource_id+'_core_'+str(count)
            sample_list.append(make_sample(name, sample.TYPE_GAUGE, 'percent', cp, resource_id))
            count = count + 1
        return sample_list
    

class cpuTimePercent (plugin.PhyServerPollster):
    def get_samples(self, cache):
        LOG.info('polling cpu time percentage of the physical server')
        base_resource_id = 'server_'+cache['host_name']
        sample_list = []
        
        #get a list of cpu times
        cpu_times = psutil.cpu_times_percent(percpu=True)
        count = 1
        for ct in cpu_times:
            name = _CPU_TIME_PERCENT
            resource_id = base_resource_id+'_core_'+str(count)
            #user time
            sample_list.append(make_sample(name+'_user_time', sample.TYPE_GAUGE, 'percent', ct.user, resource_id))
            #nice time
            sample_list.append(make_sample(name+'_nice_time', sample.TYPE_GAUGE, 'percent', ct.nice, resource_id))
            #system time
            sample_list.append(make_sample(name+'_system_time', sample.TYPE_GAUGE, 'percent', ct.system, resource_id))
            #idle time
            sample_list.append(make_sample(name+'_idle_time', sample.TYPE_GAUGE, 'percent', ct.idle, resource_id))
            #iowait time
            sample_list.append(make_sample(name+'_io_wait_time', sample.TYPE_GAUGE, 'percent', ct.iowait, resource_id))
            #interrupt request time
            sample_list.append(make_sample(name+'_interrupt_req_time', sample.TYPE_GAUGE, 'percent', ct.irq, resource_id))
            #softirq time
            sample_list.append(make_sample(name+'_soft_interrupt_req_time', sample.TYPE_GAUGE, 'percent', ct.softirq, resource_id))
            #steal time
            sample_list.append(make_sample(name+'_steal_time', sample.TYPE_GAUGE, 'percent', ct.steal, resource_id))
            #guest time
            sample_list.append(make_sample(name+'_guest_time', sample.TYPE_GAUGE, 'percent', ct.guest, resource_id))
            #guest nice time
            sample_list.append(make_sample(name+'_guest_nice_time', sample.TYPE_GAUGE, 'percent', ct.guest_nice, resource_id))

            count = count + 1
        return sample_list
    
 
        
        
        
        