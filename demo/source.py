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
from typing import Dict, Any

from indis.model.basic_attributes import BasicAttributes
from indis.model.host import Host
from indis.model.group import Group
from indis.model.service import Service
from indis.model.timeperiod import TimePeriod

from indis.provider.source import Source
import logging

from indis.provider.transfer import Transfer

cmdblog = logging.getLogger(__name__)


class NetworkSource(Source):

    # No __init__ method is allowed

    def fetch(self) -> Transfer:
        transfer = Transfer()
        self.create_timeperiod(transfer)
        self.create_templates(transfer)
        self.create_host_services(transfer)
        return transfer

    def create_host_services(self, transfer):
        demo_hosts = self.reader.read_hosts()
        for host_dict in demo_hosts:

            # Create host
            host = Host(f"{host_dict['node'].lower().strip()}")

            # Start add Host attributes
            if 'address' in host_dict:
                host.address = host_dict['address'].lower().strip()
            else:
                host.address = host_dict['node'].lower().strip()

            if 'alias' in host_dict:
                host.display_name = host_dict['alias'].strip()

            if 'info' in host_dict:
                host.notes = host_dict['info'].strip()

            if 'tags' in host_dict:
                if isinstance(host_dict['tags'], dict):
                    for key, value in host_dict['tags'].items():
                        host.vars[key] = value

            host.vars['web'] = "true"

            if 'tcp_ports' in host_dict:
                host.vars["my_ports"] = host_dict['tcp_ports']

            host.notes_url = f"https://{host_dict['node'].lower().strip()}"
            if 'parent' in host_dict:
                host.vars['parent'] = host_dict['parent']

            # Create groups
            if 'groups' in host_dict:
                for group in host_dict['groups']:
                    # Add groups to host
                    host.groups.append(group)

                    # Add groups to hostgroups
                    hostgroup = Group(name=group)
                    hostgroup.display_name = f"HOSTGROUP {group}"
                    transfer.hostgroups[hostgroup.object_name] = hostgroup

            # Add host template
            host.imports.append('demo_host_template')

            # Create service
            if 'tcp_protocols' in host_dict:
                for interface in host_dict['tcp_protocols']:
                    service = Service(host_name=host.object_name, name=f"Check {interface['protocol']}")
                    service.vars['tcp_port'] = interface['port']
                    service.display_name = f"Check_{interface['protocol']}"
                    service.enable_active_checks = True
                    transfer.services[service.object_name] = service
                    service.imports.append('demo_tcp_service_template')

            transfer.hosts[host.object_name] = host

    def create_templates(self, transfer: Transfer):

        templates = self.reader.read_templates()

        for template_dict in templates:
            if template_dict['type'] == 'host':
                template = Host(f"{template_dict['name'].lower().strip()}", object_type='template')
                self.set_template(template, template_dict)
                transfer.hosts[template.object_name] = template
            elif template_dict['type'] == 'service':
                template = Service(f"{template_dict['name'].lower().strip()}", object_type='template')
                self.set_template(template, template_dict)
                transfer.services[template.object_name] = template

    def set_template(self, template: BasicAttributes, template_dict: Dict[str, Any]):
        if 'check_command' in template_dict:
            template.check_command = template_dict['check_command']
        if 'max_check_attempts' in template_dict:
            template.max_check_attempts = template_dict['max_check_attempts']
        if 'check_period' in template_dict:
            template.check_period = template_dict['check_period']
        if 'check_timeout' in template_dict:
            template.check_timeout = template_dict['check_timeout']
        if 'import' in template_dict:
            template.imports.append(template_dict['import'])

    def create_timeperiod(self, transfer):
        tp = TimePeriod(name='demo_workday', object_type='object')
        tp.display_name = 'Demo workhours'
        tp.ranges['monday'] = '8:00-17:00'
        tp.ranges['tuesday'] = '8:00-17:00'
        tp.ranges['wednesday'] = '8:00-17:00'
        tp.ranges['thursday'] = '8:00-17:00'
        tp.ranges['friday'] = '1:00-17:00'
        tp.ranges['saturday'] = '8:00-17:00'

        transfer.timeperiods[tp.object_name] = tp
