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

from typing import Dict, Any, List

from indis.model.common import Common, to_json, to_dict


class Notification(Common):
    __initialized = False

    def __init__(self, name: str, object_type: str = 'object'):
        super().__init__(name=name, object_type=object_type)
        # self.object_name: str = name
        # Object name	Required. The name of the host this notification belongs to.
        self.host_name: str = ''
        # Object name	Optional. The short name of the service this notification belongs to. If omitted, this notification object is treated as host notification.
        self.service_name: str = ''
        # Dictionary	Optional. A dictionary containing custom variables that are specific to this notification object.
        self.vars: Dict[str, Any] = dict()
        # Array of object names	Required. A list of user names who should be notified. Optional. if the user_groups attribute is set.
        self.users: List[str] = list()
        # Array of object names	Required. A list of user group names who should be notified. Optional. if the users attribute is set.
        self.user_groups: List[str] = list()
        # Dictionary	Optional. A dictionary containing begin and end attributes for the notification.
        self.times: Dict[str, str] = dict()
        # Object name	Required. The name of the notification command which should be executed when the notification is triggered.
        self.command: str = ''
        # Duration	Optional. The notification interval (in seconds). This interval is used for active notifications. Defaults to 30 minutes. If set to 0, re-notifications are disabled.
        self.interval: int = 0
        # Object name	Optional. The name of a time period which determines when this notification should be triggered. Not set by default (effectively 24x7).
        self.period: str = ''
        # Object name	Optional. The zone this object is a member of. Please read the distributed monitoring chapter for details.
        self.zone: str = ''
        # Array	Optional. A list of type filters when this notification should be triggered. By default everything is matched.
        self.types: List[str] = list()
        # Array	Optional. A list of state filters when this notification should be triggered. By default everything is matched. Note that the states filter is ignored for notifications of type Acknowledgement!
        self.states: List[str] = list()

        self._ind = {'object_name', 'object_type'}
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
