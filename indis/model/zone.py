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
import json
from typing import List, Dict, Any

from indis.model.common import Common


class Zone(Common):
    """
    Command is the same for CheckCommand, NotificationCommand and EventCommand
    """
    __initialized = False

    def __init__(self, name: str, object_type: str = 'object'):
        super().__init__(name=name, object_type=object_type)
        # Array of object names	Optional. Array of endpoint names located in this zone.
        self.endpoints: List[str] = list()
        # Object name	Optional. The name of the parent zone. (Do not specify a global zone)
        self.parent: str = ''
        # Boolean	Optional. Whether configuration files for this zone should be synced to all endpoints. Defaults to false.
        # in icinga this is named global, but since its a reserved word in python its called is_global.
        # This is translated when json is generated
        self.is_global: bool = False

        self._ind = {'object_name', 'object_type'}
        self.__initialized = True

    def __setattr__(self, name, value):
        if self.__initialized:

            self._ind.add(name)
            object.__setattr__(self, name, value)
        else:
            object.__setattr__(self, name, value)

    # "Override" common since must handle translation from is_global to global
    def to_json(self) -> str:
        res = self.to_dict()
        return json.dumps(res)

    # "Override" common since must handle translation from is_global to global
    def to_dict(self) -> Dict[str, Any]:
        res = dict()
        for key, value in self.__dict__.items():
            if key.startswith('_'):
                # Remove all protected attributes
                continue
            if key in self._ind:
                if key == 'is_global':
                    res['global'] = value
                else:
                    res[key] = value
            elif isinstance(self.__dict__[key], dict) and self.__dict__[key]:
                res[key] = value
            elif isinstance(self.__dict__[key], list) and self.__dict__[key]:
                res[key] = value
            elif key == 'is_global':
                res['global'] = value
        return res
