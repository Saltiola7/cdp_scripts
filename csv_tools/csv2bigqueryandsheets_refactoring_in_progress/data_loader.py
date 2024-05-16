# data_loader.py
import pandas as pd

class DataLoader:
    def load_csv(self, file_stream):
        df = pd.read_csv(file_stream)
        return df