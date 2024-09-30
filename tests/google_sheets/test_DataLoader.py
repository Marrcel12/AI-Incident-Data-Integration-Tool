import pytest
from unittest.mock import patch
import pandas as pd
from google_sheets.DataLoader import GoogleSheetLoader  # Ensure correct import based on your file structure
from google_sheets.constants import EMPTY

class TestGoogleSheetLoader:
    @staticmethod
    def test_prepare_url_basic():
        url = "https://docs.google.com/spreadsheets/d/1Ab2c3dEFgHiJkLm/edit#gid=123456"
        expected = "https://docs.google.com/spreadsheets/d/1Ab2c3dEFgHiJkLm/export?gid=123456&format=csv"
        assert GoogleSheetLoader._prepare_url(url) == expected

    @staticmethod
    def test_prepare_url_no_gid():
        url = "https://docs.google.com/spreadsheets/d/1Ab2c3dEFgHiJkLm/edit"
        expected = "https://docs.google.com/spreadsheets/d/1Ab2c3dEFgHiJkLm/export?format=csv"
        assert GoogleSheetLoader._prepare_url(url) == expected

    @patch('pandas.read_csv')
    def test_get_data(self, mock_read_csv):
        # Creating a DataFrame with a MultiIndex
        mock_df = pd.DataFrame({
            ('Name', 'Subcol1'): ['Alice', 'Bob'],
            ('Age', 'Subcol2'): [25, 30]
        })
        mock_df.columns = pd.MultiIndex.from_tuples([('Name', 'Subcol1'), ('Age', 'Subcol2')])
        mock_read_csv.return_value = mock_df

        loader = GoogleSheetLoader("https://docs.google.com/spreadsheets/d/1Ab2c3dEFgHiJkLm/export?format=csv")
        result = loader.get_data()
        assert isinstance(result, pd.DataFrame)
        assert result.shape == (2, 2)

    @staticmethod
    def test_load_data_to_dict_non_empty():
        df = pd.DataFrame({
            'Height':[11,22],
            'Name': ['Alice', 'Bob'],
            'Age': [25, 30],
        }).set_index('Name')
        expected = {11: [25], 22: [30]}
        result = GoogleSheetLoader.load_data_to_dict(df=df)
        assert result == expected

    @staticmethod
    def test_create_good_indexes():
        df = pd.DataFrame({
            ('Unnamed: 0_level_0', 'Subcol1'): ['data1', 'data2'],
            ('Value', 'Subcol2'): [10, 20]
        })
        df.columns = pd.MultiIndex.from_tuples([('Unnamed: 0_level_0', 'Subcol1'), ('Value', 'Subcol2')])
        result = GoogleSheetLoader.create_good_indexes(df)
        assert result.columns.get_level_values(0).tolist() == [EMPTY, 'Value']

    @staticmethod
    def test_fill_indexes():
        df = pd.DataFrame({
            ('-', 'Subcol1'): ['data1', 'data2'],
            ('Value', 'Subcol2'): [10, 20]
        })
        df.columns = pd.MultiIndex.from_tuples([('-', 'Subcol1'), ('Value', 'Subcol2')])
        result = GoogleSheetLoader.fill_indexes(df)
        expected_columns = [('-', 'Subcol1'), ('Value', 'Subcol2')]
        assert result.columns.tolist() == expected_columns
