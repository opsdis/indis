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

import hashlib
from abc import abstractmethod
from typing import Set, Dict, Any

import redis

from indis.configuration import Configuration
from indis.provider.transfer import Transfer


class Cache:

    def __init__(self, transfer: Transfer):
        self.transfer = transfer

    @abstractmethod
    def diff(self) -> Transfer:
        pass

    @abstractmethod
    def deleted(self, object_type: str) -> Set[str]:
        pass

    @abstractmethod
    def updated(self, object_type: str) -> Set[str]:
        pass

    @abstractmethod
    def created(self, object_type: str) -> Set[str]:
        pass

    @abstractmethod
    def rollback(self):
        pass


class NoCache(Cache):

    def __init__(self, transfer: Transfer):
        super().__init__(transfer)

    def diff(self) -> Transfer:
        return None

    def deleted(self, object_type: str) -> Set[str]:
        return set()

    def updated(self, object_type: str) -> Set[str]:
        return set()

    def created(self, object_type: str) -> Set[str]:
        return set()

    def rollback(self):
        pass


class RedisCache(Cache):

    def __init__(self, prefix: str, transfer: Transfer, config: Configuration):
        super().__init__(transfer=transfer)
        self.redis_host = 'localhost' if config.get('host') is None else config.get('host')
        self.redis_port = '6379' if config.get('port') is None else config.get('port')
        self.redis_db = '0' if config.get('db') is None else config.get('db')
        self.redis_auth = None if config.get('auth') is None else config.get('auth')
        self.key_prefix = f"{prefix}:"
        self.con = self._get_cache_connection()

        self.transfer_existing: Dict[str, Dict[str, Any]] = dict()
        for object_type, value in transfer.__dict__.items():
            self.transfer_existing[object_type] = dict()
            for object in self.con.smembers(f"{self.key_prefix}{object_type}"):
                self.transfer_existing[object_type][object] = self.con.get(f"{self.key_prefix}{object_type}:{object}")
                self.con.delete(f"{self.key_prefix}{object_type}:{object}")
            self.con.delete(f"{self.key_prefix}{object_type}")

        self.transfer_current: Dict[str, Dict[str, Any]] = dict()
        pipe = self.con.pipeline()
        for object_type, value in transfer.__dict__.items():
            self.transfer_current[object_type] = dict()
            for key, obj in value.items():
                pipe.sadd(f"{self.key_prefix}{object_type}", key)
                sha = hashlib.sha256(obj.to_json().encode())
                self.transfer_current[object_type][key] = sha.hexdigest()
                pipe.set(f"{self.key_prefix}{object_type}:{key}", sha.hexdigest())
        pipe.execute()

    def rollback(self):
        """
        replace the current with existing
        :return:
        """
        pipe = self.con.pipeline()
        for object_type, value in self.transfer_existing.items():
            pipe.delete(f"{self.key_prefix}{object_type}")
            for key, sha_value in value.items():
                pipe.sadd(f"{self.key_prefix}{object_type}", key)
                pipe.set(f"{self.key_prefix}{object_type}:{object}", sha_value)

        pipe.execute()

    def diff(self) -> Transfer:
        pass

    def deleted(self, object_type: str) -> Set[str]:
        return self.transfer_existing[object_type].keys() - self.transfer_current[object_type].keys()

    def updated(self, object_type: str) -> Set[str]:
        return set()

    def created(self, object_type: str) -> Set[str]:
        return set()

    def _get_cache_connection(self):
        return redis.Redis(host=self.redis_host, port=self.redis_port, db=self.redis_db, password=self.redis_auth,
                           decode_responses=True)
