# vim: tabstop=4 shiftwidth=4 softtabstop=4 expandtab
#
# Copyright (C) 2012, The SAVI Project.
#
# @author: Eliot J. Kang <eliot@savinetwork.ca>


"""
Driver base-classes:

    (Beginning of) the contract that network drivers must follow, and shared
    types that support that contract
"""
from ceilometer.openstack.common import log

LOG = log.getLogger(__name__)

class NetworkDriver(object):
    '''Base class for Network drivers.
    :host:        host name for network driver
    :port:        (int) port number for network driver
    '''
    
    
    def __init__(self, name=None, host=None, port=None):
        if name:
            assert type(name) is str
        if host:
            assert type(host) is str
        if port:
            assert type(port) is int or type(port) is str
        
        self.name = name
        self.host = host
        self.port = str(port)
        
        if self.name and self.host and self.port:
            LOG.info("Network controller (%s) API address is %s:%s" % (self.name, self.host, self.port))

    '''Set the controller.
    :host:        host name for network driver
    :port:        (int) port number for network driver
    '''
    def set_controller(self, host, port):
        assert type(name) is str
        assert type(host) is str
        assert type(port) is int or type(port) is str
        self.name = name
        self.host = host
        self.port = str(port)

        LOG.info("Network controller (%s) API address is %s:%s" % (self.name, self.host, self.port))

    '''Get the switches.
    '''
    def get_switches(self):
        raise NotImplementedError()
        
    '''Get the ports.
    :dpid:    datapath id
    '''
    def get_ports(self, dpid):
        raise NotImplementedError()
        
    '''Get the flows.
    :dpid:    datapath id
    '''
    def get_flows(self, dpid):
        raise NotImplementedError()
    
    '''Get the desription.
    :dpid:    datapath id
    '''
    def get_description(self, dpid):
        raise NotImplementedError()
    
    '''Get the devices.
    :dpid:    datapath id
    '''
    def get_devices(self):
        raise NotImplementedError()
    
    '''Get the links.
    :dpid:    datapath id
    '''
    def get_links(self):
        raise NotImplementedError()
    
    '''Get the links.
    :dpid:    datapath id
    '''
    def get_link(self, dpid):
        raise NotImplementedError()
        
