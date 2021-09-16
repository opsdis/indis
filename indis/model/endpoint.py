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


class EndPoint(Common):
    """
    Command is the same for CheckCommand, NotificationCommand and EventCommand
    """
    __initialized = False

    def __init__(self, name: str, object_type: str = 'object'):
        super().__init__(name=name, object_type=object_type)
        # String	Optional. The hostname/IP address of the remote Icinga 2 instance.
        self.host: str = ''
        # Number	Optional. The service name/port of the remote Icinga 2 instance. Defaults to 5665.
        self.port: int = 5565
        # Duration	Optional. Duration for keeping replay logs on connection loss. Defaults to 1d (86400 seconds).
        # Attribute is specified in seconds. If log_duration is set to 0, replaying logs is disabled. You could also
        # specify the value in human readable format like 10m for 10 minutes or 1h for one hour.
        self.log_duration: str = '1d'

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
