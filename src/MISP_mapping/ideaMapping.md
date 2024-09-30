# MISP Object Mapping Guide

This document outlines the mapping of data attributes to MISP (Malware Information Sharing Platform & Threat Sharing) objects. It provides a guide on how to utilize the given Python function `map_row_to_misp_object` to transform raw incident data into structured MISP objects.

### Mapping Details:

1. **AIAAIC ID#** -> **External Analysis ID**: Used to uniquely identify the incident in MISP.

2. **Media trigger(s)** -> **External Analysis Trigger**: Links to media reports or analyses that triggered awareness of the incident.

3. **Description/links** -> **External Analysis Link**: This object stores detailed descriptions of the incident and links to external resources for further information.

4. **Headline** (formerly **Headline/title**) -> **Threat Actor Name**: Captures the essence of the incident, utilizing the name field.

5. **Purpose(s)** -> **Threat Actor Purpose**: Maps to detailing the nature and objectives of the actors behind the incident.

6. **Issue(s)** (formerly **Risks(s)**) -> **Threat Actor Risks**: Attributes related to the risk posed by the incident.

7. **Transparency** -> **Threat Actor Transparency**: Provides context on the threat actor's operations regarding transparency.

8. **Occurred** -> **Event Occurred**: Specifies when the incident actually happened.

9. **Country(ies)**, **Sector(s)**, **Deployer(s)** (formerly **Operator(s)**), **Developer(s)** -> **Organization**: Details about the entities involved are captured under these attributes.

10. **System name(s)**, **Technology(ies)** -> **Vulnerability**: Details specific systems or technologies affected, especially if the incident relates to a vulnerability.

11. **External harms** (Individual, Societal, Environmental) -> **Attribution**: Describes the impact of the incident on different external entities.

12. **Internal harms** (Strategic/reputational, Operational, Financial, Legal/regulatory) -> **Attribution**: Focused on the impact within the affected organization.

### Function Usage:

The `map_row_to_misp_object` function takes a row of data and returns a dictionary of MISP objects based on the mapping defined above. Ensure that each row of data contains all the necessary fields as specified. Missing or `None` values are appropriately handled by the function.

### Additional Information:

- Use the `get_topic_for_row` function (imported from `MISP_mapping.model.model`) to determine the associated topic based on the row content, which helps in categorizing the incident effectively.

For detailed usage of each MISP object and their properties, refer to the MISP documentation.
