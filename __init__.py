from flask import Flask, render_template, redirect, url_for, request, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2

"""
con = psycopg2.connect(host="localhost", port="9999", database="buromemursen", user="super", password="facethest0rm")
"""

app = Flask(__name__)
app.secret_key = "boraadamdir"

@app.route("/", methods=["GET", "POST"])
def index():
    if "admin" in session or "super" in session:
        return redirect(url_for("admin"))
    elif "user" in session:
        return redirect(url_for("user"))
    else:
        return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if "admin" in session or "super" in session:
        return redirect(url_for("admin"))
    elif "user" in session:
        return redirect(url_for("user"))
    else:
        if request.method == "POST":
            con = psycopg2.connect(host="localhost", port="9999", database="buromemursen", user="super",
                                   password="facethest0rm")
            cur = con.cursor()

            tckno = request.form["your_tckno"]
            password = request.form["your_pass"]

            cur.execute("select * from unionschema.members where member_tc='{}'".format(tckno))
            data = cur.fetchone()
            id = data[0]
            truePassword = data[3]
            mail = data[2]
            name = data[4]

            cur.execute("select * from unionschema.member_role where member_id = {}".format(id))
            data = cur.fetchone()
            role = data[1]

            if truePassword == None:
                return redirect(url_for("login"))
            else:
                if check_password_hash(truePassword.__str__(), password):
                    if role == 0:
                        session["super"] = "super"
                        session["id"] = id
                        session["mail"] = mail
                        session["name"] = name
                        cur.close()
                        con.close()
                        return redirect(url_for("admin"))
                    elif role == 1:
                        session["admin"] = "admin"
                        session["id"] = id
                        session["mail"] = mail
                        session["name"] = name
                        cur.close()
                        con.close()
                        return redirect(url_for("admin"))
                    elif role == 2:
                        session["user"] = "user"
                        session["id"] = id
                        session["mail"] = mail
                        session["name"] = name
                        cur.close()
                        con.close()
                        return redirect(url_for("user"))
                    else:
                        return redirect(url_for("login"))

        return render_template('login.html')


@app.route("/logout")
def logout():
    session.pop("super", None)
    session.pop("admin", None)
    session.pop("user", None)
    session.pop("id", None)
    return redirect(url_for("login"))


@app.route("/admin", methods=["POST", "GET"])
def admin():
    pass


@app.route("/user", methods=["POST", "GET"])
@app.route("/haberler", methods=["POST", "GET"])
def haberler():
    pass

@app.route("/magazalar", methods=["POST", "GET"])
def magazalar():
    pass

@app.route("/profil", methods=["POST", "GET"])
def profil():
    username  ="as"
    userrole  ="as"
    usermail  ="aas"
    usertckno = "asdasd"

    return render_template("profil.html", usermail=usermail, username=username, userrole=userrole, usertc=usertckno)


@app.route("/register", methods=["GET", "POST"])
def register():
    errorType = -1
    if "admin" in session or "super" in session:
        return redirect(url_for("admin"))

    elif "user" in session:
        return redirect(url_for("user"))

    else:
        if request.method == "POST":
            name = request.form["name"]
            email = request.form["email"]
            tckn = request.form["tckn"]
            password = request.form["pass"]
            password_again = request.form["re_pass"]

            if not password == password_again:
                return render_template("register.html",errorType=errorType)
            else:
                con = psycopg2.connect(host="localhost", port="9999", database="buromemursen", user="super",
                                       password="facethest0rm")
                cur = con.cursor()
                cur.execute("select * from unionschema.tckno_roles where tckno='{}'".format(tckn))
                tcnko_roles_control = cur.fetchone()
                if (tcnko_roles_control == None) or (len(tcnko_roles_control) == 0):
                    errorType = 0
                    return render_template("register.html",errorType=errorType)
                else:
                    role = tcnko_roles_control[2]
                    cur.execute("select * from unionschema.members where member_mail='{}'".format(email))
                    mail_control = cur.fetchall()
                    cur.execute("select * from unionschema.members where member_tc='{}'".format(tckn))
                    tc_control = cur.fetchall()
                    if (len(mail_control) or len(tc_control)) == 0:
                        password = generate_password_hash(password, method='sha256')
                        cur.execute(
                            "INSERT into unionschema.members ( member_tc, member_mail, member_password, member_name) values(%s, %s, %s, %s) RETURNING member_id",
                            (tckn, email, password, name))
                        member_id = cur.fetchone()[0]
                        cur.execute(
                            "INSERT into unionschema.member_role ( member_id, member_role) values(%s, %s)",
                            (member_id, role))
                        con.commit()
                        cur.close()
                        con.close()
                        return render_template("login.html",errorType=errorType)
                    else:
                        errorType = 1
                        cur.close()
                        con.close()
                        return render_template("register.html",errorType=errorType)
        return render_template("register.html",errorType=-1)



if __name__ == '__main__':
    app.run(debug=True)
