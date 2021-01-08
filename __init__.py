from flask import Flask, render_template, redirect, url_for, request, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
import pusher
import smtplib

"""
con = psycopg2.connect(host="localhost", port="9999", database="buromemursen", user="super", password="facethest0rm")
"""

app = Flask(__name__)
app.secret_key = "boraadamdir"

pusher_client = pusher.Pusher(
    app_id="1132585",
    key = "ed89289759f2f434f256",
    secret = "4bd8e6fd627fba65f76d",
    cluster = "eu",
    ssl=True
)

@app.route('/message', methods=['POST'])
def message():
    try:
        username = request.form.get('username')
        userid = request.form.get('userid')
        recievername = request.form.get('recievername')
        recieverid = request.form.get('recieverid')
        message = request.form.get('message')
        channelName = request.form.get('channelName')
        mesDate = request.form.get('date')
        mesTime = request.form.get('time')

        con = psycopg2.connect(host="localhost", port="9999", database="buromemursen", user="super",
                               password="facethest0rm")
        cur = con.cursor()
        cur.execute("INSERT into unionschema.message_log ( channel_name, sender_id, reciever_id, message) values(%s, %s, %s, %s)",
                            (channelName, userid, recieverid, message))
        con.commit()
        cur.close()
        con.close()
        pusher_client.trigger(channelName, 'new-message', {'username': username,'recievername':recievername,'recieverid':recieverid, 'message': message, 'date':mesDate, 'time':mesTime})

        return jsonify({'result': 'success'})
    except:
        return jsonify({'result': 'failure'})

@app.route('/messagehist', methods=['POST','GET'])
def messageHist():
    try:
        channelName = request.form.get('channelName')
        con = psycopg2.connect(host="localhost", port="9999", database="buromemursen", user="super",
                               password="facethest0rm")
        cur = con.cursor()
        cur.execute("select * from unionschema.message_log where channel_name='{}'".format(channelName))
        message_data = cur.fetchall()
        return jsonify({'result': 'success', 'message_data': message_data})
    except:
        return jsonify({'result': 'failure'})


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

@app.route("/talep", methods=["POST", "GET"])
def ticket():

    data = ""

    #pusher_client.trigger('chat-channel', 'new-message', {'message': "message"})

    if "admin" in session or "super" in session or "user" in session:

        con = psycopg2.connect(host="localhost", port="9999", database="buromemursen", user="super",
                               password="facethest0rm")
        cur = con.cursor()

        usermail = session["mail"]
        userid = session["id"]
        username = session["name"]
        if "super" in session:
            userrole = "super"

            sql = "SELECT m.member_id, m.member_name, m.member_mail, mr.member_role FROM unionschema.members as m, unionschema.member_role mr WHERE m.member_id = mr.member_id;"
            cur.execute(sql)
            data = cur.fetchall()

        elif "admin" in session:
            userrole = "yönetici"

            sql = "SELECT m.member_id, m.member_name, m.member_mail, mr.member_role FROM unionschema.members as m, unionschema.member_role mr WHERE m.member_id = mr.member_id;"
            cur.execute(sql)
            data = cur.fetchall()

        elif "user" in session:
            userrole = "üye"

            sql = "SELECT m.member_id, m.member_name, m.member_mail, mr.member_role FROM unionschema.members as m, unionschema.member_role mr WHERE m.member_id = mr.member_id AND ( mr.member_role = 0 OR mr.member_role = 1);"
            cur.execute(sql)
            data = cur.fetchall()

        cur.close()
        con.close()
        return render_template("ticket.html", data=data, userid=userid, username=username)
    else:
        return render_template("login.html")


@app.route("/user", methods=["POST", "GET"])
def user():
    pass
@app.route("/haberler", methods=["POST", "GET"])
def haberler():
    pass

@app.route("/magazalar", methods=["POST", "GET"])
def magazalar():
    pass

@app.route("/sifremi_unuttum", methods=["POST", "GET"])
def sifremi_unuttum():

    if request.method == "POST":
        print(request.form["email"])
        sender = 'from@fromdomain.com'
        receivers = [request.form["email"]]

        message = """From: From Person <from@fromdomain.com>
        To: To Person <to@todomain.com>
        Subject: SMTP e-mail test

        This is a test e-mail message.
        """

        try:
            smtpObj = smtplib.SMTP('localhost')
            smtpObj.sendmail(sender, receivers, message)
            print("Successfully sent email")
        except Exception as e:
            print("Error: unable to send email")

    return render_template("pages-forget.html")

@app.route("/profil", methods=["POST", "GET"])
def profil():
    if "admin" in session or "super" in session or "user" in session:
        con = psycopg2.connect(host="localhost", port="9999", database="buromemursen", user="super",
                               password="facethest0rm")
        cur = con.cursor()
        usermail = session["mail"]
        cur.execute("select member_tc from unionschema.members where member_mail='{}'".format(usermail))
        usertckno = cur.fetchone()[0]
        username = session["name"]
        if "super" in session:
            userrole = "super"
        elif "admin" in session:
            userrole = "yönetici"
        elif "user" in session:
            userrole = "üye"
        if request.method == "POST":
            form_mail = request.form["mail"]
            form_oldPassword = request.form["past_pass"]
            form_newPassword = request.form["pass"]
            cur.execute("select member_password from unionschema.members where member_tc='{}'".format(usertckno))
            hashed_password = cur.fetchone()[0]
            if check_password_hash(hashed_password, form_oldPassword):
                if len(form_mail) > 0:
                    cur.execute("update unionschema.members set member_mail ='{}' where member_tc='{}'".format(form_mail, usertckno))
                    usermail = form_mail
                    session["mail"] = form_mail
                if len(form_newPassword) > 0:
                    new_password = generate_password_hash(form_newPassword, method='sha256')
                    cur.execute("update unionschema.members set member_password ='{}' where member_tc='{}'".format(new_password, usertckno))
        con.commit()
        cur.close()
        con.close()
        return render_template("profil.html", usermail=usermail, username=username, userrole=userrole, usertc=usertckno)
    else:
        return redirect(url_for("login"))


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
