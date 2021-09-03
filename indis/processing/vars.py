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

from indis.processing.common import Processing


class Vars(Processing):

    def process(self) -> int:
        pc = self.config
        count = 0
        if pc and 'vars' in pc:

            for object_type in self.transfer.get_keys():
                if 'common' in pc['vars']:
                    for key, value in pc['vars']['common'].items():
                        for object_name in self.transfer.hosts.keys():
                            self.transfer.hosts[object_name].vars[key] = value
                            count += 1

                if object_type in pc['vars']:
                    # For each object specific
                    for key, value in pc['vars'][object_type].items():
                        # for object_name in self.transfer.hosts.keys():
                        for object_name in self.transfer.get_by_name('hosts').keys():
                            # self.transfer.hosts[object_name].vars[key] = value
                            self.transfer.get_by_name('hosts')[object_name].vars[key] = value
                            count += 1
        return count