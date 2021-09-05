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

from indis.provider.source import Source
import logging

from indis.provider.transfer import Transfer

cmdblog = logging.getLogger(__name__)


class NetworkSource(Source):

    # No __init__ method is allowed

    def fetch(self) -> Transfer:
        nodehosts = self.reader.read_hosts()

        transfer = Transfer()
        for host_dict in nodehosts:
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
            host.notes_url = f"https://{host_dict['node'].lower().strip()}"

            if 'groups' in host_dict:
                for group in host_dict['groups']:
                    host.groups.append(group)
                    hostgroup = Group(name=group)
                    hostgroup.display_name = f"HOSTGROUP {group}"
                    transfer.hostgroups[hostgroup.object_name] = hostgroup

            host.imports.append('base_host')
            transfer.hosts[host.object_name] = host

        return transfer


