from flask import Flask, render_template, request
from flask_mail import Mail, Message
import os
from dotenv import find_dotenv, load_dotenv

dotenv_path = find_dotenv()

load_dotenv(dotenv_path)

mail_password = os.getenv("mail_password")

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/tattoos.html')
def tattoos():
    return render_template("tattoos.html")

@app.route('/class-info.html')
def class_info():
    return render_template("class-info.html")

@app.route('/events.html')
def commissions():
    return render_template("events.html")

@app.route('/contact.html')
def contact():
    return render_template("contact.html")

@app.route('/faq.html')
def faq():
    return render_template("faq.html")

@app.route('/gallery.html')
def gallery():
    return render_template("gallery.html")

@app.route('/classes.html')
def classes():
    return render_template("classes.html")


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'autoresponder375@gmail.com'
app.config['MAIL_PASSWORD'] = 'qpgt xupv vftq umsk'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

@app.route('/form', methods=["POST"])
def form():
    sender_name = request.form.get("name")
    sender_email = request.form.get("email")
    sender_subject = request.form.get("subject")
    sender_message = request.form.get("message")

    msg = Message(subject=sender_subject, sender=sender_email, recipients=['autoresponder375@gmail.com'])
    msg.body = sender_name + " has sent a message from " + sender_email + "\n\n" + sender_message
    mail.send(msg)

    return render_template("form.html", sender_name = sender_name, sender_email = sender_email, sender_subject = sender_subject, sender_message = sender_message)
