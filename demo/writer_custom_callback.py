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

from cmdb2monitor.op5monitor.operations import Operations
from cmdb2monitor.op5monitor.writer_callback import MonitorCallback

TODO = 'todo'
DONE = 'done'
ERROR = 'error'
RESOURCE = 'resource'


class MonitorCustomCallback(MonitorCallback):
    """
    An example of a custom callback function that just prints the callbacks and show the content
    of the data.
    """

    def __init__(self):
        self.operations = dict(((ops, {TODO: 0, DONE: 0, ERROR: 0, RESOURCE: list()}) for ops in Operations))

    def change(self, operation: dict):
        print(f"callback todo operation - {operation['ops']} - {operation['resource']}")
        self.operations[operation['ops']][TODO] += 1
        self.operations[operation['ops']][RESOURCE].append(operation['resource'])

    def execute(self, operation: dict) -> bool:
        print(f"callback done operation - {operation['ops']} - {operation['resource']}")
        self.operations[operation['ops']][DONE] += 1
        if 'error' in operation:
            self.operations[operation['ops']][ERROR] += 1
        status = True
        return status
