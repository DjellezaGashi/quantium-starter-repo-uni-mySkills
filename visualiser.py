import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, dcc, html


DATA_FILE = "./data/formatted_sales.csv"
PRICE_CHANGE_DATE = pd.Timestamp("2021-01-15")
REGION_OPTIONS = ["all", "north", "east", "south", "west"]
PALETTE = {
    "page": "#f7efe4",
    "panel": "#fffaf3",
    "accent": "#d96c3d",
    "accent_soft": "#f3c8a2",
    "ink": "#2d1f1a",
    "grid": "#e7d6c4",
}


raw_sales = pd.read_csv(DATA_FILE)
raw_sales["Date"] = pd.to_datetime(raw_sales["Date"])

app = Dash(__name__)


def build_chart(selected_region: str):
    if selected_region == "all":
        filtered_sales = raw_sales.copy()
        chart_title = "Pink Morsel Sales Across All Regions"
    else:
        filtered_sales = raw_sales[raw_sales["Region"] == selected_region]
        chart_title = f"Pink Morsel Sales in the {selected_region.title()} Region"

    plotted_sales = (
        filtered_sales.groupby("Date", as_index=False)["Sales"]
        .sum()
        .sort_values("Date")
    )

    figure = px.line(
        plotted_sales,
        x="Date",
        y="Sales",
        title=chart_title,
        labels={"Date": "Date", "Sales": "Sales"},
        markers=True,
    )

    figure.update_traces(line_color=PALETTE["accent"], marker_size=5)
    figure.update_layout(
        plot_bgcolor=PALETTE["panel"],
        paper_bgcolor=PALETTE["panel"],
        font={"color": PALETTE["ink"]},
        title={"x": 0.5},
        margin={"l": 40, "r": 30, "t": 70, "b": 40},
    )
    figure.update_xaxes(showgrid=False)
    figure.update_yaxes(showgrid=True, gridcolor=PALETTE["grid"])
    figure.add_vline(
        x=PRICE_CHANGE_DATE,
        line_dash="dash",
        line_color=PALETTE["accent"],
    )
    figure.add_annotation(
        x=PRICE_CHANGE_DATE,
        y=1,
        yref="paper",
        text="15 Jan 2021 price increase",
        showarrow=False,
        xanchor="left",
        yanchor="bottom",
        font={"color": PALETTE["accent"]},
    )
    return figure


app.layout = html.Div(
    [
        html.Div(
            [
                html.H1(
                    "Pink Morsel Sales Visualiser",
                    style={
                        "marginBottom": "8px",
                        "fontFamily": "Georgia, serif",
                    },
                ),
                html.P(
                    "Explore Soul Foods sales by region and compare performance before and after the January 15, 2021 price increase.",
                    style={"marginTop": "0", "fontSize": "18px"},
                ),
            ],
            style={
                "backgroundColor": PALETTE["accent_soft"],
                "padding": "24px",
                "borderRadius": "20px",
                "boxShadow": "0 12px 30px rgba(45, 31, 26, 0.12)",
            },
        ),
        html.Div(
            [
                html.Label(
                    "Filter by region",
                    htmlFor="region-filter",
                    style={
                        "display": "block",
                        "marginBottom": "12px",
                        "fontWeight": "bold",
                    },
                ),
                dcc.RadioItems(
                    id="region-filter",
                    options=[
                        {"label": region.title(), "value": region}
                        for region in REGION_OPTIONS
                    ],
                    value="all",
                    inline=True,
                    labelStyle={
                        "marginRight": "18px",
                        "fontSize": "16px",
                    },
                    inputStyle={"marginRight": "6px"},
                ),
            ],
            style={
                "marginTop": "24px",
                "backgroundColor": PALETTE["panel"],
                "padding": "20px 24px",
                "borderRadius": "18px",
                "border": f"1px solid {PALETTE['grid']}",
            },
        ),
        html.Div(
            dcc.Graph(id="sales-line-chart", figure=build_chart("all")),
            style={
                "marginTop": "24px",
                "backgroundColor": PALETTE["panel"],
                "padding": "16px",
                "borderRadius": "18px",
                "border": f"1px solid {PALETTE['grid']}",
                "boxShadow": "0 10px 24px rgba(45, 31, 26, 0.08)",
            },
        ),
    ],
    style={
        "maxWidth": "1100px",
        "margin": "0 auto",
        "padding": "32px 20px 48px",
        "backgroundColor": PALETTE["page"],
        "color": PALETTE["ink"],
        "minHeight": "100vh",
        "fontFamily": "Arial, sans-serif",
    },
)


@app.callback(
    Output("sales-line-chart", "figure"),
    Input("region-filter", "value"),
)
def refresh_chart(selected_region: str):
    return build_chart(selected_region)


if __name__ == "__main__":
    app.run()
