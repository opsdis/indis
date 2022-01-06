# -*- coding: utf-8 -*-
"""
    Copyright (C) 2020 Opsdis AB

    This file is part of cmdb2monitor.

    cmdb2monitor is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    cmdb2monitor is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with cmdb2monitor.  If not, see <http://www.gnu.org/licenses/>.


"""

from abc import abstractmethod

from indis.provider.source_reader import SourceReader


class Reader(SourceReader):

    @abstractmethod
    def read_hosts(self) -> list:
        pass

    @abstractmethod
    def read_templates(self) -> list:
        pass
