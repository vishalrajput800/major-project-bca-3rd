from data_loader import DataLoader

def main():
    print("=" * 60)
    print("AI Powered Stock Market Analytics Dashboard")
    print("=" * 60)

    loader = DataLoader()
    loader.download_stock_data()

    print("\nAll Stock Data Downloaded Successfully")


if __name__ == "__main__":
    main()