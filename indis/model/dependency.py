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

from indis.model.common import Common, to_json, to_dict


class Dependency(Common):
    __initialized = False

    def __init__(self, name: str, parent_host: str, child_host: str):
        super().__init__(name=name, object_type='object')
        # self.object_name = name
        # Object name	Required. The parent host.
        self.parent_host_name = parent_host
        # Object name	Optional. The parent service. If omitted, this dependency object is treated as host dependency.
        self.parent_service_name = ''
        # Object name	Required. The child host.
        self.child_host_name = child_host
        # Object name	Optional. The child service. If omitted, this dependency object is treated as host dependency.
        self.child_service_name = ''
        # Boolean	Optional. Whether to disable checks (i.e., don’t schedule active checks and drop passive results) when this dependency fails. Defaults to false.
        self.disable_checks = False
        # Boolean	Optional. Whether to disable notifications when this dependency fails. Defaults to true.
        self.disable_notifications = True
        # Boolean	Optional. Whether to ignore soft states for the reachability calculation. Defaults to true.
        self.ignore_soft_states = True
        # Object name	Optional. Time period object during which this dependency is enabled.
        self.period = ''
        # Array	Optional. A list of state filters when this dependency should be OK. Defaults to [ OK, Warning ] for services and [ Up ] for hosts.
        self.states = list()

        self._ind = {'object_name', 'object_type', 'parent_host_name', 'child_host_name'}
        self.__initialized = True

    def __setattr__(self, name, value):
        if self.__initialized:

            self._ind.add(name)
            object.__setattr__(self, name, value)
        else:
            object.__setattr__(self, name, value)

    def to_json(self):
        return to_json(self)

    def to_dict(self):
        return to_dict(self)
