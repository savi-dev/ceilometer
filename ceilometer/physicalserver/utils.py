#
# Copyright (C) 2014, The SAVI Project.
#
# @author: Jieyu Lin <Jieyu.lin@savinetwork.ca>

from ceilometer import sample
from ceilometer.openstack.common import timeutils


def make_sample(name, type, unit, volumn, resource_id):
    return sample.Sample(
                name=name,
                type=type,
                unit=unit,
                volume=volumn,
                user_id=None,
                project_id=None,
                resource_id=resource_id,
                timestamp=timeutils.isotime(),
                resource_metadata=None,)
