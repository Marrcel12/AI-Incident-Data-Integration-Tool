import pytest
from MISP.helper import MISPHelper  
from pymisp import MISPEvent
import datetime

@pytest.fixture
def misp_helper(mocker):
    mocker.patch('MISP.helper.PyMISP')
    return MISPHelper('http://example.com', 'api_key')

def test_create_event(misp_helper):
    # Test the creation of an event
    event = misp_helper.create_event('Test Event')
    assert event.info == 'Test Event'
    assert event.distribution == 0
    assert event.threat_level_id == 2
    assert event.analysis == 1
    assert event.date == datetime.date.today()

def test_add_mapped_object_to_event(misp_helper, mocker):
    event = MISPEvent()
    mapped_object = {
        "external_analysis_id": "123",
        "threat_actor_name": "Bad Actor"
    }
    misp_helper.template = {
        'attributes': {
            'external_analysis_id': {'description': 'desc'},
            'threat_actor_name': {'description': 'desc'}
        }
    }

    mock_misp_object = mocker.patch('MISP.helper.MISPObject', autospec=True)
    mock_add_event = mocker.patch.object(misp_helper.misp, 'add_event', return_value=event)
    mock_update_event = mocker.patch.object(misp_helper.misp, 'update_event', return_value=event)

    _ = misp_helper.add_mapped_object_to_event(event, mapped_object)

    mock_misp_object.assert_called_once_with(
        name='ai-incident123',
        misp_objects_template_custom=misp_helper.template,
        strict=True
    )

    assert mock_misp_object.return_value.add_attribute.call_count == 2
    mock_misp_object.return_value.add_attribute.assert_any_call('external_analysis_id', value='123', comment='desc')
    mock_misp_object.return_value.add_attribute.assert_any_call('threat_actor_name', value='Bad Actor', comment='desc')

    mock_add_event.assert_called_once_with(event, pythonify=True)
    mock_update_event.assert_called_once_with(event, pythonify=True)

