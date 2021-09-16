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
from typing import Dict, Set

import requests

from indis.cache import Cache
from indis.configuration import Configuration
from indis.logging import Log as log
from indis.output.output_writer import OutputWriter
from indis.provider.transfer import Transfer

UNKNOWN = 'unknown'
DELETED = 'deleted'
NOTMODIFIED = 'notmodified'
UPDATED = 'updated'
CREATED = 'created'
logger = log(__name__)


def map_write_status(status):
    if status == 201:
        return CREATED
    if status == 200:
        return UPDATED
    if status == 304:
        return NOTMODIFIED
    return UNKNOWN


def map_delete_status(status):
    if status == 200:
        return DELETED
    if status == 304:
        return NOTMODIFIED
    return UNKNOWN


class APIWriter(OutputWriter):

    def __init__(self, config: Configuration):
        super().__init__(config)
        self.cache = None
        self.stats_create = {}
        self.stats_create_template = {}
        self.stats_delete = {}
        self.con = Connection(self.config)
        self.transfer: Transfer = Transfer()

    def write(self, transfer: Transfer, cache: Cache):

        self.transfer = transfer
        # Cache the Transfer
        self.cache = cache

        # Write templates
        for object_type in transfer.dependency_order():
            if transfer.__dict__[object_type]:
                # the transfer object is not empty
                self.stats_create_template.update(self._write_template(object_type=object_type))

        logger.debug_fmt(log_kv=self.stats_create, message="api create/update template operations")

        # Write object - real
        # Must be written in a order
        for object_type in transfer.dependency_order():
            if transfer.__dict__[object_type]:
                # the transfer object is not empty
                self.stats_create.update(self._write_object(object_type=object_type))

        logger.debug_fmt(log_kv=self.stats_create, message="api create/update object operations")

        # Handling delete objects
        for object_type in transfer.__dict__.keys():
            deleted = self.cache.deleted(object_type=object_type)

            self.stats_delete.update(self._delete_object(object_type=object_type, objects=deleted))

        logger.debug_fmt(log_kv=self.stats_delete, message="api delete object operations")

        if self.config.get('deploy'):
            self.deploy()

    def write_stats(self) -> Dict[str, Dict[str, Dict[str, int]]]:
        stats = dict()
        stats['object'] = {}
        for object_type in self.transfer.__dict__.keys():

            stats['object'][object_type] = {UPDATED: 0, CREATED: 0, DELETED: 0, NOTMODIFIED: 0}
            if object_type in self.stats_create:
                for key, value in self.stats_create[object_type].items():
                    stats['object'][object_type][value] += 1
                for key, value in self.stats_delete[object_type].items():
                    stats['object'][object_type][value] += 1

        stats['template'] = {}
        for object_type in self.transfer.__dict__.keys():

            stats['template'][object_type] = {UPDATED: 0, CREATED: 0, DELETED: 0, NOTMODIFIED: 0}
            if object_type in self.stats_create_template:
                for key, value in self.stats_create_template[object_type].items():
                    stats['template'][object_type][value] += 1
                for key, value in self.stats_delete[object_type].items():
                    stats['template'][object_type][value] += 1

        return stats

    def _write_template(self, object_type: str) -> Dict[str, Dict[str, str]]:
        stats = {object_type: dict()}

        for key, value in self.transfer.get_copy()[object_type].items():
            if value.object_type == 'template':
                status = self.con.create_object(object_name=value.object_name, object_type=object_type,
                                                body=value.to_json())
                stats[object_type][value.object_name] = map_write_status(status)

        return stats

    def _write_object(self, object_type: str) -> Dict[str, Dict[str, str]]:
        stats = {object_type: dict()}

        for key, value in self.transfer.get_copy()[object_type].items():
            if value.object_type == 'object':
                status = self.con.create_object(object_name=value.object_name, object_type=object_type,
                                                body=value.to_json())
                stats[object_type][value.object_name] = map_write_status(status)

        return stats

    def _delete_object(self, object_type: str, objects: Set[str]) -> Dict[str, Dict[str, str]]:
        stats = {object_type: dict()}

        for object_name in objects:
            status = self.con.delete_object(object_name=object_name, object_type=object_type)
            stats[object_type][object_name] = map_delete_status(status)
        return stats

    def deploy(self):
        self.con.deploy()


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

        type = self.get_url(object_type)

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
                # no_error = True

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
            logger.info_timer('put', object_type, object_name, time.time() - start_time, status)

    def delete_object(self, object_name: str, object_type: str) -> int:
        type = self.get_url(object_type)

        no_error = False
        start_time = time.time()
        status = None

        try:

            r = requests.delete(f"{self.url}/{type}?name={object_name}",
                                auth=self.auth,
                                headers=self.headers,
                                verify=self.verify)

            if r.status_code == 200 or r.status_code == 201:
                status = r.status_code

            if not no_error:
                r.raise_for_status()

            return r.status_code

        except requests.exceptions.HTTPError as err:
            logger.warn("delete failed on: {} err {}".format(object_type, err))
            if r is None:
                raise err

            return r.status_code

        except requests.exceptions.RequestException as err:
            logger.error("delete failed on: {} err {}".format(self.url, err))
            raise err
        finally:
            logger.info_timer('delete', object_type, object_name, time.time() - start_time, status)

    def deploy(self) -> int:

        no_error = False
        start_time = time.time()
        status = None

        try:

            r = requests.post(f"{self.url}/config/deploy",
                              auth=self.auth,
                              headers=self.headers,
                              verify=self.verify)

            if r.status_code == 200 or r.status_code == 201:
                status = r.status_code

            if not no_error:
                r.raise_for_status()

            return r.status_code

        except requests.exceptions.HTTPError as err:
            logger.warn("get failed on: {} err {}".format('config/deployments', err))
            if r is None:
                raise err

            return r.status_code

        except requests.exceptions.RequestException as err:
            logger.error("get failed on: {} err {}".format(self.url, err))
            raise err
        finally:
            logger.info_timer('post', "config/deploy", "", time.time() - start_time, status)

    def get_url(self, object_type):
        type = ''
        if object_type == 'hosts':
            type = 'host'
        if object_type == 'hostgroups':
            type = 'hostgroup'
        if object_type == 'services':
            type = 'service'
        if object_type == 'servicegroups':
            type = 'servicegroup'
        if object_type == 'commands':
            type = 'command'
        if object_type == 'eventcommands':
            type = 'eventcommand'
        if object_type == 'notifications':
            type = 'notification'
        if object_type == 'timeperiods':
            type = 'timeperiod'
        if object_type == 'users':
            type = 'user'
        if object_type == 'usergroups':
            type = 'usergroup'
        if object_type == 'endpoints':
            type = 'endpoint'
        if object_type == 'zones':
            type = 'zone'
        return type
