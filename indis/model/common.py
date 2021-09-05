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
from abc import abstractmethod
from typing import Dict, Any


class Common:

    def __init__(self, name):
        self.object_name = name
        self.object_type = 'object'

    @abstractmethod
    def to_json(self) -> str:
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        pass


def to_json(obj, initial=None, padding: bool = False) -> str:
    res = to_dict(initial, obj, padding)
    return json.dumps(res)


def to_dict(initial, obj=None, padding: bool = False) -> Dict[str, Any]:
    res = dict()
    for key, value in obj.__dict__.items():
        if key.startswith('_'):
            # Remove all protected attributes
            continue
        if key in obj._ind:
            res[key] = value
        elif isinstance(obj.__dict__[key], dict) and obj.__dict__[key]:
            res[key] = value
        elif isinstance(obj.__dict__[key], list) and obj.__dict__[key]:
            res[key] = value
        elif padding:
            res[key] = None
    if initial is not None:
        res.update(initial)
    return res
