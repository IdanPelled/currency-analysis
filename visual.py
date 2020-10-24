import datetime
import json
from typing import List, Union, Dict

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import mpld3
import requests

CURRENCIES = ["USD", "EUR", "JPY", "GBP", "AUD", "CAD", "CHF", "ILS"]


def get_date(date: datetime.datetime) -> str:
    """Returns a date as string."""
    return date.strftime("%Y-%m-%d")


def get_color():
    """Yields a custom color."""
    colors = ['#e60000', '#000000', '#ffa31a']
    for color in colors:
        yield color


def get_response(base: str, currencies: List[str], start: str) -> requests.Response:
    """Requests and returns data about the currencies between two dates."""
    currencies_str = ",".join(currencies)
    base_url = "https://api.exchangeratesapi.io/history"
    url = f"{base_url}?start_at={start}&end_at={get_date(datetime.datetime.now())}&symbols={currencies_str}&base={base}"
    response = requests.get(url)
    return response


def sort_data(data: dict) -> List[Dict[str, Dict[str, int]]]:
    """Sorts the data by date."""
    dates = list(data.keys())
    data_list = []
    # https://www.geeksforgeeks.org/python-sort-list-of-dates-given-as-strings
    dates.sort(key=lambda date: datetime.datetime.strptime(date, "%Y-%m-%d"))

    for date in dates:
        info = data[date]
        for currency, val in info.items():
            data_list.append({date: {currency: val}})

    return data_list


def reformat_data(data: dict, currencies: list) -> Dict[str, Dict[str, List[str]]]:
    """Reformat the data to a more usable format."""
    data = sort_data(data)
    reformatted_data = {c: {"x": [], "y": []} for c in currencies}
    for item in data:
        for date, info in item.items():
            for currency, val in info.items():
                reformatted_data[currency]["x"].append(date)
                reformatted_data[currency]["y"].append(1 / val)  # reverse the ratio

    return reformatted_data


def get_js(code: str) -> str:
    """Returns the js code between the <script> tag."""
    return code.split("<script>")[-1].split("</script>")[0]


def normalize_date(start_date: str) -> Union[str, None]:
    """Checks if the selected time frame is valid
       and if so, returns the starting date."""
    if start_date == "Last week":
        start_date = 7
    elif start_date == "Last month":
        start_date = 31
    elif start_date == "Last 3 month":
        start_date = 91
    elif start_date == "Last 6 month":
        start_date = 182
    try:
        back = datetime.timedelta(days=int(start_date))
    except (TypeError, ValueError):
        return None
    else:
        return get_date(datetime.datetime.now() - back)


def are_currencies_valid(currencies: List[str], base: str) -> bool:
    """Checks if the currencies are valid."""
    for c in currencies + [base]:
        if c not in CURRENCIES:
            return False
    return True


def check_input(base: str, currencies: List[str], time: Union[None, datetime.datetime]):
    """Checks if the input is valid."""
    if base not in currencies:
        if time is not None:
            return are_currencies_valid(currencies, base)
    return False


def get_data(base: str, currencies: List[str], start_date: str)\
            -> Union[Dict[str, Dict[str, List[str]]], None]:
    """returns the data about currencies."""
    response = get_response(base, currencies, start_date)

    if response.ok:
        data = json.loads(response.text)["rates"]
        return reformat_data(data, currencies)

    else:
        return None


def create_graph(data: dict) -> str:
    """Creates a graph and returns it as a html string."""
    fig, ax = plt.subplots()
    colors = get_color()
    patches = []

    for currency, info in data.items():
        # converts the string to a date object
        x = [datetime.datetime.strptime(d, "%Y-%m-%d").date() for d in info["x"]]
        y = info["y"]
        color = next(colors)
        ax.plot(x, y, label=currency, color=color)
        patch = mpatches.Patch(color=color, label=currency)
        patches.append(patch)

    ax.grid()
    plt.legend(handles=patches, loc='upper left')
    plt.tight_layout(pad=0)

    return get_js(mpld3.fig_to_html(fig, figid="graph-box"))


def visuals(base: str, currencies: List[str], time: str) -> Union[str, bool, None]:
    """If input is valid, returns a graph."""
    time = normalize_date(time)
    if 0 < len(currencies) < 4:
        if check_input(base, currencies, time):
            data = get_data(base, currencies, time)
            if data is not None:
                graph = create_graph(data)
                # if the action was successful
                return graph
            else:
                # if there was an error message from the API
                return False
    # if the plot parms are un-valid plot
    return None
