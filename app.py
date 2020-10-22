from flask import Flask, render_template, request

from visual import visuals

app = Flask(__name__)


@app.route('/')
def home_page():
    """Home page."""
    return render_template("index.html")


@app.route('/search')
def search_page():
    """Search result page."""
    args = request.args
    base = args.get("base-currency")
    currencies = args.getlist("secondary-currency")
    time = args.get("time-frame")

    plot = visuals(base, currencies, time)
    if isinstance(plot, str):
        return render_template(
            "search.html",
            base=base,
            currencies=currencies,
            time=time,
            plot=plot,
        )
    elif plot is None:
        # if the plot parms are un-valid plot
        print("input error")
        return render_template('index.html')
    elif not plot:
        # if there was an error message from the API
        print("API error")
    return render_template('404.html')


@app.errorhandler(404)
def page_not_found(e):
    """404 page_not_found error page."""
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(debug=True)
