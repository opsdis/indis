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

from typing import Dict, Any, Set

from indis.model.command import Command
from indis.model.dependency import Dependency
from indis.model.group import Group
from indis.model.host import Host
from indis.model.notification import Notification
from indis.model.service import Service


class Transfer:
    # Value object passing data
    def __init__(self):

        # dict hostname-> Host
        self.hosts: Dict[str, Host] = {}
        self.services: Dict[str, Service] = {}

        self.hostgroups: Dict[str, Group] = {}
        self.servicegroups: Dict[str, Group] = {}

        self.service_dependencies: Dict[str, Dependency] = {}
        self.host_dependencies: Dict[str, Dependency] = {}

        self.notifications: Dict[str, Notification] = {}
        self.commands: Dict[str, Command] = {}

        # Set of host name that should be excluded
        # self.hosts_exclude: Dict[str, Any] = {}

    def __setattr__(self, key, value):

        if not isinstance(value, dict):
            raise ValueError(f"{key} must be a dict")
        else:
            super().__setattr__(key, value)

    def __getattr__(self, key):

        if key in self.__dict__:
            return self.__dict__[key]
        else:
            raise AttributeError(f'{self.__class__.__name__} has no attribute name {key}')

    def get_copy(self) -> Dict[str, Any]:
        set_dict = {}
        for k, v in self.__dict__.items():
            if k and v:
                set_dict[k] = v
        return set_dict

    def get_keys(self) -> Set[str]:
        set_dict = set()
        for k, v in self.__dict__.items():
            if k and v:
                set_dict.add(k)
        return set_dict

    def get_by_name(self, name) -> Dict[str, Any]:
        return self.__dict__[name]

    def stats(self) -> Dict[str, int]:
        stats = {}
        for key, value in self.__dict__.items():
            stats[key] = len(value)
        return stats

    def dependency_order(self):
        return ['hostgroups', 'commands', 'hosts', 'servicegroups', 'services', 'service_dependencies',
                    'host_dependencies', 'notifications']
