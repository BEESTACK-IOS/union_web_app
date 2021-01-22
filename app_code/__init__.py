import os

from flask import Flask, render_template, redirect, url_for, request, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import date
import psycopg2
import pusher
from werkzeug.utils import secure_filename
import json

"""
con = psycopg2.connect( host="Carnagie-1760.postgres.pythonanywhere-services.com",port="11760",database="buromemursen",user="super",password="facethest0rm")

"""

app = Flask(__name__)
app.secret_key = "boraadamdir"
app.config['UPLOAD_FOLDER_FIRM'] = "static/images/firm"
app.config['UPLOAD_FOLDER_NEWS'] = "static/images/news"
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = "unionwebapp@gmail.com"
app.config['MAIL_PASSWORD'] = "Union123app"

mail = Mail(app)

pusher_client = pusher.Pusher(
    app_id="1132585",
    key="ed89289759f2f434f256",
    secret="4bd8e6fd627fba65f76d",
    cluster="eu",
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
        message_date = date.today()
        con = psycopg2.connect( host="Carnagie-1760.postgres.pythonanywhere-services.com",port="11760",database="buromemursen",user="super",password="facethest0rm")

        cur = con.cursor()

        if message == "Talep İşlemi Başlatılıyor..":
            sql_insert = "INSERT INTO unionschema.talep_log (channel_name, sender_id, reciever_id, ticket_status, mesdate, mestime) VALUES ( '{}', '{}', '{}', {}, '{}', '{}') ON CONFLICT (channel_name) DO UPDATE SET ticket_status = {}, mesdate = '{}', mestime = '{}'".format(
                channelName, userid, recieverid, 0, mesDate, mesTime, 0, mesDate, mesTime)
            log_insert = "INSERT into unionschema.system_logs ( member_id, action_id, action_name, action_date) values({}, {}, '{}', TIMESTAMP '{}')".format(
                userid, 2, 'Talep', message_date)
            cur.execute(sql_insert)
            cur.execute(log_insert)
        elif message == "Görüş Önerisi Başlatılıyor..":
            sql_insert = "INSERT INTO unionschema.talep_log (channel_name, sender_id, reciever_id, ticket_status, mesdate, mestime) VALUES ( '{}', '{}', '{}', {}, '{}', '{}') ON CONFLICT (channel_name) DO UPDATE SET ticket_status = {}, mesdate = '{}', mestime = '{}'".format(
                channelName, userid, recieverid, 1, mesDate, mesTime, 1, mesDate, mesTime)
            log_insert = "INSERT into unionschema.system_logs ( member_id, action_id, action_name, action_date) values({}, {}, '{}', TIMESTAMP '{}')".format(
                userid, 3, 'Gorus', message_date)
            cur.execute(sql_insert)
            cur.execute(log_insert)
        elif message == "Talep Karşılandı Sisteme Kaydediliyor..":
            sql_insert = "INSERT INTO unionschema.talep_log (channel_name, sender_id, reciever_id, ticket_status, mesdate, mestime) VALUES ( '{}', '{}', '{}', {}, '{}', '{}') ON CONFLICT (channel_name) DO UPDATE SET ticket_status = {}, mesdate = '{}', mestime = '{}'".format(
                channelName, userid, recieverid, 2, mesDate, mesTime, 2, mesDate, mesTime)
            log_insert = "INSERT into unionschema.system_logs ( member_id, action_id, action_name, action_date) values({}, {}, '{}', TIMESTAMP '{}')".format(
                userid, 4, 'Talep Karsilandi', message_date)
            cur.execute(sql_insert)
            cur.execute(log_insert)
        elif message == "Talep Karşılanamadı Sisteme Kaydediliyor..":
            sql_insert = "INSERT INTO unionschema.talep_log (channel_name, sender_id, reciever_id, ticket_status, mesdate, mestime) VALUES ( '{}', '{}', '{}', {}, '{}', '{}') ON CONFLICT (channel_name) DO UPDATE SET ticket_status = {}, mesdate = '{}', mestime = '{}'".format(
                channelName, userid, recieverid, 3, mesDate, mesTime, 3, mesDate, mesTime)
            log_insert = "INSERT into unionschema.system_logs ( member_id, action_id, action_name, action_date) values({}, {}, '{}', TIMESTAMP '{}')".format(
                userid, 5, 'Talep Karsilanmadi', message_date)
            cur.execute(sql_insert)
            cur.execute(log_insert)

        cur.execute(
            "INSERT into unionschema.message_log ( channel_name, sender_id, reciever_id, message, mesdate, mestime) values(%s, %s, %s, %s, %s, %s)",
            (channelName, userid, recieverid, message, mesDate, mesTime))
        con.commit()
        cur.close()
        con.close()
        pusher_client.trigger(channelName, 'new-message',
                              {'username': username, 'recievername': recievername, 'recieverid': recieverid,
                               'message': message, 'date': mesDate, 'time': mesTime})

        return jsonify({'result': 'success'})
    except Exception as e:
        return jsonify({'result': 'failure'})


@app.route('/messagehist', methods=['POST', 'GET'])
def messageHist():
    try:
        channelName = request.form.get('channelName')
        con = psycopg2.connect( host="Carnagie-1760.postgres.pythonanywhere-services.com",port="11760",database="buromemursen",user="super",password="facethest0rm")

        cur = con.cursor()
        cur.execute("select * from unionschema.message_log where channel_name='{}'".format(channelName))
        message_data = cur.fetchall()
        return jsonify({'result': 'success', 'message_data': message_data})
    except:
        return jsonify({'result': 'failure'})


@app.route('/postAdminTable', methods=['POST', 'GET'])
def postadmintable():
    try:
        con = psycopg2.connect( host="Carnagie-1760.postgres.pythonanywhere-services.com",port="11760",database="buromemursen",user="super",password="facethest0rm")

        cur = con.cursor()

        tableName = request.form.get("tablename")

        cur.execute("select * from {}".format(tableName))

        tableData = cur.fetchall()

        cur.close()
        con.close()

        return jsonify({'result': tableData})
    except:
        return jsonify({'result': "failure"})


@app.route('/postAdminTableDelete', methods=['POST', 'GET'])
def postadmintabledelete():
    try:
        con = psycopg2.connect( host="Carnagie-1760.postgres.pythonanywhere-services.com",port="11760",database="buromemursen",user="super",password="facethest0rm")

        cur = con.cursor()

        tableName = request.form.get("tablename")
        deleteId = request.form.get("deleteId")

        if tableName == "unionschema.firms":
            cur.execute("DELETE FROM {} WHERE firm_id = {}".format(tableName, deleteId))
        elif tableName == "unionschema.news":
            cur.execute("DELETE FROM {} WHERE news_id = {}".format(tableName, deleteId))
        elif tableName == "unionschema.members":
            cur.execute("DELETE FROM {} WHERE member_id = {}".format(tableName, deleteId))
        elif tableName == "unionschema.yonetim":
            cur.execute("DELETE FROM {} WHERE yonetim_id = {}".format(tableName, deleteId))
        con.commit()

        image_path = request.form.get("image_path")
        os.remove(image_path)

        cur.close()
        con.close()

        return jsonify({'result': "success"})
    except:
        return jsonify({'result': "failure"})


@app.route("/", methods=["GET", "POST"])
def index():

    data = ""
    ykdata = ""

    con = psycopg2.connect(host="Carnagie-1760.postgres.pythonanywhere-services.com", port="11760",
                           database="buromemursen", user="super", password="facethest0rm")

    cur = con.cursor()

    sql = "SELECT * FROM unionschema.news ORDER BY news_id DESC"
    cur.execute(sql);
    data = cur.fetchall()

    sql = "SELECT * FROM unionschema.yonetim ORDER BY yonetim_id DESC"
    cur.execute(sql);
    ykdata = cur.fetchall()

    cur.close()
    con.close()

    return render_template("index.html", data=data, ykdata=ykdata)

@app.route("/hakkimizda", methods=["GET", "POST"])
def hakkimizda():

    tuzuk = ""
    yonetim = ""

    con = psycopg2.connect(host="localhost", port="9999", database="buromemursen", user="super",
                           password="facethest0rm")
    cur = con.cursor()

    sql = "SELECT * FROM unionschema.tuzuk"
    cur.execute(sql);
    tuzuk = cur.fetchall()

    sql = "SELECT * FROM unionschema.yonetim"
    cur.execute(sql);
    yonetim = cur.fetchall()

    cur.close()
    con.close()

    return render_template("hakkimizda.html", tuzuk=tuzuk, yonetim=yonetim)

@app.route("/haberler_uyesiz", methods=["GET", "POST"])
def haberler_uyesiz():

    data = ""

    con = psycopg2.connect(host="localhost", port="9999", database="buromemursen", user="super",
                           password="facethest0rm")
    cur = con.cursor()

    sql = "SELECT * FROM unionschema.news ORDER BY news_id DESC"
    cur.execute(sql);
    data = cur.fetchall()

    cur.close()
    con.close()

    return render_template("haberler_uyesiz.html", data=data)

@app.route("/iletisim", methods=["GET", "POST"])
def iletisim():

    sendTo = "info@buromemursenaydin.com"
    if request.method == "POST":
        name = request.form["name"]
        mail = request.form["email"]
        message = request.form["message"]
        send_register_mail(name, mail, message,sendTo)

    return render_template("iletisim.html")


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
            if data == None:
                return redirect(url_for("login"))
            id = data[0]
            truePassword = data[3]
            mail = data[2]
            name = data[4]
            job = data[5]
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
                        session["job"] = job
                        cur.close()
                        con.close()
                        return redirect(url_for("admin"))
                    elif role == 1:
                        session["admin"] = "admin"
                        session["id"] = id
                        session["mail"] = mail
                        session["name"] = name
                        session["job"] = job
                        cur.close()
                        con.close()
                        return redirect(url_for("admin"))
                    elif role == 2:
                        session["user"] = "user"
                        session["id"] = id
                        session["mail"] = mail
                        session["name"] = name
                        session["job"] = job
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
    session.pop("mail", None)
    session.pop("name", None)
    session.pop("job", None)
    return redirect(url_for("login"))


def convert(tup, di):
    for a, b in tup:
        di.setdefault(str(a), []).append(b)
    return di


@app.route("/admin", methods=["POST", "GET"])
def admin():
    data = ""
    notificationData = ""
    systemdata = ""
    talepData = ""
    talepDataAssigned = []

    metadata = []

    if "admin" in session or "super" in session:
        con = psycopg2.connect( host="Carnagie-1760.postgres.pythonanywhere-services.com",port="11760",database="buromemursen",user="super",password="facethest0rm")

        cur = con.cursor()

        usermail = session["mail"]
        userid = session["id"]
        username = session["name"]

        sql = "SELECT m.member_name FROM unionschema.members as m, (SELECT tl.sender_id from unionschema.talep_log as tl WHERE tl.reciever_id = '{}' and tl.ticket_status != '2') tlu WHERE CAST(tlu.sender_id AS int) = m.member_id;".format(
            userid)
        cur.execute(sql)
        notificationData = cur.fetchall()
        if notificationData == None:
            notificationData = ["Kimse"]

        sql = "SELECT  ( SELECT COUNT(*) FROM unionschema.members ) AS membercount, ( SELECT COUNT(*) FROM   unionschema.firms) AS firmcount, (SELECT COUNT(*) FROM unionschema.news) AS newscount FROM    unionschema.dummy;"
        cur.execute(sql)
        metadata = cur.fetchone()
        if metadata == None:
            metadata = (None)

        sql = "SELECT m.member_name, s.action_name, s.action_date FROM unionschema.system_logs as s, unionschema.members as m WHERE m.member_id = s.member_id;"
        cur.execute(sql)
        systemdata = cur.fetchall()[:25]
        if systemdata == None:
            systemdata = ["Hiç Data Yok"]

        if "super" in session:
            userrole = "super"
            userDict = {}

            sql = "SELECT channel_name, ticket_status, mesdate FROM unionschema.talep_log"
            cur.execute(sql)
            talepData = cur.fetchall()

            sql = "SELECT member_id, member_name FROM unionschema.members"
            cur.execute(sql)
            userTuples = cur.fetchall()

            if talepData == None:
                talepData = ["kimse"]
            else:
                convert(userTuples, userDict)
                for i in range(0, len(talepData)):
                    idList = talepData[i][0].split("-")
                    talepDataAssigned.append((userDict[idList[0]][0] + "-" + userDict[idList[1]][0], talepData[i][1],
                                              talepData[i][2], talepData[i][0], idList[0], idList[1],
                                              userDict[idList[0]][0], userDict[idList[1]][0]))


        elif "admin" in session:
            userrole = "yönetici"

        if request.method == "POST":
            actName = request.form.get("submits", False)

            if actName == "firm_add":
                firm_name = request.form['firm_name']
                firm_abstract = request.form['firm_content']
                image = request.files['firm_logo']
                firm_lnt = request.form['firm_lat']
                firm_lng = request.form['firm_lng']

                imagename = secure_filename(image.filename)
                image.save(os.path.join(app.config['UPLOAD_FOLDER_FIRM'], imagename))
                image_path = app.config['UPLOAD_FOLDER_FIRM'] + "/" + imagename
                cur.execute(
                    "INSERT into unionschema.firms ( firm_name, firm_abstract, firm_logo, firm_lnt, firm_lng) values('{}', '{}', '{}', {}, {})".format
                    (firm_name.replace("'", "''"), firm_abstract.replace("'", "''"), image_path, firm_lnt, firm_lng))
                con.commit()
            elif actName == "news_add":
                news_name = request.form['news_name']
                news_abstract = request.form['news_content']
                news_ilceid = request.form['news_ilce']
                image = request.files['news_logo']

                imagename = secure_filename(image.filename)
                image.save(os.path.join(app.config['UPLOAD_FOLDER_NEWS'], imagename))
                image_path = app.config['UPLOAD_FOLDER_NEWS'] + "/" + imagename
                cur.execute(
                    "INSERT into unionschema.news ( news_name, news_abstract, news_logo, news_ilceid) values('{}', '{}', '{}', {})".format
                    (news_name.replace("'", "''"), news_abstract.replace("'", "''"), image_path, news_ilceid))
                con.commit()

            elif actName == "tckno_add":
                tckno = request.form['tckno']
                tckno_role = request.form['tckno_role']

                cur.execute(
                    "INSERT into unionschema.tckno_roles ( tckno, related_role) values( '{}', {}) ON CONFLICT (tckno) DO UPDATE SET related_role = {}".format
                    (tckno, tckno_role, tckno_role))
                con.commit()

            elif actName == "ilce_yetkilisi_add":
                yetkili_name = request.form["ilce_yetkilisi_name"]
                ilce_id = request.form["ilce_name"]
                yetkili_mail = request.form["ilce_yetkilisi_mail"]
                yetkili_phone = request.form["ilce_yetkilisi_phone"]

                cur.execute(
                    "INSERT into unionschema.ilce_sorumlulari ( ilce_id, ilce_sorumlu_name, ilce_sorumlu_phone, ilce_sorumlu_mail) values( {},'{}','{}', '{}') ON CONFLICT (ilce_id) DO UPDATE SET ilce_sorumlu_name = '{}', ilce_sorumlu_phone = '{}', ilce_sorumlu_mail = '{}'".format
                    (ilce_id, yetkili_name, yetkili_phone, yetkili_mail, yetkili_name, yetkili_phone, yetkili_mail))
                con.commit()

            elif actName == "yk_add":
                # print(request.form["yk_name"])
                name = request.form["yk_name"]
                rutbe = request.form["yk_rutbe"]
                image = request.files['yonetim_logo']

                imagename = secure_filename(image.filename)
                image.save(os.path.join(app.config['UPLOAD_FOLDER_NEWS'], imagename))
                image_path = app.config['UPLOAD_FOLDER_NEWS'] + "/" + imagename
                cur.execute(
                    "INSERT into unionschema.yonetim (yonetim_name, yonetim_logo, yonetim_rutbe) values('{}', '{}', '{}')".format
                    (name, image_path, rutbe))
                con.commit()

            elif actName == "tz_add":
                # print(request.form["tuzuk_content"])
                tuzuk = request.form["tuzuk_content"]
                cur.execute(
                    "INSERT into unionschema.tuzuk (tuzuk_abstract) values('{}')".format
                    (tuzuk.replace("'", "''")))
                con.commit()

        cur.close()
        con.close()
        return render_template("admin.html", data=data, notificationData=notificationData, userrole=userrole,
                               talepDataAssigned=talepDataAssigned, metadata=metadata, systemdata=systemdata)

    else:
        userrole = "üye"
        return redirect(url_for("logout"))


@app.route("/talep", methods=["POST", "GET"])
def ticket():
    data = ""
    notificationData = ""

    if "admin" in session or "super" in session or "user" in session:

        con = psycopg2.connect( host="Carnagie-1760.postgres.pythonanywhere-services.com",port="11760",database="buromemursen",user="super",password="facethest0rm")

        cur = con.cursor()

        usermail = session["mail"]
        userid = session["id"]
        username = session["name"]

        sql = "SELECT m.member_name FROM unionschema.members as m, (SELECT tl.sender_id from unionschema.talep_log as tl WHERE tl.reciever_id = '{}' and tl.ticket_status != '2') tlu WHERE CAST(tlu.sender_id AS int) = m.member_id;".format(
            userid)
        cur.execute(sql);
        notificationData = cur.fetchall()
        if notificationData == None:
            notificationData = ["Kimse"]

        if "super" in session:
            userrole = "super"

            sql = "SELECT m.member_id, m.member_name, m.member_mail, mr.member_role, m.member_job FROM unionschema.members as m, unionschema.member_role mr WHERE m.member_id = mr.member_id;"
            cur.execute(sql)
            data = cur.fetchall()
        elif "admin" in session:
            userrole = "yönetici"

            sql = "SELECT m.member_id, m.member_name, m.member_mail, mr.member_role, m.member_job FROM unionschema.members as m, unionschema.member_role mr WHERE m.member_id = mr.member_id;"
            cur.execute(sql)
            data = cur.fetchall()

        elif "user" in session:
            userrole = "üye"

            sql = "SELECT m.member_id, m.member_name, m.member_mail, mr.member_role, m.member_job FROM unionschema.members as m, unionschema.member_role mr WHERE m.member_id = mr.member_id AND ( mr.member_role = 0 OR mr.member_role = 1);"
            cur.execute(sql)
            data = cur.fetchall()

        cur.close()
        con.close()
        return render_template("ticket.html", data=data, userid=userid, username=username, userrole=userrole,
                               notificationData=notificationData)
    else:
        return render_template("login.html")


@app.route("/user", methods=["POST", "GET"])
def user():
    data = ""
    notificationData = ""

    if "admin" in session or "super" in session or "user" in session:

        con = psycopg2.connect( host="Carnagie-1760.postgres.pythonanywhere-services.com",port="11760",database="buromemursen",user="super",password="facethest0rm")

        cur = con.cursor()

        usermail = session["mail"]
        userid = session["id"]
        username = session["name"]

        sql = "SELECT m.member_name FROM unionschema.members as m, (SELECT tl.sender_id from unionschema.talep_log as tl WHERE tl.reciever_id = '{}' and tl.ticket_status != '2') tlu WHERE CAST(tlu.sender_id AS int) = m.member_id;".format(
            userid)
        cur.execute(sql);
        notificationData = cur.fetchall()
        if notificationData == None:
            notificationData = ["Kimse"]

        if "super" in session:
            userrole = "super"

        elif "admin" in session:
            userrole = "yönetici"

        elif "user" in session:
            userrole = "üye"

        sql = "SELECT * FROM unionschema.news ORDER BY news_id DESC"
        cur.execute(sql);
        data = cur.fetchall()

        cur.close()
        con.close()

    return render_template("haberler.html", userrole=userrole, data=data)


@app.route("/haberler", methods=["POST", "GET"])
def haberler():
    data = ""
    notificationData = ""

    if "admin" in session or "super" in session or "user" in session:

        con = psycopg2.connect( host="Carnagie-1760.postgres.pythonanywhere-services.com",port="11760",database="buromemursen",user="super",password="facethest0rm")

        cur = con.cursor()

        usermail = session["mail"]
        userid = session["id"]
        username = session["name"]

        sql = "SELECT m.member_name FROM unionschema.members as m, (SELECT tl.sender_id from unionschema.talep_log as tl WHERE tl.reciever_id = '{}' and tl.ticket_status != '2') tlu WHERE CAST(tlu.sender_id AS int) = m.member_id;".format(
            userid)
        cur.execute(sql);
        notificationData = cur.fetchall()
        if notificationData == None:
            notificationData = ["Kimse"]

        if "super" in session:
            userrole = "super"

        elif "admin" in session:
            userrole = "yönetici"

        elif "user" in session:
            userrole = "üye"

        sql = "SELECT * FROM unionschema.news ORDER BY news_id DESC"
        cur.execute(sql);
        data = cur.fetchall()

        cur.close()
        con.close()

    return render_template("haberler.html", userrole=userrole, data=data)


@app.route("/magazalar", methods=["POST", "GET"])
def magazalar():
    data = ""
    notificationData = ""

    if "admin" in session or "super" in session or "user" in session:

        con = psycopg2.connect( host="Carnagie-1760.postgres.pythonanywhere-services.com",port="11760",database="buromemursen",user="super",password="facethest0rm")

        cur = con.cursor()

        usermail = session["mail"]
        userid = session["id"]
        username = session["name"]

        sql = "SELECT m.member_name FROM unionschema.members as m, (SELECT tl.sender_id from unionschema.talep_log as tl WHERE tl.reciever_id = '{}' and tl.ticket_status != '2') tlu WHERE CAST(tlu.sender_id AS int) = m.member_id;".format(
            userid)
        cur.execute(sql);
        notificationData = cur.fetchall()
        if notificationData == None:
            notificationData = ["Kimse"]

        if "super" in session:
            userrole = "super"

        elif "admin" in session:
            userrole = "yönetici"

        elif "user" in session:
            userrole = "üye"

        sql = "SELECT * FROM unionschema.firms ORDER BY firm_id DESC"
        cur.execute(sql);
        data = cur.fetchall()

        con.close()
        cur.close()

    return render_template("magazalar.html", userrole=userrole, data=data)


def send_reset_mail(mail_adress, token):
    msg = Message('Password Reset', sender='unionwebapp@gmail.com', recipients=[mail_adress])
    msg.body = f'''Sifrenizi sifirlamak icin: {url_for('pass_reset', token=token, _external=True)} '''
    mail.send(msg)

def send_register_mail(user_name, user_mail, user_message,sendTo):
    msg = Message('Password Reset', sender='unionwebapp@gmail.com', recipients=[sendTo])
    msg.body = "kullanıcı adı = '{}', kullanıcı mail = '{}', kullanıcı mesaj = '{}'".format(user_name,user_mail,user_message)
    mail.send(msg)

def get_reset_token(user_id, expires_sec):
    ser = Serializer(app.config['SECRET_KEY'], expires_sec)
    return ser.dumps(user_id).decode('utf-8')


def verify_token(token):
    ser = Serializer(app.config['SECRET_KEY'])
    try:
        id = ser.loads(token)[0]
        return id
    except:
        return redirect("login.html")


@app.route("/sifremi_unuttum", methods=["POST", "GET"])
def sifremi_unuttum():
    if request.method == "POST":
        mail = request.form["email"]
        con = psycopg2.connect( host="Carnagie-1760.postgres.pythonanywhere-services.com",port="11760",database="buromemursen",user="super",password="facethest0rm")

        cur = con.cursor()
        cur.execute("select member_id from unionschema.members where member_mail='{}'".format(mail))
        memberid = cur.fetchone()
        if memberid:
            token = get_reset_token(memberid, 900)
            send_reset_mail(mail, token)
        else:
            print("error in userid: {} no reletad mail".format(memberid))

        cur.close()
        con.close()

    return render_template("pages-forget.html")


@app.route("/sifremi_unuttum/<token>", methods=["POST", "GET"])
def pass_reset(token):
    if "admin" in session or "super" in session:
        return redirect(url_for("admin"))

    elif "user" in session:
        return redirect(url_for("user"))
    else:
        member_id = verify_token(token)
        if request.method == "POST":
            password = request.form["pass"]
            re_password = request.form["re_pass"]
            if (password == re_password) and len(password) > 0:
                con = psycopg2.connect(host="localhost", port="9999", database="buromemursen", user="super",
                                       password="facethest0rm")
                cur = con.cursor()
                password = generate_password_hash(password, method='sha256')
                cur.execute(
                    "update unionschema.members set member_password ='{}' where member_id='{}'".format(password,
                                                                                                       member_id))
                con.commit()
                cur.close()
                con.close()
        return render_template("reset-password.html")


@app.route("/profil", methods=["POST", "GET"])
def profil():
    notificationData = ""
    if "admin" in session or "super" in session or "user" in session:
        con = psycopg2.connect( host="Carnagie-1760.postgres.pythonanywhere-services.com",port="11760",database="buromemursen",user="super",password="facethest0rm")

        cur = con.cursor()
        usermail = session["mail"]
        cur.execute("select member_tc from unionschema.members where member_mail='{}'".format(usermail))
        usertckno = cur.fetchone()[0]
        username = session["name"]
        userjob = session["job"]

        sql = "SELECT m.member_name FROM unionschema.members as m, (SELECT tl.sender_id from unionschema.talep_log as tl WHERE tl.reciever_id = '{}' and tl.ticket_status != '2') tlu WHERE CAST(tlu.sender_id AS int) = m.member_id;".format(
            session["id"])
        cur.execute(sql);
        notificationData = cur.fetchall()
        if notificationData == None:
            notificationData = ["Kimse"]

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
            form_job = request.form["alan"]
            cur.execute("select member_password from unionschema.members where member_tc='{}'".format(usertckno))
            hashed_password = cur.fetchone()[0]
            if check_password_hash(hashed_password, form_oldPassword):
                if len(form_mail) > 0:
                    cur.execute(
                        "update unionschema.members set member_mail ='{}' where member_tc='{}'".format(form_mail,
                                                                                                       usertckno))
                    usermail = form_mail
                    session["mail"] = form_mail
                if len(form_newPassword) > 0:
                    new_password = generate_password_hash(form_newPassword, method='sha256')
                    cur.execute(
                        "update unionschema.members set member_password ='{}' where member_tc='{}'".format(new_password,
                                                                                                           usertckno))
                if len(form_job) > 0:
                    cur.execute(
                        "update unionschema.members set member_job ='{}' where member_tc='{}'".format(form_job,
                                                                                                      usertckno))
                    session["job"] = form_job
            """job = session["job"]
            print(job)"""
        con.commit()
        cur.close()
        con.close()
        return render_template("profil.html", usermail=usermail, username=username, userrole=userrole, usertc=usertckno,
                               notificationData=notificationData, userjob=userjob)
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
            register_date = date.today()

            if not password == password_again:
                return render_template("register.html", errorType=errorType)
            else:
                con = psycopg2.connect(host="localhost", port="9999", database="buromemursen", user="super",
                                       password="facethest0rm")
                cur = con.cursor()
                cur.execute("select * from unionschema.tckno_roles where tckno='{}'".format(tckn))
                tcnko_roles_control = cur.fetchone()
                if (tcnko_roles_control == None) or (len(tcnko_roles_control) == 0):
                    errorType = 0
                    return render_template("register.html", errorType=errorType)
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
                        log_insert = "INSERT into unionschema.system_logs ( member_id, action_id, action_name, action_date) values({}, {}, '{}', TIMESTAMP '{}')".format(
                            member_id, 1, 'Kayit', register_date)
                        cur.execute(log_insert)
                        con.commit()
                        cur.close()
                        con.close()
                        return render_template("login.html", errorType=errorType)
                    else:
                        errorType = 1
                        cur.close()
                        con.close()
                        return render_template("register.html", errorType=errorType)
        return render_template("register.html", errorType=-1)


if __name__ == '__main__':
    app.run(debug=True)
