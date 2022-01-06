# -*- coding: utf-8 -*-
"""
    Copyright (C) 2020  Opsdis AB

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

from demo.reader import Reader

import json


class FileReader(Reader):

    # Implement Reader.read_hosts method

    def read_hosts(self) -> list:
        return FileReader.get_content(self.config.get('demo_file'))

    def read_templates(self) -> list:
        return FileReader.get_content(self.config.get('demo_template_file'))

    @staticmethod
    def get_content(file_name: str) -> list:
        with open(file_name) as file:
            content = file.read()
            return json.loads(content)
