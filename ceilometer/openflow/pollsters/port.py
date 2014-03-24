#
# Copyright (C) 2014, The SAVI Project.
#
# @author: Jieyu Lin <Jieyu.lin@savinetwork.ca>

from ceilometer.openstack.common import log
from ceilometer import sample
from ceilometer.openstack.common import timeutils
import abc

LOG = log.getLogger(__name__)

_PORT_REV_BYTE='openflow_port_rx_bytes'
_PORT_SENT_BYTE='openflow_port_tx_bytes'
_PORT_REV_PACKET='openflow_port_rx_packets'
_PORT_SENT_PACKET='openflow_port_tx_packets'
_PORT_RX_DROPPED='openflow_port_rx_dropped'
_PORT_TX_DROPPED='openflow_port_tx_dropped'
_PORT_RX_ERRORS='openflow_port_rx_errors'
_PORT_TX_ERRORS='openflow_port_tx_errors'

PORT_TYPE='port'

class PortBase(object):
    """base class for port statistics"""
    
    __metaclass__ = abc.ABCMeta
    
    def get_type (self):
        return PORT_TYPE
    
    @abc.abstractmethod
    def get_samples(self, switch, stats):
        """
        :param switch: a switch dpid
        :param stats: the port statistics of that switch
        """

class PortReceivedBytes(PortBase):

    def get_samples(self, switch, stats):
        LOG.info('calculating received bytes for switch with dpid %s', switch)
        sample_list = []
        for port_stat in stats:
            rx_bytes = port_stat['rx_bytes']
            port_num = port_stat['port_no']
            name = _PORT_REV_BYTE
            resource_id = switch+'_port_'+str(port_num)
            s = sample.Sample(
                name=name,
                type=sample.TYPE_CUMULATIVE,
                unit='bytes',
                volume=rx_bytes,
                user_id=None,
                project_id=None,
                resource_id=resource_id,
                timestamp=timeutils.isotime(),
                resource_metadata=None,)
            sample_list.append(s)
            
        return sample_list
    
class PortSentBytes(PortBase):

    def get_samples(self, switch, stats):
        LOG.info('calculating transmitted bytes for switch with dpid %s', switch)
        sample_list = []
        for port_stat in stats:
            tx_bytes = port_stat['tx_bytes']
            port_num = port_stat['port_no']
            name = _PORT_SENT_BYTE
            resource_id = switch+'_port_'+str(port_num)
            s = sample.Sample(
                name=name,
                type=sample.TYPE_CUMULATIVE,
                unit='bytes',
                volume=tx_bytes,
                user_id=None,
                project_id=None,
                resource_id=resource_id,
                timestamp=timeutils.isotime(),
                resource_metadata=None,)
            sample_list.append(s)
            
        return sample_list
    
class PortReceivedPackets(PortBase):

    def get_samples(self, switch, stats):
        LOG.info('calculating received packets for switch with dpid %s', switch)
        sample_list = []
        for port_stat in stats:
            rx_packets = port_stat['rx_packets']
            port_num = port_stat['port_no']
            name = _PORT_REV_PACKET
            resource_id = switch+'_port_'+str(port_num)
            s = sample.Sample(
                name=name,
                type=sample.TYPE_CUMULATIVE,
                unit='packets',
                volume=rx_packets,
                user_id=None,
                project_id=None,
                resource_id=resource_id,
                timestamp=timeutils.isotime(),
                resource_metadata=None,)
            sample_list.append(s)
            
        return sample_list

class PortSentPackets(PortBase):

    def get_samples(self, switch, stats):
        LOG.info('calculating sent packets for switch with dpid %s', switch)
        sample_list = []
        for port_stat in stats:
            tx_packets = port_stat['tx_packets']
            port_num = port_stat['port_no']
            name = _PORT_SENT_PACKET
            resource_id = switch+'_port_'+str(port_num)
            s = sample.Sample(
                name=name,
                type=sample.TYPE_CUMULATIVE,
                unit='packets',
                volume=tx_packets,
                user_id=None,
                project_id=None,
                resource_id=resource_id,
                timestamp=timeutils.isotime(),
                resource_metadata=None,)
            sample_list.append(s)
            
        return sample_list
    
class PortRxDropped(PortBase):

    def get_samples(self, switch, stats):
        LOG.info('calculating sent packets for switch with dpid %s', switch)
        sample_list = []
        for port_stat in stats:
            tx_packets = port_stat['rx_dropped']
            port_num = port_stat['port_no']
            name = _PORT_RX_DROPPED
            resource_id = switch+'_port_'+str(port_num)
            s = sample.Sample(
                name=name,
                type=sample.TYPE_CUMULATIVE,
                unit='packets',
                volume=tx_packets,
                user_id=None,
                project_id=None,
                resource_id=resource_id,
                timestamp=timeutils.isotime(),
                resource_metadata=None,)
            sample_list.append(s)
            
        return sample_list
    
class PortTxDropped(PortBase):

    def get_samples(self, switch, stats):
        LOG.info('calculating sent packets for switch with dpid %s', switch)
        sample_list = []
        for port_stat in stats:
            tx_packets = port_stat['tx_dropped']
            port_num = port_stat['port_no']
            name = _PORT_TX_DROPPED
            resource_id = switch+'_port_'+str(port_num)
            s = sample.Sample(
                name=name,
                type=sample.TYPE_CUMULATIVE,
                unit='packets',
                volume=tx_packets,
                user_id=None,
                project_id=None,
                resource_id=resource_id,
                timestamp=timeutils.isotime(),
                resource_metadata=None,)
            sample_list.append(s)
            
        return sample_list
    
class PortRxErrors(PortBase):

    def get_samples(self, switch, stats):
        LOG.info('calculating sent packets for switch with dpid %s', switch)
        sample_list = []
        for port_stat in stats:
            tx_packets = port_stat['rx_errors']
            port_num = port_stat['port_no']
            name = _PORT_RX_ERRORS
            resource_id = switch+'_port_'+str(port_num)
            s = sample.Sample(
                name=name,
                type=sample.TYPE_CUMULATIVE,
                unit='errors',
                volume=tx_packets,
                user_id=None,
                project_id=None,
                resource_id=resource_id,
                timestamp=timeutils.isotime(),
                resource_metadata=None,)
            sample_list.append(s)
            
        return sample_list
    

class PortTxErrors(PortBase):

    def get_samples(self, switch, stats):
        LOG.info('calculating sent packets for switch with dpid %s', switch)
        sample_list = []
        for port_stat in stats:
            tx_packets = port_stat['tx_errors']
            port_num = port_stat['port_no']
            name = _PORT_TX_ERRORS
            resource_id = switch+'_port_'+str(port_num)
            s = sample.Sample(
                name=name,
                type=sample.TYPE_CUMULATIVE,
                unit='errors',
                volume=tx_packets,
                user_id=None,
                project_id=None,
                resource_id=resource_id,
                timestamp=timeutils.isotime(),
                resource_metadata=None,)
            sample_list.append(s)
            
        return sample_list