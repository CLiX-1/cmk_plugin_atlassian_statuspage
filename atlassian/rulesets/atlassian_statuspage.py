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
# CHECKMK RULESET: Atlassian Statuspage (special agent)
#
# This file provides the parameter definitions for integrating Atlassian Statuspage monitoring into
# Checkmk.
# Atlassian Statuspage is a Checkmk special agent (atlassian_statuspage).
####################################################################################################

from cmk.rulesets.v1 import Help, Message, Title
from cmk.rulesets.v1.form_specs import (
    CascadingSingleChoice,
    CascadingSingleChoiceElement,
    DefaultValue,
    DictElement,
    Dictionary,
    FieldSize,
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
            "This special agent retrieves data from an Atlassian statuspages.<br>To monitor these "
            "resources, apply this rule to a <b>single host</b>.<br><b>Tip:</b> You can adjust the "
            "query interval using the rule <b>Normal check interval for service checks</b> to "
            "limit the number of API requests."
        ),
        elements={
            "url": DictElement(
                parameter_form=String(
                    title=Title("Statuspage URL"),
                    help_text=Help(
                        "The base URL of the Atlassian statuspage you want to monitor.<br>"
                        "Examples:<br><ul>"
                        "<li><tt>https://confluence.status.atlassian.com</tt></li>"
                        "<li><tt>https://metastatuspage.com</tt></li></ul>"
                    ),
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
                            error_msg=Message("Statuspage URL cannot be empty."),
                        ),
                    ],
                ),
                required=True,
            ),
            "filter": DictElement(
                parameter_form=CascadingSingleChoice(
                    title=Title("Filter components"),
                    help_text=Help(
                        "Filter which components to monitor by name. You can either:<br><br><ul>"
                        "<li><b>Include</b>: Only monitor the specified components<br></li>"
                        "<li><b>Exclude</b>: Monitor all components except the specified ones"
                        "</li></ul>Use the exact names of the components. For example, use the "
                        "name from the services that have already been added.<br>If no filter "
                        "is set, all components will be monitored."
                    ),
                    elements=[
                        CascadingSingleChoiceElement(
                            name="filter_include",
                            title=Title("Include"),
                            parameter_form=List[str](
                                element_template=String(
                                    custom_validate=[
                                        LengthInRange(
                                            min_value=1,
                                            error_msg=Message("Component name cannot be empty."),
                                        ),
                                    ],
                                ),
                                custom_validate=[
                                    LengthInRange(
                                        min_value=1,
                                        error_msg=Message(
                                            "At least one component name must be specified."
                                        ),
                                    ),
                                ],
                            ),
                        ),
                        CascadingSingleChoiceElement(
                            name="filter_exclude",
                            title=Title("Exclude"),
                            parameter_form=List[str](
                                element_template=String(
                                    custom_validate=[
                                        LengthInRange(
                                            min_value=1,
                                            error_msg=Message("Component name cannot be empty."),
                                        ),
                                    ],
                                ),
                                custom_validate=[
                                    LengthInRange(
                                        min_value=1,
                                        error_msg=Message(
                                            "At least one component name must be specified."
                                        ),
                                    ),
                                ],
                            ),
                        ),
                    ],
                    prefill=DefaultValue("filter_include"),
                ),
            ),
            "proxy": DictElement(
                parameter_form=Proxy(
                    title=Title("HTTP proxy"),
                    help_text=Help(
                        "Configure HTTP proxy settings for the API connections.<br><br>"
                        "If not configured, the system environment proxy settings will be used."
                    ),
                ),
            ),
            "timeout": DictElement(
                parameter_form=TimeSpan(
                    title=Title("API request timeout"),
                    help_text=Help(
                        "Specify a custom timeout (in seconds) for the API request.<br>"
                        "<br>If not specified, the default timeout is <b>10 seconds</b>."
                    ),
                    displayed_magnitudes=[TimeMagnitude.SECOND],
                    custom_validate=[
                        NumberInRange(
                            min_value=3,
                            max_value=600,
                            error_msg=Message(
                                "The <b>API request timeout</b> must be between 3s and 600s."
                            ),
                        ),
                    ],
                    prefill=DefaultValue(10.0),
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
