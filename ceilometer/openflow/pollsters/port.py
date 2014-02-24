from ceilometer.openstack.common import log
from ceilometer import sample
from ceilometer.openstack.common import timeutils

LOG = log.getLogger(__name__)

_PORT_REV_BYTE='port_rx_bytes'
_PORT_SENT_BYTE='port_tx_bytes'
_PORT_REV_PACKET='port_rx_packets'
_PORT_SENT_PACKET='port_tx_packets'


class PortReceivedBytes(object):

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
    
class PortSentBytes(object):

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
    
class PortReceivedPackets(object):

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

class PortSentPackets(object):

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
    