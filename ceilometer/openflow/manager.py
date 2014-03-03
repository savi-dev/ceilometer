# -*- encoding: utf-8 -*-
#
# Copyright © 2012-2013 eNovance <licensing@enovance.com>
#
# Author: Julien Danjou <julien@danjou.info>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from oslo.config import cfg
from stevedore import extension
from stevedore import driver
import socket 

from ceilometer import agent
from ceilometer.openstack.common import log
from ceilometer.openstack.common import service as os_service
from ceilometer.openstack.common.rpc import service as rpc_service
from ceilometer import service
from ceilometer.openflow import drivers
from ceilometer.openflow.pollsters import port, flow

LOG = log.getLogger(__name__)

CONF_OPTS = [
    cfg.StrOpt('of_ctrl_host',
               default=socket.gethostbyname(socket.gethostname()),
               help='host address of the node that has OpenFlow controller running'),
    cfg.StrOpt('of_ctrl_port',
               default=8090,
               help='host port number of the node that has OpenFlow controller running'),
    cfg.StrOpt('ofi_driver',
               default='ryu',
               help='driver for communicating with the OpenFlow controller'),
]

cfg.CONF.register_opts(CONF_OPTS, group='openflow')



class PollingTask(agent.PollingTask):
    def poll_and_publish_stat(self, stats, pollster_type):
        with self.publish_context as publisher:
            for switch in stats:
                s_stat = stats[switch]
                cache = {} #currently not used
                for pollster in self.pollsters:
                    try:
                        if pollster.obj.get_type()==pollster_type:
                            LOG.info("Polling pollster %s", pollster.name)
                            samples = list(pollster.obj.get_samples(
                                switch,
                                s_stat,
                            ))
                            publisher(samples)
                    except Exception as err:
                        LOG.warning('Continue after error from %s: %s',
                                    pollster.name, err)
                        LOG.exception(err)


    def poll_and_publish(self):
        try:
            switches = self.manager.ofDriver.get_switches()
            if not switches:
                LOG.warning('no switch is connected to the current controller, there maybe configuration issue')
        except Exception as err:
            LOG.exception('Unable to retrieve switches information: %s', err)
            return
        
        try:
            switches_port_stats = {}
            switches_flow_stats = {}
            for switch in switches:
                LOG.info('Get port and flow statistic for switch: %s', switch)
                port_stats = self.manager.ofDriver.get_ports(switch)
                flow_stats = self.manager.ofDriver.get_flows(switch)
                switches_port_stats[switch] = port_stats
                switches_flow_stats[switch] = flow_stats
                LOG.info('Received port statistic: %s', port_stats)
                LOG.info('Received flow statistic: %s', flow_stats)
        except Exception as err:
            LOG.exception('Unable to retrieve stats: %s', err)
        else:
            self.poll_and_publish_stat(switches_port_stats, port.PORT_TYPE)
            self.poll_and_publish_stat(switches_flow_stats, flow.FLOW_TYPE)
            


class AgentManager(agent.AgentManager):

    def __init__(self):
        super(AgentManager, self).__init__(
            extension.ExtensionManager(
                namespace='ceilometer.poll.openflow',
                invoke_on_load=True,
            ),
        )
        self.ofDriver = drivers.get_driver(cfg.CONF.openflow.ofi_driver, 
                                            cfg.CONF.openflow.of_ctrl_host, 
                                            cfg.CONF.openflow.of_ctrl_port)
        #self.ofDriver = driver.RyuNetworkDriver(cfg.CONF.openflow.of_ctrl_host, cfg.CONF.openflow.of_ctrl_port)
    def create_polling_task(self):
        return PollingTask(self)

#     def setup_notifier_task(self):
#         """For nova notifier usage."""
#         task = PollingTask(self)
#         for pollster in self.pollster_manager.extensions:
#             task.add(
#                 pollster,
#                 self.pipeline_manager.pipelines)
#         self.notifier_task = task
# 
#     def poll_instance(self, context, instance):
#         """Poll one instance."""
#         self.notifier_task.poll_and_publish_instances([instance])

#     @property
#     def inspector(self):
#         return self._inspector



def agent_compute():
    service.prepare_service()
    os_service.launch(rpc_service.Service(cfg.CONF.host,
                                          'ceilometer.agent.openflow',
                                          AgentManager())).wait()
