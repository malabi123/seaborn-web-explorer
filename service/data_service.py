import seaborn as sns
import pandas as pd
import numpy as np


class DataService:
    _df = sns.load_dataset('titanic')
    _df['alive'] = _df['alive'].map(
        lambda x: x == 'yes'if pd.notna(x) else np.nan)

    @staticmethod
    def get_df():
        return DataService._df.copy()

    @staticmethod
    def get_df_html():
        return DataService._df.to_html()

    @staticmethod
    def get_df_columns():
        return DataService._df.columns

    @staticmethod
    def get_df_number_columns():
        return DataService._df.select_dtypes(include='number').columns
