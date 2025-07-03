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
# Checkmk ruleset for configuration of the Atlassian Statuspage special agent.


from cmk.rulesets.v1 import Help, Message, Title
from cmk.rulesets.v1.form_specs import (
    CascadingSingleChoice,
    CascadingSingleChoiceElement,
    DefaultValue,
    DictElement,
    Dictionary,
    FieldSize,
    InputHint,
    List,
    Proxy,
    String,
    TimeMagnitude,
    TimeSpan,
)
from cmk.rulesets.v1.form_specs.validators import LengthInRange, NumberInRange, Url, UrlProtocol
from cmk.rulesets.v1.rule_specs import SpecialAgent, Topic


def _parameter_form_special_agent_atlassian_statuspage() -> Dictionary:
    return Dictionary(
        title=Title("Atlassian Statuspage"),
        help_text=Help(
            "This special agent requests data from an Atlassian statuspages. To monitor a "
            "statuspage, add this rule to a single host.<br>You may also want to adjust the query "
            "interval with the rule <b>Normal check interval for service checks</b>."
        ),
        elements={
            "url": DictElement(
                parameter_form=String(
                    title=Title("Statuspage URL"),
                    help_text=Help("The URL of the Atlassian statuspage."),
                    field_size=FieldSize.LARGE,
                    custom_validate=[
                        Url(
                            protocols=[
                                UrlProtocol.HTTP,
                                UrlProtocol.HTTPS,
                            ]
                        ),
                        LengthInRange(
                            min_value=1,
                        ),
                    ],
                ),
                required=True,
            ),
            "filter": DictElement(
                parameter_form=CascadingSingleChoice(
                    title=Title("Filter Components"),
                    help_text=Help(
                        "Set a filter to either include or exclude specific components."
                    ),
                    elements=[
                        CascadingSingleChoiceElement(
                            name="filter_include",
                            title=Title("Include"),
                            parameter_form=List[str](
                                element_template=String(),
                            ),
                        ),
                        CascadingSingleChoiceElement(
                            name="filter_exclude",
                            title=Title("Exclude"),
                            parameter_form=List[str](
                                element_template=String(),
                            ),
                        ),
                    ],
                    prefill=DefaultValue("filter_include"),
                ),
            ),
            "proxy": DictElement(
                parameter_form=Proxy(
                    title=Title("HTTP Proxy"),
                    help_text=Help(
                        "The HTTP proxy that will be used for the connection. If not set, "
                        "the environment settings will be used."
                    ),
                ),
            ),
            "timeout": DictElement(
                parameter_form=TimeSpan(
                    title=Title("Connection Timeout"),
                    help_text=Help(
                        "Define a custom timeout in seconds for the connection.<br>The default "
                        "timeout is 10s."
                    ),
                    displayed_magnitudes=[TimeMagnitude.SECOND],
                    custom_validate=[
                        NumberInRange(
                            min_value=3,
                            max_value=600,
                            error_msg=Message("The timeout must be between 3s and 600s."),
                        ),
                    ],
                    prefill=InputHint(value=10.0),
                ),
            ),
        },
    )


rule_spec_atlassian_statuspage = SpecialAgent(
    name="atlassian_statuspage",
    title=Title("Atlassian Statuspage"),
    parameter_form=_parameter_form_special_agent_atlassian_statuspage,
    topic=Topic.CLOUD,
)
