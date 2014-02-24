#
# Copyright 2013 University of Toronto
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Base class for OpenFlow Interface Drivers
# Drivers for specific OF Controllers should overwrite these functions
# Ideally drivers should not retain any state information within themselves
# Can be used as is to test the network applications and controllers alone

# Use httplib for now, look into requests lib later
import httplib
import json

from janus.common import logging
from janus.network.common.status_codes import *
from janus.network.of_controller.ofi_constants import OFICMDS
from janus.network.of_controller.ofi_base_driver import OFIBaseDriver
from janus.network.of_controller.janus_of_consts import JANFLOWACTIONS
from janus.network.of_controller.flow_entry import FlowEntry
import traceback

LOG = logging.getLogger("janus.network.of_controller.backend.ryu")

# Driver for Ryu
class RyuOFIDriver(OFIBaseDriver):
    def __init__(self, host = None, port = None):
        super(RyuOFIDriver, self).__init__(host, port)
        self._conn = {}
        # (dpid, buffer_id, in_port), output ports specified in body, also packet content is specified in body
        self.output_url = '/v1.0/packetAction/%s/output/%s_%s'

        # (dpid, buffer_id, in_port)
        self.drop_url = '/v1.0/packetAction/%s/drop/%s_%s'

        # Flow match and actions specified in body
        self.addFlow_url = '/stats/flowentry/add'

        # (dpid)
        self.delAllFlow_url = '/stats/flowentry/clear/%s'

        # Flow match specified in body
        self.delFlow_url = '/stats/flowentry/delete'

        self.delUserFlow_url = '/stats/del_user_flow/%s/%s/%s'

        self.mac_ip_assoc_url = '/stats/mac_ip'

        self.mac_ip_del_list_url = '/stats/mac_ip/del_list'

        self.getFlowStats_url = '/stats/flow/%s'
        
        self.getPortStats_url = '/stats/port/%s'

        self.installRuleMatch_url = '/stats/flowentry/store_install/%s'

        self.getRuleMatch_url = '/stats/flowentry/store/%s'

    # Returns a dictionary version of the flow match in a form Ryu can use
    def _getMatchDict(self, flow):
        assert isinstance(flow, FlowEntry)
        match = {}

        if flow.in_port:
            match['in_port'] = flow.in_port
        if flow.dl_src:
            match['dl_src'] = flow.dl_src
        if flow.dl_dst:
            match['dl_dst'] = flow.dl_dst
        if flow.dl_type:
            match['dl_type'] = flow.dl_type
        if flow.dl_vlan:
            match['dl_vlan'] = flow.dl_vlan
        if flow.dl_vlan_pcp:
            match['dl_vlan_pcp'] = flow.dl_vlan_pcp
        if flow.nw_src:
            match['nw_src'] = flow.nw_src
        if flow.nw_dst:
            match['nw_dst'] = flow.nw_dst
        if flow.nw_proto:
            match['nw_proto'] = flow.nw_proto
        if flow.nw_tos:
            match['nw_tos'] = flow.nw_tos
        if flow.tp_src:
            match['tp_src'] = flow.tp_src
        if flow.tp_dst:
            match['tp_dst'] = flow.tp_dst

        return match

    def _controllerActionGetReturn(self, dpid, action, method, body = None):
        if self._dp_controller_address is not None:
            (host, port) = self._dp_controller_address(dpid)
            if host is None or port is None:
                host = self.host
                port = self.port
        else:
            host = self.host
            port = self.port
        ret = None
        url = action
        try:
            self._conn[dpid].request(method, url, body)
            res = self._conn[dpid].getresponse()
            ret = res.read()
        except:
            LOG.info("FAILED TO SEND TO CONTROLLER FIRST Time: url = %s ; body = %s" % (url, body))
            try:
                self._conn[dpid] = httplib.HTTPConnection(host, port, timeout = 0.2)
                self._conn[dpid].request(method, url, body)
                res = self._conn[dpid].getresponse()
                ret = res.read()
            except:
                traceback.print_exc()
                LOG.warn("FAILED TO SEND TO CONTROLLER: url = %s ; body = %s" % (url, body))
                pass
            pass
        return ret

    def _controllerAction(self, dpid, action, method, body = None):
        if self._dp_controller_address is not None:
            (host, port) = self._dp_controller_address(dpid)
            if host is None or port is None:
                host = self.host
                port = self.port
        else:
            host = self.host
            port = self.port

        status = JANUS_ERROR
        url = action
        try:
            self._conn[dpid].request(method, url, body)
            res = self._conn[dpid].getresponse()
            res.read()
        except:
            LOG.info("FAILED TO SEND TO CONTROLLER FIRST Time: url = %s ; body = %s" % (url, body))
            try:
                self._conn[dpid] = httplib.HTTPConnection(host, port, timeout = 0.2)
                self._conn[dpid].request(method, url, body)
                res = self._conn[dpid].getresponse()
                res.read()
            except:
                traceback.print_exc()
                LOG.warn("FAILED TO SEND TO CONTROLLER: url = %s ; body = %s" % (url, body))
                pass
            pass
        return JANUS_SUCCESS
    """
        if res.status in ( httplib.OK,
                          httplib.CREATED,
                          httplib.ACCEPTED,
                          httplib.NO_CONTENT ):
        raise httplib.HTTPException(
            res, 'code %d reason %s' % ( res.status, res.reason ),
            res.getheaders(), res.read() )
    """

    def _packet_out(self, **kwargs):
        LOG.debug("Ryu driver outputting packet")
        dpid = kwargs.get('dpid')
        buffer_id = kwargs.get('buffer_id')
        in_port = kwargs.get('in_port')
        body = {'out_port_list': kwargs.get('out_ports')}
        if kwargs.get('data', None):
            body['data'] = kwargs.get('data')
        flow = kwargs.get('flow', None)
        if flow is not None and len(flow.actions) > 0:
            actions = []
            for act in flow.getActions():
                if act.action_id == JANFLOWACTIONS.JAN_ACT_OUTPUT:
                    actions.append({"type": "OUTPUT", "port": act.param})
                elif act.action_id == JANFLOWACTIONS.JAN_ACT_SET_DL_DST:
                    actions.append({"type": "SET_DL_DST", "dl_dst": act.param})
                else:
                    LOG.debug("%s ERROR: Unimplemented actions", self.__class__.__name__)
            body['actions'] = actions
        status = self._controllerAction(dpid, self.output_url % (dpid, buffer_id, in_port),
                                                    'PUT', json.dumps(body))
        return status

    def _packet_drop(self, **kwargs):
        LOG.debug("Ryu driver dropping packet")
        dpid = kwargs.get('dpid')
        buffer_id = kwargs.get('buffer_id')
        in_port = kwargs.get('in_port')
        status = self._controllerAction(dpid, self.drop_url % (dpid, buffer_id, in_port), 'DELETE')
        return status

    def _flow_add(self, **kwargs):
        LOG.debug("Ryu driver adding flow")
        dpid = kwargs.get('dpid')
        flow = kwargs.get('flow')
        priority = flow.priority
        assert flow.isAllWild() is False

        actions = []
        for act in flow.getActions():
            if act.action_id == JANFLOWACTIONS.JAN_ACT_OUTPUT:
                if act.param is None:
                    # change to drop
                    actions = []
                    break
                actions.append({"type": "OUTPUT", "port": act.param})
            elif act.action_id == JANFLOWACTIONS.JAN_ACT_SET_DL_DST:
                actions.append({"type": "SET_DL_DST", "dl_dst": act.param})
            else:
                LOG.debug("%s ERROR: Unimplemented actions", self.__class__.__name__)


        match = self._getMatchDict(flow)
        body = {"dpid": dpid, "actions": actions, "idle_timeout": flow.idle_timeout, "cookie": 0, "hard_timeout": flow.hard_timeout, "match": match}
        if priority is not None:
            body['priority'] = priority

        LOG.debug("ADDING FLOW dpid = %s, in_port = %s, src = %s, dst = %s, actions = %s",
                    (dpid), flow.in_port, flow.dl_src, flow.dl_dst, actions)
        status = self._controllerAction(dpid, self.addFlow_url, 'POST', json.dumps(body))
        return status

    def _flow_del(self, **kwargs):
        LOG.debug("Ryu driver deleting flow")
        dpid = kwargs.get('dpid')
        flow = kwargs.get('flow')

        if flow.isAllWild() and not flow.out_port:
            # Delete all flows
            # LOG.debug("Deleting all flows in switch %s", hex(dpid))
            status = self._controllerAction(dpid, self.delAllFlow_url % dpid, 'DELETE')
        else:
            # Delete specific flows
            match = self._getMatchDict(flow)
            body = {"dpid": dpid, "match": match}
            if flow.out_port:
                body["out_port"] = flow.out_port
            status = self._controllerAction(dpid, self.delFlow_url, 'POST', json.dumps(body))
        return status

    def _flow_mod(self, **kwargs):
        LOG.debug("Ryu driver modifying flow")
        return JANUS_SUCCESS

    def _mac_ip_assoc(self, **kwargs):
        LOG.info("ryu mac_ip_assoc")
        body = {}
        dpid = body['dpid'] = kwargs.get('dpid')
        body['mac'] = kwargs.get('mac')
        body['port_no'] = kwargs.get('port_no')
        body['ip'] = kwargs.get('ip')
        status = self._controllerAction(dpid, self.mac_ip_assoc_url, 'POST', json.dumps(body))
        return JANUS_SUCCESS

    def _mac_del(self, **kwargs):
        LOG.info("ryu mac_del")
        body = {}
        body['dpid'] = kwargs.get('dpid')
        body['mac'] = kwargs.get('mac')
        body['port'] = kwargs.get('port')
        body['ip'] = kwargs.get('ip', '0.0.0.0')
        body['dpid_list'] = kwargs.get('dpid_list', [])
        ctrl_dict = {}
        for id in body['dpid_list']:
            if self._dp_controller_address is not None:
                (host, port) = self._dp_controller_address(id)
                if host is not None and port is not None:
                    ctrl_dict[(host, port)] = id
        for id in ctrl_dict.values():
            status = self._controllerAction(id, self.mac_ip_assoc_url + '/del/%s_%s_%s' % (body['dpid'], body['port'], body['mac']), 'POST', json.dumps(body))
        return JANUS_SUCCESS

    def _mac_ip_list(self, **kwargs):
        LOG.info("ryu mac_ip_list")
        body = {}
        dpid = body['dpid'] = kwargs.get('dpid')
        body['mac_ip_list'] = kwargs.get('mac_ip_list')
        status = self._controllerAction(dpid, self.mac_ip_del_list_url, 'POST', json.dumps(body))
        return JANUS_SUCCESS

    def _user_flow_add(self, **kwargs):
        LOG.debug("Ryu driver adding user flow")
        dpid = kwargs.get('dpid')
        flow = kwargs.get('flow')
        status = self._controllerAction(int(dpid), self.addFlow_url, 'POST', json.dumps(flow))
        return status

    def _user_flow_del(self, **kwargs):
        LOG.debug("Ryu driver del user flow")
        dpid = kwargs.get('dpid')
        h_dpid = str(hex(int(dpid)))
        user_id = kwargs.get('user_id', None)
        id = kwargs.get('id', None)
        status = self._controllerAction(int(dpid), self.delUserFlow_url % (user_id, h_dpid, id), 'POST')
        return status

    def _get_flow_stats(self, **kwargs):
        LOG.debug("Ryu driver get flow stats")
        dpid = kwargs.get('dpid')
        match = kwargs.get('match', {})
        flow = {}
        flow['match'] = match
        ret = self._controllerActionGetReturn(int(dpid), self.getFlowStats_url % (dpid), 'PUT', json.dumps(flow))
        return json.loads(ret)

    def _get_port_stats(self, **kwargs):
        LOG.debug("Ryu driver get port stats")
        dpid = kwargs.get('dpid')
        ret = self._controllerActionGetReturn(int(dpid), self.getPortStats_url % (dpid), 'GET')
        return json.loads(ret)

    def _install_rule_for_match(self, **kwargs):
        LOG.debug("Ryu driver install rule for match")
        dpid = kwargs.get('dpid')
        match = {}
        for key in 'dl_src', 'dl_dst', 'eth_type', 'in_port':
            match[key] = kwargs.get(key, None)
        flow = {}
        flow['match'] = match
        status = self._controllerAction(int(dpid), self.installRuleMatch_url % (dpid), 'PUT', json.dumps(flow))
        return status

    def _get_rule_from_controller(self, **kwargs):
        LOG.debug("Ryu driver get rule for match")
        dpid = kwargs.get('dpid')
        match = {}
        for key in 'dl_src', 'dl_dst', 'eth_type', 'in_port':
            match[key] = kwargs.get(key, None)
        flow = {}
        flow['match'] = match
        ret = self._controllerActionGetReturn(int(dpid), self.getRuleMatch_url % (dpid), 'PUT', json.dumps(flow))
        return json.loads(ret)
