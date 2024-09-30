import json
import math
from pymisp import PyMISP, MISPEvent, MISPObject, MISPAttribute
import datetime


class MISPHelper:
    def __init__(self, url, key, verifycert=False):
        self.misp = PyMISP(url, key, verifycert)
        with open(
            "C:\\Users\\marce\\Documents\\repo\\final_project\\src\\MISP\\definition.json",
            "r",
        ) as j:
            self.template = json.loads(j.read())

    def create_event(self, info, distribution=0, threat_level_id=2, analysis=1):
        event = MISPEvent()
        event.info = info
        event.distribution = distribution
        event.threat_level_id = threat_level_id
        event.analysis = analysis
        event.date = datetime.date.today().strftime("%Y-%m-%d")
        return event

    def add_mapped_object_to_event(self, event, mapped_object):
        ai_incident_object = MISPObject(
            name=f'ai-incident{mapped_object["external_analysis_id"]}',
            misp_objects_template_custom=self.template,
            strict=True,
        )
        for key, attr in self.template["attributes"].items():
            value = mapped_object.get(key)

            if value is not None:

                if not isinstance(value, str) and math.isnan(value):
                    value = ""
                ai_incident_object.add_attribute(
                    key, value=value, comment=attr["description"]
                )
        event = self.misp.add_event(event, pythonify=True)
        event.add_object(ai_incident_object)
        return self.misp.update_event(event, pythonify=True)
