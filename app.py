from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # You can later add authentication logic here
        return f"Welcome, {username}!"
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("registration.html")

if __name__ == "__main__":
    app.run(debug=True)
