import time
import pandas as pd
import re
import numpy as np
from google_sheets.constants import EMPTY


class GoogleSheetLoader:
    def __init__(self, url):
        self.url = self._prepare_url(url)
        self.data_dict = {}

    @classmethod
    def _prepare_url(self, url):
        pattern = r"https://docs\.google\.com/spreadsheets/d/([a-zA-Z0-9-_]+)(/edit#gid=(\d+)|/edit.*)?"
        replacement = (
            lambda m: f"https://docs.google.com/spreadsheets/d/{m.group(1)}/export?"
            + (f"gid={m.group(3)}&" if m.group(3) else "")
            + "format=csv"
        )
        return re.sub(pattern, replacement, url)

    @classmethod
    def load_data_to_dict(self, df):
        if not df.empty and len(df.columns) >= 2:
            return df.set_index(df.columns[0]).T.to_dict("list")

    @classmethod
    def create_good_indexes(self, df):
        for i, columns_old in enumerate(df.columns.levels):
            columns_new = np.where(
                columns_old.str.contains("Unnamed"), EMPTY, columns_old
            )
            df.rename(
                columns=dict(zip(columns_old, columns_new)), level=i, inplace=True
            )
        return df

    @classmethod
    def fill_indexes(self, df):
        new_cols = []
        for i, column_names in enumerate(df.columns):
            if column_names[0] == EMPTY and i != 0:
                new_cols.append(
                    (
                        new_cols[i - 1][0],
                        column_names[1],
                    )
                )
            else:
                new_cols.append(column_names)
        df.columns = pd.MultiIndex.from_tuples(new_cols)
        return df

    @classmethod
    def process_columns(self, df):
        df = self.create_good_indexes(df)
        self.fill_indexes(df)
        return df

    def get_data(self, get_dict=False, nrows=None, pf=False):
        if nrows:
            df = pd.read_csv(self.url, skiprows=1, header=[0, 1], nrows=nrows)
            if pf:
                return time.time()
        else:
            df = pd.read_csv(filepath_or_buffer=self.url, skiprows=1, header=[0, 1])
        df = self.process_columns(df)
        if not self.data_dict and get_dict:
            return self.load_data_to_dict(df)
        return df
