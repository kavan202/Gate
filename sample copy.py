from test import mark
from flask import Flask, render_template, request
app = Flask(__name__)
@app.route("/", methods=["GET", "POST"])
def home():
    marks = None

    if request.method == "POST":
        url = request.form["url"]
        marks = mark(url)

    return render_template("index.html", marks=marks)

if __name__ == "__main__":
    app.run(debug=True)