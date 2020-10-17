import json
from datetime import datetime
from typing import List

import matplotlib.pyplot as plt
import mpld3
import requests


def get_date() -> str:
    """Returns a date string."""
    now = datetime.now()
    return now.strftime("%Y-%m-%d")


def get_response(base: str, currencies: List[str], start: str, end: str = get_date()) -> requests.Response:
    """Requests and returns data about the currencies between two dates."""
    currencies_str = ",".join(currencies)
    base_url = "https://api.exchangeratesapi.io/history"
    url = (base_url + "?start_at=" + start + "&end_at=" + end
           + "&symbols=" + currencies_str + "&base=" + base)
    return requests.get(url)


def sort_data(data: dict):
    """"""
    dates = list(data.keys())
    data_list = []
    # https: // www.geeksforgeeks.org / python - sort - list - of - dates - given -as-strings /
    dates.sort(key=lambda date: datetime.strptime(date, "%Y-%m-%d"))

    for date in dates:
        info = data[date]
        for currency, val in info.items():
            data_list.append({date: {currency: val}})

    return data_list


def reformat_data(data: dict, currencies: list):
    """"""
    data = sort_data(data)
    reformatted_data = {c: {"x": [], "y": []} for c in currencies}
    for item in data:
        for date, info in item.items():
            for currency, val in info.items():
                reformatted_data[currency]["x"].append(date)
                reformatted_data[currency]["y"].append(1 / val)  # reverse the ratio

    return reformatted_data


def get_data(base, currencies, start_date):
    """returns the data about currencies."""
    json_response = get_response(base, currencies, start_date).text
    data = json.loads(json_response)["rates"]
    return reformat_data(data, currencies)


def get_color():
    colors = ['#155e63', '#76b39d']
    for color in colors:
        yield color


def create_plot(base: str, currencies: List[str], start_date: str) -> str:
    """Creates a plot and returns it as a html string."""
    data = get_data(base, currencies, start_date)
    fig, ax = plt.subplots()
    colors = get_color()

    for currency, info in data.items():
        # converts the string to a date object
        x = [datetime.strptime(d, "%Y-%m-%d").date() for d in info["x"]]
        y = info["y"]
        ax.plot(x, y, label=currency, color=next(colors))

    plt.subplots_adjust(right=.8)
    plt.ylabel(base)
    plt.xlabel('Time')
    return mpld3.fig_to_html(fig)


if __name__ == "__main__":
    plot_code = create_plot("EUR", ["USD", "ILS"], "2020-10-1")
    print(plot_code)
