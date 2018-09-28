from flask import Flask, flash, url_for, redirect, session, render_template, request

from functools import wraps

from content_management import Content

from db_connect import connection
from MySQLdb import escape_string as thwart
from passlib.hash import sha256_crypt
import gc

from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired

from functions import Registration_Checker

import datetime





"""
from content_management import Content
from db_connect import connection
from passlib.hash import sha256_crypt
from MySQLdb import escape_string as thwart
import datetime
import gc

#Import Content management dictionary, to be able to dynamically do stuff
PAGE_DICTIONARY = Content()
"""
#####################################
### APP SETUP #######################
#####################################

app = Flask(__name__)

app.config.update(dict(
    DEBUG = True,
    #EMAIL SETTINGS
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_SSL=False,
    MAIL_USE_TLS=True,
    MAIL_USERNAME = 'vertike@gmail.com',
    MAIL_PASSWORD = 'arti1234567890'  
))

mail = Mail(app)


#TODO: GET confirmation e-mail working
tokenizer = URLSafeTimedSerializer("Secret TOKEN!")

PAGE_DICTIONARY = Content()


###############################
### LOGIN WRAPPER #############
###############################

#TODO: Cookies need to be used carefully
#TODO: Learn about cookies

### LOGIN WRAPPER ###
def Login_Required(function):
    @wraps(function)
    def wrap(*args, **kwargs):
        if "Logged_In" in session:
            return function(*args, **kwargs)
        else:
            flash("You need to log in!")
            return redirect(url_for("Login_Page"))
    return wrap
    
    



### Main Page ###
@app.route('/')
def homepage():
    return render_template("main.html", PAGE_DICTIONARY = PAGE_DICTIONARY)



######################################
### USER System >>> Login/Register ###
######################################
    
### Login ###
@app.route('/Login_Page/', methods = ["GET","POST"])
def Login_Page():
    error = ''
    try:
        c, conn = connection()
        if request.method == "POST":
            data = c.execute ("SELECT * FROM Users WHERE User_Name = (%s)", [thwart(request.form["User_Name"])])
            data = c.fetchone()[1]
            if sha256_crypt.verify(request.form["Login_Password"], data):
                session["Logged_In"] = True
                session["User_Name"] = request.form["User_Name"]
                flash("You are logged in")
                return redirect(url_for("dashboard"))
            else:
                error = "Invalid Credentials. Try Again."       
        gc.collect()
        return render_template("User_System/Login_Page.html", PAGE_DICTIONARY = PAGE_DICTIONARY, error = error)        
    except Exception as e:
        #flash(e)
        error = "Invalid Credentials. Try Again."
        return render_template("User_System/Login_Page.html", PAGE_DICTIONARY = PAGE_DICTIONARY, error = error)

#TODO: Haha
### Register ###
#######################################
###  ALL PASSWORD RULES COME HERE #####
#######################################

    

    

