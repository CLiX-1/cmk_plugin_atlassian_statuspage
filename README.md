# Checkmk Plugin: Atlassian Statuspage Special Agent 

The **Atlassian Statuspage** Special Agent is an extension for the monitoring software **Checkmk**.  
It can be integrated into Checkmk 2.3 or newer.

You can download the extension package as an `.mkp` file from the [releases](../../releases) in this repository and upload it directly to your Checkmk site.  
See the Checkmk [documentation](https://docs.checkmk.com/latest/en/mkps.html) for details.

## Plugin Information

The Plugin provides monitoring for the component status health of Atlassian statuspages.

See [Check Details](#check-details) for more information.

## Check Details

### Atlassian Statuspage Components Health

#### Description

This check monitors the health state of statuspage components.

#### Checkmk Service Example

![grafik](https://github.com/user-attachments/assets/deb43589-2381-4e53-be2b-96b3ce34397a)

#### Checkmk Parameters

You can configure the severity level for each component health state:
1. **Operational**: Set the severity level of the state Operational. The default severity level is ok.
2. **Degraded Performance**: Set the severity level of the state Degraded Performanc. The default severity level is warning.
3. **Partial Outage**: Set the severity level of the state Partial Outage. The default severity level is critical.
4. **Major Outage**: Set the severity level of the state Major Outage. The default severity level is critical.

## Steps to Get It Working

### Checkmk Special Agent Configuration

1. Log in to your Checkmk site

#### Add Checkmk Host

1. Add a new host in **Setup** > **Hosts**
2. Configure your custom settings and set
    -   **IP address family**: No IP
    -   **Checkmk agent / API integrations**: API integrations if configured, else Checkmk agent
3. Save

#### Add Special Agent Rule

1. Navigate to the Special Agent rule **Setup** > **Atlassian Statuspage** (use the search bar)
2. Add a new rule and configure the required settings
    -   **Statuspage URL**
    -   Optionally configure a filter to include or exclude specific components
    -   Add the newly created host in **Explicit hosts**
3. Save and go to your new host and discover your new services
4. Activate the changes
