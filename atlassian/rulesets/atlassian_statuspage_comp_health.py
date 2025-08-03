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
# CHECKMK RULESET: Atlassian Statuspage Components Health (check plug-in)
#
# This file defines the check plug-in parameters for the "Atlassian Statuspage Components Health"
# check. The check is part of the Microsoft Entra special agent (atlassian_statuspage).
####################################################################################################


from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import DefaultValue, DictElement, Dictionary, ServiceState
from cmk.rulesets.v1.rule_specs import CheckParameters, HostCondition, Topic


def _parameter_form_atlassian_statuspage_comp_health() -> Dictionary:
    return Dictionary(
        title=Title("Check parameters"),
        help_text=Help(
            "Check parameters for the Atlassian Statuspage components health. "
            "To use this service, you need to set up the <b>Atlassian Statuspage</b> special "
            "agent."
        ),
        elements={
            "operational": DictElement(
                parameter_form=ServiceState(
                    title=Title("Operational"),
                    help_text=Help(
                        "Set the severity level of the state <i>operational</i>. "
                        "The default severity level is ok."
                    ),
                    prefill=DefaultValue(0),
                ),
            ),
            "degraded_performance": DictElement(
                parameter_form=ServiceState(
                    title=Title("Degraded performance"),
                    help_text=Help(
                        "Set the severity level of the state <i>Degraded performance</i>. "
                        "The default severity level is warning."
                    ),
                    prefill=DefaultValue(1),
                ),
            ),
            "partial_outage": DictElement(
                parameter_form=ServiceState(
                    title=Title("Partial outage"),
                    help_text=Help(
                        "Set the severity level of the state <i>Partial outage</i>. "
                        "The default severity level is critical."
                    ),
                    prefill=DefaultValue(2),
                ),
            ),
            "major_outage": DictElement(
                parameter_form=ServiceState(
                    title=Title("Major outage"),
                    help_text=Help(
                        "Set the severity level of the state <i>Major outage</i>. "
                        "The default severity level is critical."
                    ),
                    prefill=DefaultValue(2),
                ),
            ),
        },
    )


rule_spec_atlassian_statuspage_comp_health = CheckParameters(
    name="atlassian_statuspage_comp_health",
    title=Title("Atlassian Statuspage Components Health"),
    parameter_form=_parameter_form_atlassian_statuspage_comp_health,
    topic=Topic.CLOUD,
    condition=HostCondition(),
)