#####################
### Register page ###
#####################
#TODO: Put the password check in a module
@app.route('/Register_Page/', methods = ["GET","POST"])
def Register_Page():
    error = ""
    try:
        c, conn = connection()
        if request.method == "POST":
            attempted_username = request.form["User_Name"]
            attempted_email = request.form["Email"]
            attempted_password = request.form["Password"]
            attempted_repassword = request.form["Re_Password"]
            attempted_accept = request.form.get("Accept", False)
            if attempted_accept != False:
                attempted_accept = True
            ### Flashing the input for delevopment purposes ###
            flash(attempted_username)
            flash(attempted_email)
            flash(attempted_password)
            flash(attempted_repassword)
            flash(attempted_accept)
            ###################################
            ### Registration checking #########
            ###################################
            error = Registration_Checker(attempted_username, attempted_email, 
                                         attempted_password, attempted_repassword,
                                         attempted_accept)
            if error != "":
                render_template("User_System/Register_Page.html", PAGE_DICTIONARY = PAGE_DICTIONARY, error = error)
            #####################################
            ### PASSWORD ENCRYPTION #############
            #####################################
            else:
                encrypted_password = sha256_crypt.encrypt((str(attempted_password)))
                x = c.execute("SELECT * FROM Users WHERE User_Name = (%s)", [attempted_username])
                y = c.execute("SELECT * FROM Users WHERE E_Mail = (%s)", [attempted_email])
                if int(x) > 0:
                    error = "That username is already taken, please choose another"
                    render_template("Register_Page.html", PAGE_DICTIONARY = PAGE_DICTIONARY, error = error)
                elif int(y) > 0:
                    error = "That e-mail is already taken, please choose another"
                    render_template("Register_Page.html", PAGE_DICTIONARY = PAGE_DICTIONARY, error = error)
                else:
                    c.execute("INSERT INTO Users (User_Name, User_Password, E_mail, Registration_Date, " +
                               "Last_Login, User_Rank, User_Rights, User_Activated) " +
                              "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", [thwart(attempted_username),
                               thwart(encrypted_password), thwart(attempted_email), datetime.datetime.today(),
                               datetime.datetime.today(), 0, 0, 0])
                    conn.commit()
                    token = tokenizer.dumps(attempted_email, salt = "Email-confirm_HAHA")
                    c.execute("SELECT * FROM Users WHERE User_Name = (%s)", [attempted_username])
                    User_Data = c.fetchall()
                    User_ID = User_Data[0][0]
                    flash(User_Data)
                    flash(User_ID)
                    #flash(token)
                    #flash(tokenizer.loads(token, salt = "Email-confirm_HAHA", max_age = 3600))
                    #TODO: Make a nice email
                    msg = Message("Hello World",
                                  sender="vertike@gmail.com",
                                  recipients=["vertikegroup@gmail.com"])
                    msg.body = ("Dear " + User_Data[0][2] + "\r\n \r\n"
                               + "Here is your activation link: \r\n"
                               + "http://142.93.232.189/Confirm_Email/?token=" + str(token) + "&userid=" + str(User_ID))
                    mail.send(msg)
                    flash("Thanks for registering")
                    c.close()
                    conn.close()
                    gc.collect()
                    session["Logged_In"] = True
                    session["User_Name"] = attempted_username
                    return redirect(url_for("Succesful_Registration"))
        return render_template("User_System/Register_Page.html", PAGE_DICTIONARY = PAGE_DICTIONARY, error = error)
    except Exception as e:
        flash(e)
        return render_template("User_System/Register_Page.html", PAGE_DICTIONARY = PAGE_DICTIONARY, error = error)

##############################
### CONFIRMATION WAS SENT ####
##############################


@app.route("/Succesful_Registration/")
def Succesful_Registration():
    return render_template("User_System/Succesful_Registration.html", PAGE_DICTIONARY = PAGE_DICTIONARY)

#TODO: Overwrite Activated >>> IMPORTANT
@app.route("/Confirm_Email/", methods = ["GET", "POST"])
def Confirm_Email():
    error = ""
    try:
        c, conn = connection()
        User_ID = request.args.get("userid", None)
        token = request.args.get("token", None)
        c.execute("SELECT E_Mail FROM Users WHERE User_ID = (%s)", [User_ID])
        User_E_Mail = c.fetchone()[0]
        if User_E_Mail == tokenizer.loads(token, salt = "Email-confirm_HAHA", max_age = 7200):
            c.execute("UPDATE Users SET User_Activated=1 WHERE User_ID = (%s)", [User_ID])
            conn.commit()
            c.close()
            conn.close()
            gc.collect()
            flash("TOKEN WORKS; U r activated")
            return redirect (url_for("homepage"))
        else:
            error = "User_ID is: " + str(User_ID) + ". Token is: " + str(token)
            return render_template("User_System/Confirm_Email.html", PAGE_DICTIONARY = PAGE_DICTIONARY, error = error)
    except SignatureExpired:
        #TODO: Fix this, to make it beautiful
        return "The token has expired"
    except Exception as e:
        flash(e)
        return render_template("User_System/Confirm_Email.html", PAGE_DICTIONARY = PAGE_DICTIONARY, error = error)

### Logout


@app.route("/Logout/")
@Login_Required
def Logout():
    session.clear()
    flash("You have been logged out")
    gc.collect()
    return redirect(url_for("homepage"))

#################
### DASHBOARD ###
#################
        

@app.route('/dashboard/')
def dashboard():
    return render_template("dashboard.html", PAGE_DICTIONARY = PAGE_DICTIONARY)

### 404 ERROR HANDLING ###
@app.errorhandler(404)
def Page_Not_Found(e):
    return render_template("Error_Handling/404Error.html", PAGE_DICTIONARY = PAGE_DICTIONARY)

@app.errorhandler(405)
def Method_Not_Found(e):
    return render_template("Error_Handling/405Error.html", PAGE_DICTIONARY = PAGE_DICTIONARY)

@app.route('/slashboard/')
def slashboard():
    try:
        return render_template("dashboard.html", PAGE_DICTIONARY = wtf)
    except Exception as e:
        return render_template("Error_Handling/500Error.html", error = e)


#TODO: Here is the RUNNING command
if __name__ == "__main__":
    app.run(debug=True)
