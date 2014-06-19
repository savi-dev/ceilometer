# -*- encoding: utf-8 -*-
#
# Copyright © 2013 eNovance
#
# Author: Mehdi Abaakouk <mehdi.abaakouk@enovance.com>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# Alarm notifier using Email

import eventlet
import requests
import urlparse

from oslo.config import cfg

from ceilometer.alarm import notifier
from ceilometer.openstack.common import jsonutils
from ceilometer.openstack.common import log

import smtplib

LOG = log.getLogger(__name__)

CONF_OPTS = [
    cfg.StrOpt('from_addr',
               help='Email address of the sender'),
    cfg.StrOpt('email_password',
               help='Email password of the sender'),
    cfg.StrOpt('send_to_addr',
               help='Email address to send'),

]


cfg.CONF.register_opts(CONF_OPTS, group='email')




class EmailAlarmNotifier(notifier.AlarmNotifier):
    """Email alarm notifier."""

    @staticmethod
    def notify(action, alarm_id, previous, current, reason):
        LOG.info("Notifying alarm %s from %s to %s with action %s because %s",
                 alarm_id, previous, current, action, reason)
        body = {'alarm_id': alarm_id, 'previous': previous,
                'current': current, 'reason': reason}
        kwargs = {'data': jsonutils.dumps(body)}
        
	to = cfg.CONF.email.send_to_addr 
        from_addr=cfg.CONF.email.from_addr
        addr_pwd=cfg.CONF.email.email_password
       
        print "to is: %s"% to
        print "from_addr: %s"% from_addr
        print "addr_pwd: %s"% addr_pwd 
      
	smtpserver = smtplib.SMTP("smtp.gmail.com",587)
	smtpserver.ehlo()
	smtpserver.starttls()
	smtpserver.ehlo
	smtpserver.login(from_addr, addr_pwd)
	header = 'To:' + to + '\n' + 'From: ' + from_addr + '\n' + 'Subject:Alarm Notification \n'
	msg = header + '\n An alarm has been triggered because the data received from the meter crossed the threshold set in the alarm.\n\n' 
        info = 'Alarm ID: '+ body["alarm_id"]+ '\n'
        info = info + 'Previous State: '+ body["previous"]+ '\n'
        info = info + 'Current State: '+ body["current"]+ '\n'
        info = info + 'Reason: '+ body["reason"]+ '\n'

        msg = msg + info     
    
	try: 
            smtpserver.sendmail(from_addr, to, msg)
            smtpserver.close()
            LOG.info("Successfully sent email to user")
        except RuntimeError as e:
	    LOG.error("Failed to send email to user, Reason: %s"% e)

