from flask import Flask, render_template, redirect, url_for, request, session, flash
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
                if password == truePassword.__str__():

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
@app.route("/register", methods=["GET", "POST"])
def register():
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
            print(name, email, tckn, password, password_again)

            if not password == password_again:
                flash("Sifreler uyusmuyor!")

            else:
                con = psycopg2.connect(host="localhost", port="5432", database="UnionDB", user="postgres",
                                       password="Sarris5599")
                cur = con.cursor()
                cur.execute("select * from unionschema.tckno_roles where tckno='{}'".format(tckn))
                tcnko_roles_control = cur.fetchone()
                if (tcnko_roles_control == None) or (len(tcnko_roles_control) == 0):
                    print("hata")
                    return render_template("register.html")
                else:
                    role = tcnko_roles_control[2]
                    print(role)
                    cur.execute("select * from unionschema.members where member_mail='{}'".format(email))
                    mail_control = cur.fetchall()
                    cur.execute("select * from unionschema.members where member_tc='{}'".format(tckn))
                    tc_control = cur.fetchall()
                    if (len(mail_control) or len(tc_control)) == 0:
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
                        return render_template("login.html")
                    else:
                        print("hata")
                        return render_template("register.html")
            return render_template("register.html")
        return render_template("register.html")


@app.route("/user", methods=["POST", "GET"])
def user():
    pass


if __name__ == '__main__':
    app.run(debug=True)
