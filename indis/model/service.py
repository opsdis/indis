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

from indis.model.basic_attributes import BasicAttributes

from indis.model.common import Common, to_json, to_dict


class Service(Common, BasicAttributes):
    __initialized = False

    def __init__(self, name: str, host_name: str):
        super().__init__(name)
        # 	Object name	Required. The host this service belongs to. There must be a Host object with that name.
        self.host_name = host_name

        self.__initialized = True

    def __setattr__(self, name, value):
        if self.__initialized:
            # your __setattr__ implementation here
            self._ind.add(name)
            object.__setattr__(self, name, value)
        else:
            object.__setattr__(self, name, value)

    def to_json(self, padding: bool = False):
        res = {'host_name': self.host_name}
        return to_json(self, res)

    def to_dict(self):
        res = {'host_name': self.host_name}
        return to_dict(self, res)
