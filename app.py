from flask import Flask, render_template, request
import smtplib

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

@app.route('/commissions.html')
def commissions():
    return render_template("commissions.html")

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

@app.route('/form', methods=["POST"])
def form():
    sender_name = request.form.get("name")
    sender_email = request.form.get("email")
    sender_subject = request.form.get("subject")
    sender_message = request.form.get("message")

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login("christian375h@gmail.com", "hvvq pamz cqqn jecw")
    server.sendmail("christian375h@gmail.com", sender_email, sender_message)

    return render_template("form.html", sender_name = sender_name, sender_email = sender_email, sender_subject = sender_subject, sender_message = sender_message)
