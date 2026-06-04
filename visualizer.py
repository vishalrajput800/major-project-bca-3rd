import pandas as pd
import matplotlib.pyplot as plt


class StockVisualizer:

    def __init__(self, file_path):
        self.df = pd.read_csv(file_path)

        self.df["Date"] = pd.to_datetime(self.df["Date"])

    def plot_closing_price(self):

        plt.figure(figsize=(12, 6))

        plt.plot(
            self.df["Date"],
            self.df["Close"],
            label="Close Price"
        )

        plt.title("Stock Closing Price Trend")

        plt.xlabel("Date")

        plt.ylabel("Price")

        plt.legend()

        plt.grid(True)

        plt.tight_layout()

        plt.savefig(
            "screenshots/closing_price_trend.png"
        )

        plt.show()

    def plot_moving_average(self):

        plt.figure(figsize=(12, 6))

        plt.plot(
            self.df["Date"],
            self.df["Close"],
            label="Close Price"
        )

        plt.plot(
            self.df["Date"],
            self.df["MA20"],
            label="MA20"
        )

        plt.plot(
            self.df["Date"],
            self.df["MA50"],
            label="MA50"
        )

        plt.title(
            "Moving Average Analysis"
        )

        plt.xlabel("Date")

        plt.ylabel("Price")

        plt.legend()

        plt.grid(True)

        plt.tight_layout()

        plt.savefig(
            "screenshots/moving_average.png"
        )

        plt.show()


if __name__ == "__main__":

    visualizer = StockVisualizer(
        "data/reliance.csv"
    )

    visualizer.plot_closing_price()

    visualizer.plot_moving_average()