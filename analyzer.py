import pandas as pd
import os


class StockAnalyzer:

    def __init__(self, file_path):
        self.file_path = file_path
        self.df = pd.read_csv(file_path)

        self.df["Date"] = pd.to_datetime(self.df["Date"])

        numeric_cols = ["Close", "High", "Low", "Open", "Volume"]

        for col in numeric_cols:
            self.df[col] = pd.to_numeric(self.df[col], errors="coerce")

        self.df.dropna(inplace=True)

    def basic_info(self):

        print("\n" + "=" * 60)
        print(f"Stock Analysis : {os.path.basename(self.file_path)}")
        print("=" * 60)

        print(f"\nTotal Records : {len(self.df)}")

        print(f"\nDate Range :")
        print(f"Start : {self.df['Date'].min()}")
        print(f"End   : {self.df['Date'].max()}")

        print("\nMissing Values:")
        print(self.df.isnull().sum())

    def calculate_indicators(self):

        self.df["MA20"] = self.df["Close"].rolling(20).mean()

        self.df["MA50"] = self.df["Close"].rolling(50).mean()

        self.df["Daily_Return"] = self.df["Close"].pct_change() * 100

        self.df["Volatility"] = (
            self.df["Daily_Return"]
            .rolling(20)
            .std()
        )

    def summary(self):

        print("\nPrice Summary")

        print(f"Highest Close : {self.df['Close'].max():.2f}")

        print(f"Lowest Close  : {self.df['Close'].min():.2f}")

        print(f"Average Close : {self.df['Close'].mean():.2f}")

    def save(self):

        self.df.to_csv(self.file_path, index=False)

        print("\nIndicators Added Successfully")

        print("File Updated")


if __name__ == "__main__":

    analyzer = StockAnalyzer("data/reliance.csv")

    analyzer.basic_info()

    analyzer.calculate_indicators()

    analyzer.summary()

    analyzer.save()