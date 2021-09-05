# -*- coding: utf-8 -*-
"""
    Copyright (C) 2021  Opsdis AB

    This file is part of indis - Icinga native directory importer service.

    indis is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    indis is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with indis.  If not, see <http://www.gnu.org/licenses/>.

"""

from indis.processor.common import Processing
from indis.model.group import Group


class Groups(Processing):

    def process(self) -> int:
        pc = self.config
        count = 0
        if pc and 'groups' in pc:

            create_hostgroups = set()
            for object_type in self.transfer.get_keys():
                if object_type in pc.get('groups'):
                    # For each object specific
                    for group in pc.get('groups')[object_type]:
                        for object_name in self.transfer.hosts.keys():
                            self.transfer.hosts[object_name].groups.append(group)
                            create_hostgroups.add(Group(name=group))
                            count += 1

            # Add hostgroups that is added since it may not exists
            for host_group in create_hostgroups:
                self.transfer.hostgroups[host_group.object_name] = host_group

        return count
