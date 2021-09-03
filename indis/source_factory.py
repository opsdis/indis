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
import inspect
import logging

from indis.provider.source import Source
from indis.provider.transfer import Transfer

cmdblogging = logging.getLogger(__name__)


class Factory:

    def __init__(self, cmdb, configuration, reader: None):

        self.cmdb = cmdb
        try:
            self.source_name = configuration.get('source')[self.cmdb].get('name')
            self.source_module = configuration.get('source')[self.cmdb].get('class')
            self.source_interface = configuration.get('source')[self.cmdb].get('access').get('reader_inf')
            if not self.source_name or not self.source_module or not self.source_interface:
                raise AttributeError('Missing mandatory config for source')
        except Exception as err:
            raise AttributeError(err)

        self.cmdb_reader_name = None if configuration.get('source')[self.cmdb].get('access').get('reader') is None \
            else configuration.get('source')[cmdb].get('access').get('reader')

        self.configuration = configuration

        self.reader = None
        if reader:
            if isinstance(reader, Factory._get_class(self.source_interface)):
                self.reader = reader
            else:
                raise AttributeError("The reader object is not according to interface")

        # create Source object

        clazz = Factory._get_class(self.source_module)
        self.source_obj: Source = clazz(self.configuration.get(self.configuration.get('source')[self.cmdb].get('name')),
                                        self._get_reader())
        if not isinstance(self.source_obj, Source):
            raise AttributeError("The reader object is not according to interface")

    def _get_reader(self):
        """
        The method find and instantiate the Reader class for the cmdb.
        It support Reader __init__ constructors with 1 or 2 arguments.
        If 1 argument -> configuration
        If 2 arguments -> configuration, cmdb_name
        If using 2 arguments the Reader class do not need to know the configuration
        name for the cmdb.
        :return: object of the Reader class
        """

        if self.reader:
            return self.reader
        elif self.configuration.get('source')[self.cmdb].get('access').get('reader'):
            clazz = Factory._get_class(self.configuration.get('source')[self.cmdb].get('access').get('reader'))

            arg_list = inspect.getfullargspec(clazz.__init__).args

            if clazz and len(arg_list) == 2:
                #print(self.configuration.get(self.configuration.get('source')[self.cmdb].get('name')))
                return clazz(self.configuration.get(self.configuration.get('source')[self.cmdb].get('name')))
            else:
                return None
        else:
            return None

    def fetch(self) -> Transfer:
        """
        The method return a method, fetch, that is specific for the CMDB provider.
        The fetch method that is return must by itself return a dictionary of Host objects with the key of the host name
        and the hostgroup set with the name of the host groups as plain string.
        :return:
        """

        transfer = self.source_obj.fetch()

        cmdblogging.info("Using source factory {} ".format(self.source_name))

        return transfer

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
