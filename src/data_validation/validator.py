import pandas as pd

class DataValidator:
    def __init__(self, df):
        self.df = df

    def check_missing_values(self):
        return self.df.isnull().sum()

    def check_duplicates(self):
        return self.df[self.df.duplicated()]

    def validate_schema(self, required_columns):
        missing = [c for c in required_columns if c not in self.df.columns]
        return missing

    def run_all_checks(self, required_columns):
        return {
            "missing_values": self.check_missing_values(),
            "duplicates": self.check_duplicates(),
            "missing_columns": self.validate_schema(required_columns)
        }
