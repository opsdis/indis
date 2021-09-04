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

import os

import yaml


class Singleton(type):
    """
    Provide singleton pattern to MonitorConfig. A new instance is only created if:
     - instance do not exists
     - config is provide in constructor call, __init__
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances or args:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Configuration(object, metaclass=Singleton):

    def __init__(self, configfile=None):
        self.conf = {}
        try:
            if os.getenv('IND_CONF_FILE'):
                with open(os.getenv('IND_CONF_FILE'), 'r', encoding='utf-8') as yml_file:
                    self.conf = yaml.load(yml_file, Loader=yaml.FullLoader)

            elif configfile is None:
                with open("config.yml", 'r', encoding='utf-8') as yml_file:
                    self.conf = yaml.load(yml_file, Loader=yaml.FullLoader)
            else:
                with open(configfile, 'r', encoding='utf-8') as yml_file:
                    self.conf = yaml.load(yml_file)
        except FileNotFoundError as err:
            raise err

    @staticmethod
    def get_keys():
        return Configuration().conf.keys()

    @staticmethod
    def get(name):
        if name in Configuration().conf:
            return Configuration().conf[name]
        else:
            return None
