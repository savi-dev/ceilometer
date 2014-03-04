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
    cfg.StrOpt('enable_drivers',
               default=['cpu_time', 'cpu_percent', 'cpu_time_percent'],
               help='a list of enabled drivers for polling information of the physical server'),
]

cfg.CONF.register_opts(CONF_OPTS, group='physicalserver')



class PollingTask(agent.PollingTask):
    
        
    def poll_and_publish(self):
        with self.publish_context as publisher:
            cache = {} #currently not used
            cache['host_name'] = socket.gethostname()
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
            named.NamedExtensionManager(
                namespace='ceilometer.poll.physicalserver',
                names=cfg.CONF.physicalserver.enable_drivers,
                invoke_on_load=True,
            ),
        )
        
        print self.pollster_manager.extensions
        print cfg.CONF.physicalserver.enable_drivers
        
        if not list(self.pollster_manager):
            LOG.warning('Failed to load any driver')
        
    def create_polling_task(self):
        return PollingTask(self)


def agent_physicalserver():
    service.prepare_service()
    os_service.launch(rpc_service.Service(cfg.CONF.host,
                                          'ceilometer.agent.physicalserver',
                                          AgentManager())).wait()
