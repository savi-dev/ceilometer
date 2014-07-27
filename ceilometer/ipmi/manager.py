# vim: tabstop=4 shiftwidth=4 softtabstop=4 expandtab
#
# Copyright (C) 2014, The SAVI Project.
#
# @author: Jieyu Lin <Jieyu.lin@savinetwork.ca>

import socket
from oslo.config import cfg
from stevedore import extension
from stevedore import named

from ceilometer import agent
from ceilometer.openstack.common import log
from ceilometer.openstack.common import service as os_service
from ceilometer.openstack.common.rpc import service as rpc_service
from ceilometer import service
from ceilometer.openflow import drivers
from ceilometer.openflow.pollsters import port, flow

LOG = log.getLogger(__name__)

CONF_OPTS = [
    cfg.StrOpt('host_ip',
               default=['127.0.0.1'],
               help='IP address of the server to obtain IPMI information'),
    cfg.StrOpt('username',
               default=['admin'],
               help='User name of the IPMI interface'),
    cfg.StrOpt('password',
               default=['admin'],
               help='Password of the IPMI interface'),
]

cfg.CONF.register_opts(CONF_OPTS, group='ipmi')



class PollingTask(agent.PollingTask):
    
        
    def poll_and_publish(self):
        with self.publish_context as publisher:
            cache = {} #currently not used
            cache['host_ip'] = self.manager.host
            cache['username'] = self.manager.username
            cache['password'] = self.manager.password
            for pollster in self.pollsters:
                try:
                    LOG.info("Polling pollster %s", pollster.name)
                    samples = list(pollster.obj.get_samples(cache))
                    publisher(samples)
                except Exception as err:
                    LOG.warning('Continue after error from %s: %s',
                                pollster.name, err)
                    LOG.exception(err)
            


class AgentManager(agent.AgentManager):

    def __init__(self):
        super(AgentManager, self).__init__(
            extension.ExtensionManager(
                namespace='ceilometer.poll.ipmi',
                invoke_on_load=True,
            ),
        )
        
        '''TODO: need to put the sensitive information into a safe place'''
        self.host = cfg.CONF.ipmi.host_ip
        self.username = cfg.CONF.ipmi.username
        self.password = cfg.CONF.ipmi.password
        
    def create_polling_task(self):
        return PollingTask(self)


def agent_physicalserver():
    service.prepare_service()
    os_service.launch(rpc_service.Service(cfg.CONF.host,
                                          'ceilometer.agent.ipmi',
                                          AgentManager())).wait()
