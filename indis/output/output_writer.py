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

from abc import abstractmethod
from typing import Dict

from indis.cache import Cache
from indis.configuration import Configuration
from indis.provider.transfer import Transfer


class OutputWriter:
    def __init__(self, config: Configuration):
        self.config = config

    @abstractmethod
    def write(self, transfer: Transfer, cache: Cache):
        pass

    @abstractmethod
    def write_stats(self) -> Dict[str, Dict[str, Dict[str, int]]]:
        pass
