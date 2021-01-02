from flask import Flask, render_template, redirect, url_for, request, session
import psycopg2

"""
con = psycopg2.connect(host="localhost", port="9999", database="tohumdb", user="super", password="whqrnr&6mxAj7")
"""


app = Flask(__name__)
app.secret_key = "boraadamdir"

@app.route("/",methods=["GET","POST"])
def index():
    if "admin" in session:
        return redirect(url_for("admin"))
    elif "user" in session:
        return redirect(url_for("user"))
    else:
        return redirect(url_for("login"))

@app.route("/register",methods=["GET","POST"])
def register():
    pass

@app.route("/login",methods=["GET","POST"])
def login():
    pass

@app.route("/logout")
def logout():
    session.pop("admin",None)
    session.pop("user",None)
    session.pop("id",None)
    return redirect(url_for("login"))

@app.route("/admin",methods=["POST","GET"])
def admin():
    pass

@app.route("/user", methods=["POST","GET"])
def user():
    pass




if __name__ == '__main__':
    app.run(debug=True)