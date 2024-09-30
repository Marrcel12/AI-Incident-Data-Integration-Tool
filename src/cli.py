import json
import click
from MISP.handler import create_event_with_object
from google_sheets.DataLoader import GoogleSheetLoader
from google_sheets.constants import URL
from MISP_mapping.serialization import map_row_to_misp_object
import pandas as pd

CSV_NAME = "../output_files/data_from_AIAAIC"
MISP_NAME = "../output_files/misp_objects_from_AIAAIC"


@click.group(chain=True)
def cli():
    pass


@cli.command()
@click.option(
    "--save-path-aiaaic",
    type=click.Path(),
    default=f"{CSV_NAME}.csv",
    help="Path to save the data frame.",
)
def get_data_from_sheet(save_path_aiaaic):
    gsl = GoogleSheetLoader(url=URL)
    df = gsl.get_data()
    df.to_csv(save_path_aiaaic, index=False)
    click.echo(f"DataFrame saved to {save_path_aiaaic}")


@cli.command()
@click.option(
    "--load-path",
    type=click.Path(),
    default=f"{CSV_NAME}.csv",
    help="Path from where to load the data frame.",
)
@click.option(
    "--save-path-misp-full",
    type=click.Path(),
    default=f"{MISP_NAME}.json",
    help="Path to save the data frame.",
)
@click.option(
    "--save-path-misp-first",
    type=click.Path(),
    default=f"{MISP_NAME}_10_first.json",
    help="Path to save the dataframe.",
)
def map_to_misp(load_path, save_path_misp_full, save_path_misp_first):
    misp_objects = []
    df = pd.read_csv(load_path, header=[0, 1])
    click.echo(f"Loaded DataFrame:\n{df}")
    for _, row in df.iterrows():
        misp_object = map_row_to_misp_object(row)
        misp_objects.append(misp_object)

    with open(save_path_misp_first, "w+", encoding="utf-8") as f:
        f.write(json.dumps(misp_objects[:10]))
    click.echo(f"10 first JSON MiSP objects saved to {save_path_misp_first}")

    with open(save_path_misp_full, "w+", encoding="utf-8") as f:
        f.write(json.dumps(misp_objects))
    click.echo(f"Full JSON MiSP objects saved to {save_path_misp_full}")


@cli.command()
def direct_process():
    gsl = GoogleSheetLoader(url=URL)
    df = gsl.get_data()
    for misp_object in [map_row_to_misp_object(row) for _, row in df.iterrows()]:
        create_event_with_object(misp_object)


if __name__ == "__main__":
    cli()
