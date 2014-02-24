
import abc
from stevedore import driver

def get_driver(name, host, port, namespace='ceilometer.openflow.d'):
    """Get OpenFlow driver and load it.

    :param name: name of the driver.
    :param namespace: Namespace to use to look for drivers.
    """
    
    loaded_driver = driver.DriverManager(namespace, name)
    return loaded_driver.driver(host,port)

class DriversBase(object):
    """Base class for plugins that publish the sampler."""

    __metaclass__ = abc.ABCMeta

    def __init__(self, abc):
        pass

    @abc.abstractmethod
    def testfunction(self, text):
        "Publish samples into final conduit."