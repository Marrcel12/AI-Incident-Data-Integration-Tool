from google_sheets.DataLoader import GoogleSheetLoader
from google_sheets.constants import URL
from MISP.handler import create_event_with_object
import time
from MISP_mapping.serialization import map_row_to_misp_object

# TESTING_NUMBER_ROWS =[100,1_000,32_100]
TESTING_NUMBER_ROWS = [4, 100]


def run_for_rows_entire_system(number_of_rows=100):
    start = time.time()
    gsl = GoogleSheetLoader(url=URL)
    df = gsl.get_data(nrows=number_of_rows)
    for misp_object in [map_row_to_misp_object(row) for _, row in df.iterrows()]:
        create_event_with_object(misp_object)
    return time.time() - start


def run_for_rows_data_coll(number_of_rows=100):
    start = time.time()
    gsl = GoogleSheetLoader(url=URL)
    return gsl.get_data(nrows=number_of_rows, pf=True) - start


def run_for_rows_pre_processing(number_of_rows=100):
    gsl = GoogleSheetLoader(url=URL)
    start = time.time()
    _ = gsl.get_data(nrows=number_of_rows)
    return time.time() - start


def run_for_rows_serialization(number_of_rows=100):
    gsl = GoogleSheetLoader(url=URL)
    df = gsl.get_data(nrows=number_of_rows)
    start = time.time()
    [map_row_to_misp_object(row) for _, row in df.iterrows()]
    return time.time() - start


def run_for_misp_integration(number_of_rows=100):
    gsl = GoogleSheetLoader(url=URL)
    df = gsl.get_data(nrows=number_of_rows)
    data = [map_row_to_misp_object(row) for _, row in df.iterrows()]
    start = time.time()
    for misp_object in data:
        create_event_with_object(misp_object)
    return time.time() - start


enter_text = (
    f"Starting running performance testing for: {TESTING_NUMBER_ROWS} number of rows"
)

print(enter_text)
for number_of_rows in TESTING_NUMBER_ROWS:
    res = [
        f"For number of rows {number_of_rows} time of processing AIAAIC Data Collection, equals {run_for_rows_data_coll(number_of_rows=number_of_rows)} sec"
    ]
    res.append(
        f"For number of rows {number_of_rows} time of Data Preprocessing, equals {run_for_rows_pre_processing(number_of_rows=number_of_rows)} sec"
    )
    res.append(
        f"For number of rows {number_of_rows} time of Data Serialization, equals {run_for_rows_serialization(number_of_rows=number_of_rows)} sec"
    )
    res.append(
        f"For number of rows {number_of_rows} time of processing MISP Integration, equals {run_for_misp_integration(number_of_rows=number_of_rows)} sec"
    )
    print("\n".join(res))
    with open("performance_result.txt", "a+") as f:
        f.write("\n" + enter_text)
        f.write("\n".join(res))
        f.readline()
