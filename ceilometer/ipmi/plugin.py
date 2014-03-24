#
# Copyright (C) 2014, The SAVI Project.
#
# @author: Jieyu Lin <Jieyu.lin@savinetwork.ca>

import abc

class ImpiPollster(object):
    """Base class for pollster in ipmi agent.
    """

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_samples(self,cache):
        """Return a list of sample corresponding to each pollster class.

        :param cache: A caching dictionary for passing data between pollsters and caching data
        """