from flask import Flask, render_template, request, session, redirect, url_for, abort

app = Flask('app')

@app.route("/")
def index():
    return render_template("templates/index.html")


if __name__ == '__main__':
    app.run(debug=True)