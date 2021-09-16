# -*- coding: utf-8 -*-
"""
    Copyright (C) 2020  Opsdis AB

    This file is part of cmdb2monitor.

    cmdb2monitor is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    cmdb2monitor is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with cmdb2monitor.  If not, see <http://www.gnu.org/licenses/>.

"""
from indis.model.host import Host
from indis.model.group import Group
from indis.model.timeperiod import TimePeriod

from indis.provider.source import Source
import logging

from indis.provider.transfer import Transfer

cmdblog = logging.getLogger(__name__)


class NetworkSource(Source):

    # No __init__ method is allowed

    def fetch(self) -> Transfer:
        # Create a transfer object
        transfer = Transfer()

        # Create a timeperiod template
        tp = TimePeriod(name='opsdis_workday_tp', object_type='object')
        tp.display_name = 'Opsdis workhours'
        tp.ranges['monday'] = '8:00-17:00'
        tp.ranges['tuesday'] = '8:00-17:00'
        tp.ranges['wednesday'] = '8:00-17:00'
        tp.ranges['thursday'] = '8:00-17:00'
        tp.ranges['friday'] = '8:00-17:00'
        tp.ranges['saturday'] = '8:00-17:00'

        transfer.timeperiods[tp.object_name] = tp

        nodehosts = self.reader.read_hosts()

        for host_dict in nodehosts:
            host = Host(f"{host_dict['name'].lower().strip()}",object_type='template')

            # Start add Host attributes
            if 'check_command' in host_dict:
                host.check_command = host_dict['check_command']

            if 'max_check_attempts' in host_dict:
                host.max_check_attempts = host_dict['max_check_attempts']

            if 'check_period' in host_dict:
                host.check_period = host_dict['check_period']

            if 'check_timeout' in host_dict:
                host.check_period = host_dict['check_timeout']

            transfer.hosts[host.object_name] = host


        return transfer


