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

import logging
from typing import Dict

from indis.cache import Cache
from indis.output.output_writer import OutputWriter
from indis.provider.transfer import Transfer

cmdblogging = logging.getLogger(__name__)


class Factory:

    def __init__(self, cmdb, configuration):

        self.cmdb = cmdb

        self.output_name = configuration.get('output').get('writer')
        if not self.output_name:
            self.output_name = "indis.output.json_writer.JsonFileWriter"

        self.configuration = configuration.get('output').get('configuration')

        self.reader = None

        clazz = Factory._get_class(self.output_name)
        self.writer_obj: OutputWriter = clazz(self.configuration)
        if not isinstance(self.writer_obj, OutputWriter):
            raise AttributeError("The writer object is not according to interface")

    def write(self, transfer: Transfer, cache: Cache):
        """
        The method return a method, fetch, that is specific for the CMDB provider.
        The fetch method that is return must by itself return a dictionary of Host objects with the key of the host name
        and the hostgroup set with the name of the host groups as plain string.
        :return:
        """

        cmdblogging.info("Using writer factory {} ".format(self.writer_obj))
        self.writer_obj.write(transfer, cache)

    def write_stats(self) -> Dict[str, Dict[str, int]]:
        return self.writer_obj.write_stats()

    @staticmethod
    def _get_module(name):
        return __import__(name, fromlist=[''])

    @staticmethod
    def _get_class(kls):

        try:
            parts = kls.split('.')
            module = ".".join(parts[:-1])
            m = __import__(module)
            for comp in parts[1:]:
                m = getattr(m, comp)
            return m
        except Exception as err:
            cmdblogging.error(f"Class {kls} failed {err}")
            raise err
