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
import time
from typing import Dict, List

import requests

from indis.logging import Log as log
from indis.output.output_writer import OutputWriter
from indis.provider.transfer import Transfer

logger = log(__name__)


class APIWriter(OutputWriter):

    def write(self, transfer: Transfer):
        self.con = Connection(self.config)
        self.transfer = transfer
        # Must be written in a order
        stats = {}
        stats.update(self.write_object('hostgroups'))
        stats.update(self.write_object('hosts'))
        logger.debug_fmt(log_kv=stats, message="icinga director api")

    def write_object(self, object_type) -> Dict[str, List[Dict[str, int]]]:
        stats = {object_type: list()}

        for key, value in self.transfer.get_copy()[object_type].items():
            status = self.con.create_object(object_name=value.object_name, object_type=object_type, body=value.to_json())
            stats[object_type].append({value.object_name: status})
        return stats


class Connection:

    def __init__(self, conf):
        user = conf.get('user')
        passwd = conf.get('password')
        self.url = conf.get('url')
        self.auth = (user, passwd)
        self.headers = {'Accept': 'application/json'}
        self.verify = False
        self.retries = 5

    def create_object(self, object_name: str, object_type: str, body: str) -> int:

        type = ''
        if object_type == 'hosts':
            type = 'host'
        if object_type == 'hostgroups':
            type = 'hostgroup'

        no_error = False
        start_time = time.time()
        status = None

        try:
            # Do PUT first - if the object exists it will be updated
            r = requests.put(f"{self.url}/{type}?name={object_name}",
                             data=body,
                             auth=self.auth,
                             headers=self.headers,
                             verify=self.verify)

            if r.status_code == 404:
                # If the object do not exist do POST
                r = requests.post(f"{self.url}/{type}",
                                 data=body,
                                 auth=self.auth,
                                 headers=self.headers,
                                 verify=self.verify)

                status = r.status_code
                no_error = True

            if r.status_code == 200 or r.status_code == 201:
                status = r.status_code

            if not no_error:
                r.raise_for_status()

            return r.status_code

        except requests.exceptions.HTTPError as err:
            logger.warn("put failed on: {} err {}".format(object_type, err))
            if r is None:
                raise err

            logger.dump_command('put', r.status_code, r.text, self.url, body)
            return r.status_code

        except requests.exceptions.RequestException as err:
            logger.error("put failed on: {} err {}".format(self.url, err))
            raise err
        finally:
            logger.info_timer('put', object_type, time.time() - start_time, 1, status)
