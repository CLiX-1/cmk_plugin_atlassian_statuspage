#!/usr/bin/env python3
# -*- coding: utf-8; py-indent-offset: 4; max-line-length: 100 -*-

# Copyright (C) 2025  Christopher Pommer <cp.software@outlook.de>

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.


####################################################################################################
# Checkmk check plugin for monitoring the components from an Atlassian statuspage.
# The plugin works with data from the Atlassian Statuspage special agent (atlassian_statuspage).

# Example data from special agent:
# <<<atlassian_statuspage_comp_health:sep(0)>>>
# [
#     {
#         "component_name": "SMS Messaging",
#         "status": "operational",
#         "description": "The SMS Messaging service."
#     },
#     ...
# ]


import json
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any


from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    Result,
    Service,
    State,
    StringTable,
)


@dataclass(frozen=True)
class ComponentStatus:
    component_name: str
    status: str
    description: str | None
    url: str


Section = Mapping[str, ComponentStatus]


def parse_atlassian_statuspage_comp_health(string_table: StringTable) -> Section:
    parsed = {}
    for item in json.loads("".join(string_table[0])):
        parsed[item["component_name"]] = ComponentStatus(**item)
    return parsed


def discover_atlassian_statuspage_comp_health(section: Section) -> DiscoveryResult:
    for group in section:
        yield Service(item=group)


def check_atlassian_statuspage_comp_health(
    item: str, params: Mapping[str, Any], section: Section
) -> CheckResult:
    component = section.get(item)
    if component is None:
        return

    details = (
        f"Statuspage: {component.url}\n"
        f"Description: {component.description if component.description else '(Not available)'}"
    )

    component_status_lower = component.status.lower()
    if component_status_lower not in params:
        yield Result(
            state=State.UNKNOWN,
            summary=f"Status: {component.status.capitalize()} (undefined)",
            details=details,
        )
    else:
        yield Result(
            state=State(params[component_status_lower]),
            summary=f"Status: {component.status.capitalize()}",
            details=details,
        )


agent_section_atlassian_statuspage_comp_health = AgentSection(
    name="atlassian_statuspage_comp_health",
    parse_function=parse_atlassian_statuspage_comp_health,
)


check_plugin_atlassian_statuspage_comp_health = CheckPlugin(
    name="atlassian_statuspage_comp_health",
    service_name="Health %s",
    discovery_function=discover_atlassian_statuspage_comp_health,
    check_function=check_atlassian_statuspage_comp_health,
    check_ruleset_name="atlassian_statuspage_comp_health",
    check_default_parameters={
        "operational": 0,
        "degraded_performance": 1,
        "partial_outage": 2,
        "major_outage": 2,
    },
)
