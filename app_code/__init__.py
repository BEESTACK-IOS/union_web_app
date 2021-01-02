from flask import Flask, render_template, redirect, url_for, request, session
import psycopg2

"""
con = psycopg2.connect(host="localhost", port="9999", database="tohumdb", user="super", password="whqrnr&6mxAj7")
"""


app = Flask(__name__)
app.secret_key = "boraadamdir"




if __name__ == '__main__':
    app.run(debug=True)