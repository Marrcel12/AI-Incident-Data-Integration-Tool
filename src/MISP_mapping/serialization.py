from MISP_mapping.model.model import get_topic_for_row


def map_row_to_misp_object(row):
    row_text = " ".join(
        str(value) for value in row.values if value not in [None, "", " ", "nan", "Nan"]
    )
    misp_object = {
        "external_analysis_id": row[("AIAAIC ID#", "-")],
        "external_analysis_trigger": row[("Media trigger(s)", "-")],
        "external_analysis_link": row[("Description/links", "-")],
        "threat_actor_name": row[("Headline", "-")],
        "threat_actor_purpose": row[("Purpose(s)", "-")],
        "threat_actor_risks": row[("Issue(s)", "-")],
        "threat_actor_transparency": row[("Transparency", "-")],
        "event_occurred": row[("Occurred", "-")],
        "organization_countries": row[("Country(ies)", "-")],
        "organization_sectors": row[("Sector(s)", "-")],
        "organization_operators": row[("Deployer(s)", "-")],
        "organization_developers": row[("Developer(s)", "-")],
        "vulnerability_system_names": row[("System name(s)", "-")],
        "vulnerability_technologies": row[("Technology(ies)", "-")],
        "attribution_external_harm_individual": row[("External harms", "Individual")],
        "attribution_external_harm_societal": row[("External harms", "Societal")],
        "attribution_external_harm_environmental": row[
            ("External harms", "Environmental")
        ],
        "attribution_internal_harm_strategic_reputational": row[
            ("Internal harms", "Strategic/reputational")
        ],
        "attribution_internal_harm_operational": row[("Internal harms", "Operational")],
        "attribution_internal_harm_financial": row[("Internal harms", "Financial")],
        "attribution_internal_harm_legal_regulatory": row[
            ("Internal harms", "Legal/regulatory")
        ],
        "associated_topic": get_topic_for_row(row_text),
    }
    return misp_object
