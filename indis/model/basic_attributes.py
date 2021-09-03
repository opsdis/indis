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

from typing import List, Dict, Any


class BasicAttributes:
    __initialized = False

    def __init__(self, name: str):
        self.object_name = name
        # String	Optional. A short description of the service.
        self.display_name = ''
        # Array of object names	Optional. The service groups this service belongs to.
        self.groups: List[str] = list()
        # Dictionary	Optional. A dictionary containing custom variables that are specific to this service.
        self.vars: Dict[str, Any] = dict()
        # Object name	Required. The name of the check command.
        self.check_command: str = ''
        # Number	Optional. The number of times a service is re-checked before changing into a hard state. Defaults to 3.
        self.max_check_attempts: int = 3
        # Object name	Optional. The name of a time period which determines when this service should be checked. Not set by default (effectively 24x7).
        self.check_period: str = ''
        # Duration	Optional. Check command timeout in seconds. Overrides the CheckCommand’s timeout attribute.
        self.check_timeout: int = 0
        # Duration	Optional. The check interval (in seconds). This interval is used for checks when the service is in a HARD state. Defaults to 5m.
        self.check_interval: str = '5m'
        # Duration	Optional. The retry interval (in seconds). This interval is used for checks when the service is in a SOFT state. Defaults to 1m. Note: This does not affect the scheduling after a passive check result.
        self.retry_interval: int = 0
        # Boolean	Optional. Whether notifications are enabled. Defaults to true.
        self.enable_notifications: bool = True
        # Boolean	Optional. Whether active checks are enabled. Defaults to true.
        self.enable_active_checks: bool = True
        # Boolean	Optional. Whether passive checks are enabled. Defaults to true.
        self.enable_passive_checks: bool = True
        # Boolean	Optional. Enables event handlers for this host. Defaults to true.
        self.enable_event_handler: bool = True
        # Boolean	Optional. Whether flap detection is enabled. Defaults to false.
        self.enable_flapping: bool = False
        # Boolean	Optional. Whether performance data processing is enabled. Defaults to true.
        self.enable_perfdata: bool = True
        # Object name	Optional. The name of an event command that should be executed every time the service’s state changes or the service is in a SOFT state.
        self.event_command: str = ''
        # Number	Optional. Flapping upper bound in percent for a service to be considered flapping. 30.0
        self.flapping_threshold_high: float = 30.0
        # Number	Optional. Flapping lower bound in percent for a service to be considered not flapping. 25.0
        self.flapping_threshold_low: float = 25.0
        # Array	Optional. A list of states that should be ignored during flapping calculation. By default no state is ignored.
        self.flapping_ignore_states: List[str] = list()
        # Boolean	Optional. Treat all state changes as HARD changes. See here for details. Defaults to false.
        self.volatile: bool = False
        # Object name	Optional. The zone this object is a member of. Please read the distributed monitoring chapter for details.
        self.zone: str = ''
        # Object name	Optional. The endpoint where commands are executed on.
        self.command_endpoint: str = ''
        # String	Optional. Notes for the service.
        self.notes: str = ''
        # String	Optional. URL for notes for the service (for example, in notification commands).
        self.notes_url: str = ''
        # String	Optional. URL for actions for the service (for example, an external graphing tool).
        self.action_url: str = ''
        # String	Optional. Icon image for the service. Used by external interfaces only.
        self.icon_image: str = ''
        # String	Optional. Icon image description for the service. Used by external interface only.
        self.icon_image_alt: str = ''

        self._ind = {'object_name'}
        self.__initialized = True

    def __setattr__(self, name, value):
        if self.__initialized:
            self._ind.add(name)
            object.__setattr__(self, name, value)
        else:
            object.__setattr__(self, name, value)

    def __getattr__(self, name):
        if name == 'groups':
            return list(set(self.groups))
        else:
            return object.__getattr__(self, name)
