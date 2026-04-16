import csv
from decimal import Decimal
from glob import glob
from pathlib import Path


DATA_DIR = Path("data")
INPUT_PATTERN = "daily_sales_data_*.csv"
OUTPUT_FILE = DATA_DIR / "formatted_sales.csv"


def calculate_sales(price: str, quantity: str) -> str:
    unit_price = Decimal(price.replace("$", "").strip())
    units_sold = Decimal(quantity.strip())
    return format(unit_price * units_sold, ".2f")


def transform_sales_data() -> None:
    rows = []

    for file_path in sorted(glob(str(DATA_DIR / INPUT_PATTERN))):
        with open(file_path, newline="") as source_file:
            reader = csv.DictReader(source_file)

            for row in reader:
                if row["product"].strip().lower() != "pink morsel":
                    continue

                rows.append(
                    {
                        "Sales": calculate_sales(row["price"], row["quantity"]),
                        "Date": row["date"].strip(),
                        "Region": row["region"].strip(),
                    }
                )

    with open(OUTPUT_FILE, "w", newline="") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=["Sales", "Date", "Region"])
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    transform_sales_data()
