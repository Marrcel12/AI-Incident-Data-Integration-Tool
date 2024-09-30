from MISP.helper import MISPHelper
from MISP.constants import MISP_URL, MISP_KEY, EVENT_INFO

helper = MISPHelper(MISP_URL, MISP_KEY, verifycert=False)


def create_event_with_object(mapped_object, event_info=EVENT_INFO):
    event = helper.create_event(
        f"{mapped_object['threat_actor_name']} \n|{event_info} with id:{mapped_object['external_analysis_id']}"
    )
    return helper.add_mapped_object_to_event(event, mapped_object)
