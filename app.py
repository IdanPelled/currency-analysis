from flask import Flask, render_template, request

from visual import visuals

app = Flask(__name__)


@app.route('/')
def home_page():
    """Home page."""
    return render_template("index.html")


@app.route('/search', methods=['POST', "GET"])
def search_page():
    """Search result page."""
    if request.method == 'POST':
        form = request.form
        base = form.get("base-currency")
        currencies = form.getlist("secondary-currency")
        time = form.get("time-frame")

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
            return render_template('index.html')
        elif not plot:
            # if there was an error message from the API
            # or the page was not found
            return "<h1>API Error</h1><p>We are having some problems, try again soon."
    else:
        # if the user tries to go to the search page with a GET request.
        return '<h1>Error</h1><p>Please fill the form to get to the "search page".'


@app.route('/disclaimer')
def disclaimer():
    """Disclaimer page."""
    return render_template("disclaimer.html")


if __name__ == "__main__":
    app.run(debug=True)
