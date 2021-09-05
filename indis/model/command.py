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

from typing import List, Dict, Any

from indis.model.common import Common, to_json, to_dict


class Command(Common):
    """
    Command is the same for CheckCommand, NotificationCommand and EventCommand
    """
    __initialized = False

    def __init__(self, name: str):
        super().__init__(name=name)
        #self.object_name = name
        # Array	Required. The command.: This can either be an array of individual command arguments. Alternatively a
        # string can be specified in which case the shell interpreter (usually /bin/sh) takes care of parsing the
        # command.
        # When using the “arguments” attribute this must be an array. Can be specified as function for advanced implementations.
        self.command: List[str] = list()
        # Dictionary	Optional. A dictionary of macros which should be exported as environment variables prior to executing the command.
        self.env: Dict[str, str] = dict()
        # Dictionary	Optional. A dictionary containing custom variables that are specific to this command.
        self.vars: Dict[str, Any] = dict()
        # Duration	Optional. The command timeout in seconds. Defaults to 1m.
        self.timeout: str = ''
        # Dictionary	Optional. A dictionary of command arguments.
        self.arguments: Dict[str, str] = dict()

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
