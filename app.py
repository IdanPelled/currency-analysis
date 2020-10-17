from flask import Flask, render_template, request

app = Flask(__name__)


def is_valid(args):
    if args:
        return True


@app.route('/')
def home_page():
    if is_valid(request.args):
        print(request.args["secondary-currency"])
        print('!')
        return render_template(
            "search.html",
            base=request.args.get("base-currency"),
            currencies=request.form.getlist("secondary-currency"),
            time=request.args["time-frame"]
        )
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)