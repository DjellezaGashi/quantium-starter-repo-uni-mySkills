import pandas as pd
from dash import Dash, dcc, html
import plotly.express as px


DATA_FILE = "./data/formatted_sales.csv"
PRICE_CHANGE_DATE = "2021-01-15"


sales_frame = pd.read_csv(DATA_FILE)
sales_frame["Date"] = pd.to_datetime(sales_frame["Date"])

daily_sales = (
    sales_frame.groupby("Date", as_index=False)["Sales"]
    .sum()
    .sort_values("Date")
)

sales_figure = px.line(
    daily_sales,
    x="Date",
    y="Sales",
    title="Pink Morsel Sales Visualiser",
    labels={"Date": "Date", "Sales": "Sales"},
)

sales_figure.add_vline(
    x=PRICE_CHANGE_DATE,
    line_dash="dash",
    line_color="red",
    annotation_text="Price increase",
    annotation_position="top left",
)

app = Dash(__name__)

app.layout = html.Div(
    [
        html.H1("Pink Morsel Sales Visualiser"),
        dcc.Graph(id="sales-line-chart", figure=sales_figure),
    ]
)


if __name__ == "__main__":
    app.run()
