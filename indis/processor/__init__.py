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

from indis.configuration import Configuration
from indis.processor.common import Processing
from indis.provider.transfer import Transfer
# The import of the classes that is subclasses of Processing
from indis.processor.groups import Groups
from indis.processor.vars import Vars


def processing(transfer: Transfer, config: Configuration) -> Dict[str, int]:
    """
    Find all processing "plugins", instantiate them and and execute the objects process() method.
    All classes to execute must be part of above imports
    Must been imported
    :param transfer:
    :param config:
    :return:
    """
    processed = {}
    for clazz in Processing.__subclasses__():
        proc_obj: Processing = clazz(transfer=transfer, config=config)
        processed[type(proc_obj).__name__] = proc_obj.process()
    return processed
