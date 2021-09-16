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

from typing import List, Dict

from indis.model.common import Common, to_json, to_dict


class TimePeriod(Common):
    """
    Command is the same for CheckCommand, NotificationCommand and EventCommand
    """
    __initialized = False

    def __init__(self, name: str, object_type: str = 'object'):
        super().__init__(name=name, object_type=object_type)
        # String	Optional. A short description of the time period.
        self.display_name: str = ''
        # Dictionary	Required. A dictionary containing information which days and durations apply to this timeperiod.
        self.ranges: Dict[str, str] = dict()
        # Boolean	Optional. Whether to prefer timeperiods includes or excludes. Default to true.
        self.prefer_includes = True
        # Array of object names	Optional. An array of timeperiods, which should exclude from your timerange.
        self.excludes: List[str] = list()
        # Array of object names	Optional. An array of timeperiods, which should include into your timerange
        self.includes: List[str] = list()

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
