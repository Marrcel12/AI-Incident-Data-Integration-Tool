
import pytest
from unittest.mock import MagicMock, patch
from MISP_mapping.serialization import map_row_to_misp_object  # Ensure the module path is correct

def mock_df_row():
    mock_row = MagicMock()
    mock_row.__getitem__.side_effect = lambda x: {
        ("AIAAIC ID#", "-"): "12345",
        ("Media trigger(s)", "-"): "Sample Trigger",
        ("Description/links", "-"): "http://example.com",
        ("Headline", "-"): "Sample Headline",
        ("Purpose(s)", "-"): "Sample Purpose",
        ("Issue(s)", "-"): "Sample Issue",
        ("Transparency", "-"): "Sample Transparency",
        ("Occurred", "-"): "Sample Occurred",
        ("Country(ies)", "-"): "Sample Country",
        ("Sector(s)", "-"): "Sample Sector",
        ("Deployer(s)", "-"): "Sample Deployer",
        ("Developer(s)", "-"): "Sample Developer",
        ("System name(s)", "-"): "Sample System",
        ("Technology(ies)", "-"): "Sample Technology",
        ("External harms", "Individual"): "Sample External Harm Individual",
        ("External harms", "Societal"): "Sample External Harm Societal",
        ("External harms", "Environmental"): "Sample External Harm Environmental",
        ("Internal harms", "Strategic/reputational"): "Sample Internal Harm Strategic",
        ("Internal harms", "Operational"): "Sample Internal Harm Operational",
        ("Internal harms", "Financial"): "Sample Internal Harm Financial",
        ("Internal harms", "Legal/regulatory"): "Sample Internal Harm Legal"
    }.get(x, "-")
    mock_row.values = iter([
        "12345", "Sample Trigger", "http://example.com", "Sample Headline",
        "Sample Purpose", "Sample Issue", "Sample Transparency", "Sample Occurred",
        "Sample Country", "Sample Sector", "Sample Deployer", "Sample Developer",
        "Sample System", "Sample Technology", "Sample External Harm Individual",
        "Sample External Harm Societal", "Sample External Harm Environmental",
        "Sample Internal Harm Strategic", "Sample Internal Harm Operational",
        "Sample Internal Harm Financial", "Sample Internal Harm Legal"
    ])
    return mock_row

@pytest.fixture
def row():
    return mock_df_row()

def test_map_row_to_misp_object_with_mock(row):
    expected_topic = 'IT Risk'
    
    with patch('MISP_mapping.serialization.get_topic_for_row', return_value=expected_topic) as mock_get_topic:
        result = map_row_to_misp_object(row)

        assert result["external_analysis_id"] == "12345"
        assert result["external_analysis_trigger"] == "Sample Trigger"
        assert result["external_analysis_link"] == "http://example.com"
        assert result["threat_actor_name"] == "Sample Headline"
        assert result["associated_topic"] == expected_topic

def test_map_row_to_misp_object_with_missing_fields(row):
    row.__getitem__.side_effect = lambda x: {
        ("AIAAIC ID#", "-"): None, 
        ("Media trigger(s)", "-"): " "  
    }.get(x, "-")

    result = map_row_to_misp_object(row)
    
    assert result["external_analysis_id"] == None
    assert result["external_analysis_trigger"] == " "