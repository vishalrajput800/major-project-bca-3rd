import os
import pandas as pd
import yfinance as yf
from config import STOCKS, START_DATE, END_DATE, DATA_FOLDER


class DataLoader:

    def __init__(self):
        os.makedirs(DATA_FOLDER, exist_ok=True)

    def download_stock_data(self):

        for company_name, ticker in STOCKS.items():

            try:
                print(f"\nDownloading {company_name} ({ticker})...")

                data = yf.download(
                    ticker,
                    start=START_DATE,
                    end=END_DATE,
                    auto_adjust=True,
                    progress=False
                )

                # MultiIndex fix
                if isinstance(data.columns, pd.MultiIndex):
                    data.columns = data.columns.get_level_values(0)

                data.reset_index(inplace=True)

                file_path = os.path.join(
                    DATA_FOLDER,
                    f"{company_name.lower().replace(' ', '_')}.csv"
                )

                data.to_csv(file_path, index=False)

                print(f"Saved: {file_path}")
                print(f"Rows: {len(data)}")

            except Exception as e:
                print(f"Error downloading {company_name}: {e}")


if __name__ == "__main__":
    loader = DataLoader()
    loader.download_stock_data()