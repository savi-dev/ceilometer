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

_PROCESS_CPU_TIME = 'phy_process_cpu_time'
_PROCESS_CPU_PERCENT = 'phy_process_cpu_percent'
_PROCESS_MEM_USAGE = 'phy_process_memory_usage'
_PROCESS_MEM_PERCENTAGE = 'phy_process_memory_percentage'
_PROCESS_DISKIO = 'phy_process_diskio'
_PROCESS_THREAD_NUM = 'phy_process_thread_number'
_PROCESS_CONTEXT_SWITCH_NUM = 'phy_process_context_sw_number'




class processCpuTime (plugin.PhyServerPollster):
    def get_samples(self, cache):
        LOG.info('polling process cpu time of the physical server')
        resource_id = 'server_'+cache['host_name']+'_process_'
        sample_list = []
        
        name = _PROCESS_CPU_TIME
        pids = psutil.get_pid_list()
        for pid in pids:
            resource_id = resource_id + pid
            p = psutil.Process(pid)
            cpu_time = p.get_cpu_times()
            sample_list.append(make_sample(name+'_user', sample.TYPE_CUMULATIVE, 'seconds', cpu_time.user, resource_id))
            sample_list.append(make_sample(name+'_system', sample.TYPE_CUMULATIVE, 'seconds', cpu_time.system, resource_id))
            
        return sample_list


class processCpuPercent (plugin.PhyServerPollster):
    def get_samples(self, cache):
        LOG.info('polling process cpu percentage of the physical server')
        resource_id = 'server_'+cache['host_name']+'_process_'
        sample_list = []
        
        name = _PROCESS_CPU_PERCENT
        pids = psutil.get_pid_list()
        for pid in pids:
            resource_id = resource_id + pid
            p = psutil.Process(pid)
            cpu_percent = p.get_cpu_percent()
            sample_list.append(make_sample(name, sample.TYPE_GAUGE, 'percent', cpu_percent, resource_id))
            
        return sample_list
    
class processMemUsage (plugin.PhyServerPollster):
    def get_samples(self, cache):
        LOG.info('polling process memory usage of the physical server')
        resource_id = 'server_'+cache['host_name']+'_process_'
        sample_list = []
        
        name = _PROCESS_MEM_USAGE
        pids = psutil.get_pid_list()
        for pid in pids:
            resource_id = resource_id + pid
            p = psutil.Process(pid)
            mem_usage = p.get_memory_info()
            sample_list.append(make_sample(name+'_rss', sample.TYPE_GAUGE, 'bytes', mem_usage.rss, resource_id))
            sample_list.append(make_sample(name+'_vms', sample.TYPE_GAUGE, 'bytes', mem_usage.vms, resource_id))
            
        return sample_list
    
    
class processMemPercent (plugin.PhyServerPollster):
    def get_samples(self, cache):
        LOG.info('polling process memory usage percentage of the physical server')
        resource_id = 'server_'+cache['host_name']+'_process_'
        sample_list = []
        
        name = _PROCESS_MEM_PERCENTAGE
        pids = psutil.get_pid_list()
        for pid in pids:
            resource_id = resource_id + pid
            p = psutil.Process(pid)
            mem_percent = p.get_memory_percent()
            sample_list.append(make_sample(name, sample.TYPE_GAUGE, 'percent', mem_percent, resource_id))
            
        return sample_list
    
class processDiskIO (plugin.PhyServerPollster):
    def get_samples(self, cache):
        LOG.info('polling process disk IO of the physical server')
        resource_id = 'server_'+cache['host_name']+'_process_'
        sample_list = []
        
        name = _PROCESS_DISKIO
        pids = psutil.get_pid_list()
        for pid in pids:
            resource_id = resource_id + pid
            p = psutil.Process(pid)
            disk_io = p.get_io_counters()
            sample_list.append(make_sample(name+'_read_count', sample.TYPE_CUMULATIVE, 'numbers', disk_io.read_count, resource_id))
            sample_list.append(make_sample(name+'_write_count', sample.TYPE_CUMULATIVE, 'numbers', disk_io.write_count, resource_id))
            sample_list.append(make_sample(name+'_read_bytes', sample.TYPE_CUMULATIVE, 'bytes', disk_io.read_bytes, resource_id))
            sample_list.append(make_sample(name+'_write_bytes', sample.TYPE_CUMULATIVE, 'bytes', disk_io.write_bytes, resource_id))
        return sample_list
    

class processThreadNum (plugin.PhyServerPollster):
    def get_samples(self, cache):
        LOG.info('polling process thread numbers of the physical server')
        resource_id = 'server_'+cache['host_name']+'_process_'
        sample_list = []
        
        name = _PROCESS_THREAD_NUM
        pids = psutil.get_pid_list()
        for pid in pids:
            resource_id = resource_id + pid
            p = psutil.Process(pid)
            thread_num = p.get_num_threads()
            sample_list.append(make_sample(name, sample.TYPE_GAUGE, 'threads', thread_num, resource_id))
            
        return sample_list

class processCtxSwNum (plugin.PhyServerPollster):
    def get_samples(self, cache):
        LOG.info('polling process context switch numbers of the physical server')
        resource_id = 'server_'+cache['host_name']+'_process_'
        sample_list = []
        
        name = _PROCESS_CONTEXT_SWITCH_NUM
        pids = psutil.get_pid_list()
        for pid in pids:
            resource_id = resource_id + pid
            p = psutil.Process(pid)
            ctx_sw_times = p.get_num_ctx_switches()
            sample_list.append(make_sample(name+'_voluntary', sample.TYPE_CUMULATIVE, 'switches', ctx_sw_times.voluntary, resource_id))
            sample_list.append(make_sample(name+'_involuntary', sample.TYPE_CUMULATIVE, 'switches', ctx_sw_times.involuntary, resource_id))

        return sample_list
