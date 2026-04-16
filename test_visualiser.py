from visualiser import app


def test_page_title_is_rendered(dash_duo):
    dash_duo.start_server(app)
    heading = dash_duo.wait_for_element("h1", timeout=10)
    assert heading.text == "Pink Morsel Sales Visualiser"


def test_sales_chart_is_rendered(dash_duo):
    dash_duo.start_server(app)
    chart = dash_duo.wait_for_element("#sales-line-chart", timeout=10)
    assert chart is not None


def test_region_selector_is_rendered(dash_duo):
    dash_duo.start_server(app)
    selector = dash_duo.wait_for_element("#region-filter", timeout=10)
    assert selector is not None
