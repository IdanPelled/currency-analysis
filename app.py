from flask import Flask, render_template, request, redirect, url_for

from plot import create_plot

app = Flask(__name__)


def is_valid(args):
    if args:
        return True


@app.route('/')
def home_page():
    return render_template("index.html")


@app.route('/search')
def search_page():
    args = request.args
    if is_valid(args):
        base = args.get("base-currency")
        currencies = args.getlist("secondary-currency")
        time = args.get("time-frame")
        plot = create_plot(base, ["USD", "ILS"], time)
        return render_template(
            "search.html",
            base=base,
            currencies=currencies,
            time=time,
            plot=plot
        )
    else:
        return redirect(url_for('home_page'))


@app.errorhandler(404)
def page_not_found():
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(debug=True)
