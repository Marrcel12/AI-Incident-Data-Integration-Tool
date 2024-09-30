from google_sheets.DataLoader import GoogleSheetLoader
from google_sheets.constants import URL
from MISP.handler import create_event_with_object

from MISP_mapping.serialization import map_row_to_misp_object

if __name__ == "__main__":
    gsl = GoogleSheetLoader(url=URL)
    df = gsl.get_data()
    for misp_object in [map_row_to_misp_object(row) for _, row in df.iterrows()]:
        create_event_with_object(misp_object)
