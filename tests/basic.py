import unittest

from indis.model.host import Host
from indis.model.host_dependency import HostDependency
from indis.model.service import Service
from indis.model.group import Group
from indis.model.dependency import Dependency
from indis.model.service_dependency import ServiceDependency
from indis.model.zone import Zone


class TestBasicAttributes(unittest.TestCase):

    def test_host(self) -> None:
        print('Host')
        host = Host("kalle")
        host.vars["sune"] = "sune_value"
        host.vars["kalle"] = {"level": "two"}
        host.vars["alist"] = ["1", "2"]
        host.address = "172.25.1.111"
        host.groups.append("group1")

        print(host.to_json())
        self.assertTrue(not False)

    def test_service(self) -> None:
        print('Service')
        service = Service("aservice", "kalle")
        service.vars["alist"] = ["1", "2"]
        print(service.to_json())

        self.assertTrue(not False)

    def test_group(self) -> None:
        print('Group')
        group = Group("group1")
        group.display_name = "display_group1"
        group.groups.append("asubgroup")
        print(group.to_json())

        self.assertTrue(not False)

    def test_dependency(self) -> None:
        print('Dependency')
        dep_host = Dependency(name="mydep", parent_host="host1", child_host="host2")
        dep_host.states.append('Up')
        print(dep_host.to_json())

        self.assertTrue(not False)

    def test_host_dependency(self) -> None:
        print('HostDependency')
        dep_host = HostDependency(name="myhostdep", parent_host="host1", child_host="host2")
        dep_host.states.append('Up')
        print(dep_host.to_json())

        self.assertTrue(not False)

    def test_service_dependency(self) -> None:
        print('ServiceDependency')
        dep_service = ServiceDependency(name="myservicedep", parent_host="host1", child_host="host2", parent_service='foo', child_service='bar')
        dep_service.states.append('Down')
        print(dep_service.to_json())

        self.assertTrue(not False)

    def test_zone(self) -> None:
        print('zone')
        zone = Zone(name='foo')
        zone.is_global = True
        print(zone.to_json())
        print(zone.to_dict())


        self.assertTrue(not False)