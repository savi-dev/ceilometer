#
# Copyright (C) 2014, The SAVI Project.
#
# @author: Jieyu Lin <Jieyu.lin@savinetwork.ca>

from ceilometer.openstack.common import log
from ceilometer import sample
from ceilometer.openstack.common import timeutils
import abc

LOG = log.getLogger(__name__)

FLOW_TYPE = 'flow'

_FLOW_BYTE_COUNT = 'openflow_flow_byte_count'
_FLOW_DURATION_SEC = 'openflow_flow_duration_second'
_FLOW_DURATION_NSEC = 'openflow_flow_duration_nsec'
_FLOW_PACKET_COUNT = 'openflow_flow_packet_count'

class FlowBase(object):
    """base class for port statistics"""
    
    __metaclass__ = abc.ABCMeta
    
    def get_type (self):
        return FLOW_TYPE
    
    @abc.abstractmethod
    def get_samples(self, switch, stats):
        """
        :param switch: a switch dpid
        :param stats: the flow statistics of that switch
        """
        

class flowByteCount (FlowBase):
    def get_samples(self, switch, stats):
        LOG.info('Getting flow byte count for switch with dpid %s', switch)
        sample_list = []
        for flow_stat in stats:
            byte_count = flow_stat['byte_count']
            flow_id = flow_stat['cookie']

            name = _FLOW_BYTE_COUNT
            resource_id = switch+'_flow_'+str(flow_id)
            s = sample.Sample(
                name=name,
                type=sample.TYPE_CUMULATIVE,
                unit='bytes',
                volume=byte_count,
                user_id=None,
                project_id=None,
                resource_id=resource_id,
                timestamp=timeutils.isotime(),
                resource_metadata=None,)
            sample_list.append(s)
            
        return sample_list

class flowPacketCount (FlowBase):
    def get_samples(self, switch, stats):
        LOG.info('Getting flow packet count for switch with dpid %s', switch)
        sample_list = []
        for flow_stat in stats:
            byte_count = flow_stat['packet_count']
            flow_id = flow_stat['cookie']

            name = _FLOW_PACKET_COUNT
            resource_id = switch+'_flow_'+str(flow_id)
            s = sample.Sample(
                name=name,
                type=sample.TYPE_CUMULATIVE,
                unit='packets',
                volume=byte_count,
                user_id=None,
                project_id=None,
                resource_id=resource_id,
                timestamp=timeutils.isotime(),
                resource_metadata=None,)
            sample_list.append(s)
            
        return sample_list
    
class flowDurationSec (FlowBase):
    def get_samples(self, switch, stats):
        LOG.info('Getting flow duration sec for switch with dpid %s', switch)
        sample_list = []
        for flow_stat in stats:
            byte_count = flow_stat['duration_sec']
            flow_id = flow_stat['cookie']

            name = _FLOW_DURATION_SEC
            resource_id = switch+'_flow_'+str(flow_id)
            s = sample.Sample(
                name=name,
                type=sample.TYPE_CUMULATIVE,
                unit='seconds',
                volume=byte_count,
                user_id=None,
                project_id=None,
                resource_id=resource_id,
                timestamp=timeutils.isotime(),
                resource_metadata=None,)
            sample_list.append(s)
            
        return sample_list
    
class flowDurationMsec (FlowBase):
    def get_samples(self, switch, stats):
        LOG.info('Getting flow duration nsec for switch with dpid %s', switch)
        sample_list = []
        for flow_stat in stats:
            byte_count = flow_stat['duration_nsec']
            flow_id = flow_stat['cookie']

            name = _FLOW_DURATION_NSEC
            resource_id = switch+'_flow_'+str(flow_id)
            s = sample.Sample(
                name=name,
                type=sample.TYPE_GAUGE,
                unit='nsec',
                volume=byte_count,
                user_id=None,
                project_id=None,
                resource_id=resource_id,
                timestamp=timeutils.isotime(),
                resource_metadata=None,)
            sample_list.append(s)
            
        return sample_list
    