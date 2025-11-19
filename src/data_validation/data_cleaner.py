import pandas as pd

class DataCleaner:
    def __init__(self, df):
        self.df = df

    def remove_duplicates(self):
        self.df = self.df.drop_duplicates()
        return self.df

    def strip_text_fields(self):
        for col in self.df.select_dtypes(include=['object']):
            self.df[col] = self.df[col].str.strip()
        return self.df

    def fill_missing(self, fill_dict):
        self.df = self.df.fillna(fill_dict)
        return self.df

    def clean_all(self, fill_dict=None):
        self.remove_duplicates()
        self.strip_text_fields()
        if fill_dict:
            self.fill_missing(fill_dict)
        return self.df
