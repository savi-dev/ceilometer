# vim: tabstop=4 shiftwidth=4 softtabstop=4 expandtab
#
# Copyright (C) 2012, The SAVI Project.
#
# @author: Eliot J. Kang <eliot@savinetwork.ca>
# @author: Jieyu Lin <Jieyu.lin@savinetwork.ca>


"""
A driver for Ryu openflow controller.
"""
import requests
from requests.exceptions import ConnectionError

# from ryu.lib.dpid import dpid_to_str
# 
# from ceilometer.openstack.common import log
# from ceilometer.openflow import driver
# from whale.exception import NotFound
# from ryu.ofproto.ofproto_v1_0 import OFPFW_ALL
# 
# LOG = log.getLogger(__name__)

from ryu.lib.dpid import dpid_to_str

from whale.openstack import logging
from whale.network import driver
from whale import config
from whale.exception import NotFound

LOG = logging.getLogger(__name__)
CONF = config.CONF

class RyuNetworkDriver(driver.NetworkDriver):

    
    def __init__(self, host = None, port = None):
        super(RyuNetworkDriver, self).__init__('ryu', host, port)

        LOG.info("Network controller (%s) API address is %s:%s" % (self.name, self.host, self.port))

        # (dpid)
        self.desc_resource = '/stats/desc/%s'

        # (dpid)
        self.port_resource = '/stats/port/%s'

        # (dpid)
        self.flow_resource = '/stats/flow/%s'

        self.switch_resource = '/stats/switches'

        self.device_resource = '/stats/devices'

        self.topology = '/topology/links'

        # (dpid)
        self.topology_link = '/topology/switch/%s/links'

    def _get(self, url, body = None):
        full_url = 'http://%s:%s%s' % (self.host, self.port, url)
        try:
            r = requests.get(full_url, timeout = 0.2)
            if r.status_code == 200:
                return r.json()
            raise NotFound('url %s')
        except Exception, err:
            print err
            return None

    def _put(self, url, body = None):
        full_url = 'http://%s:%s%s' % (self.host, self.port, url)
        try:
            r = requests.put(full_url, timeout = 0.2, data = body)
            if r.status_code == 200:
                return r.json()
            raise NotFound('url %s')
        except Exception, err:
            LOG.exception (err)
            return None

    def get_switches(self):
        LOG.debug(_("get_switches"))
        dps = self._get(self.switch_resource)
        if dps == None:
            return None
        dpstr = []
        for (dp, dp_hex) in dps:
            dpstr.append(dpid_to_str(dp))
        return dpstr

    def get_ports(self, dpid):
        LOG.debug(_("get_ports in %s") % dpid)
        ports = self._get(self.port_resource % int(dpid, 16))
        if ports is not None:
            return ports[dpid]
        return None


    def get_flows(self, dpid):
        LOG.debug(_("get_flows in %s") % dpid)
        flow = {'match':{}}
        flows = self._put(self.flow_resource % int(dpid, 16), flow)
        if flows is not None:
            return flows[dpid]
        return None

    def get_description(self, dpid):
        LOG.debug(_("get_description in %s") % dpid)
        desc = self._get(self.desc_resource % int(dpid, 16))
        if desc is not None:
            desc = desc[dpid]
            # remove white spaces from the string
            for k in desc.keys():
                desc[k] = desc[k].strip('\x00')
            # add controller information
            desc['controller name'] = self.name
            desc['controller host'] = self.host
            desc['controller port'] = self.port
            return desc
        return None

    def get_devices(self):
        LOG.debug(_("get_devices"))
        return self._get(self.device_resource)

    def get_links(self):
        LOG.debug(_("get_links"))
        links = self._get(self.topology)
        if links is not None:
            return links['items']
        return None

    def get_link(self, dpid):
        LOG.debug(_("get_link: %s") % dpid)
        return self._get(self.topology_link % int(dpid, 16))

