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
# This is part of the Checkmk special agent for monitoring Atlassian Statuspage.
# It builds the configuration parameters for the special agent call.


from pydantic import BaseModel
from typing import Iterator, List, Optional

from cmk.server_side_calls.v1 import (
    EnvProxy,
    HostConfig,
    NoProxy,
    Secret,
    SpecialAgentCommand,
    SpecialAgentConfig,
    URLProxy,
)


class Params(BaseModel):
    url: str
    filter: tuple[str, list[str]] = ("", [])
    proxy: Optional[URLProxy | NoProxy | EnvProxy] = None
    timeout: Optional[float] = 10.0


def generate_special_agent_commands(
    params: Params,
    _host_config: HostConfig,
) -> Iterator[SpecialAgentCommand]:
    args: List[str | Secret] = [
        "--url",
        params.url,
        "--timeout",
        str(params.timeout),
    ]

    if params.filter[0] == "filter_include":
        args += ["--filter-include", ",".join(params.filter[1])]
    elif params.filter[0] == "filter_exclude":
        args += ["--filter-exclude", ",".join(params.filter[1])]

    if params.proxy:
        match params.proxy:
            case URLProxy(url=url):
                args += ["--proxy", url]
            case EnvProxy():
                args += ["--proxy", "FROM_ENVIRONMENT"]
            case NoProxy():
                args += ["--proxy", "NO_PROXY"]

    yield SpecialAgentCommand(command_arguments=args)


special_agent_atlassian_statuspage = SpecialAgentConfig(
    name="atlassian_statuspage",
    parameter_parser=Params.model_validate,
    commands_function=generate_special_agent_commands,
)
