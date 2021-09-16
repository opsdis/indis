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
from indis.model.common import to_json, to_dict


class Host(BasicAttributes):
    __initialized = False

    def __init__(self, name, object_type: str = 'object'):
        super().__init__(name=name, object_type=object_type)

        # String Optional. The host’s IPv4 address. Available as command runtime macro $address$ if set.
        self.address = None
        # String	Optional. The host’s IPv6 address. Available as command runtime macro $address6$ if set.
        self.address6 = None
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
