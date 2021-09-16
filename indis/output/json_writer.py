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
from typing import Dict

from indis.cache import Cache
from indis.configuration import Configuration
from indis.output.output_writer import OutputWriter
from indis.provider.transfer import Transfer


class JsonFileWriter(OutputWriter):

    def __init__(self, config: Configuration):
        super().__init__(config)
        self.stats = dict()

    def write(self, transfer: Transfer, cache: Cache):

        for object_type in transfer.get_keys():
            if self.config and self.config.get('directory'):
                with open(self.config.get('directory') + "/" + object_type + '.json', 'w') as fd:
                    fd.write('[')
                    sep = ''
                    self.stats[object_type] = {'created': 0}
                    for key, value in transfer.get_copy()[object_type].items():
                        self.stats[object_type]['created'] += 1
                        fd.write(sep)
                        fd.write(value.to_json())
                        sep = ','
                    fd.write(']')
            else:
                print('[', end='')
                sep = ''
                self.stats[object_type] = {'created': 0}
                for key, value in transfer.get_copy()[object_type].items():
                    self.stats[object_type]['created'] += 1
                    print(sep, end='')
                    print(value.to_json(), end='')
                    sep = ','
                print(']', end='')

    def write_stats(self) -> Dict[str, Dict[str, Dict[str, int]]]:
        return self.stats
