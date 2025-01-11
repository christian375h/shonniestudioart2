from flask import Flask, render_template, request, jsonify, redirect
from flask_mail import Mail, Message
import os, json

import stripe

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
def events():
    checkoutObj.setCount(1)
    checkoutObj.setSelection('facePaint')
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

# STRIPE PAYMENT INTENT
stripe.api_key = os.getenv('stripe_api_key_sk')

@app.route('/checkout.html')
def checkout():
    return render_template(
        'checkout.html', 
        selection = get_payment_selection(), 
        price = convert_price(calculate_order_amount()),
        count = checkoutObj.getPartySize(),
        stripeKeyPK = os.getenv('stripe_api_key_pk')
        )

@app.route('/success.html')
def success():
    return render_template(
        'success.html', 
        selection = get_payment_selection(),
        email = checkoutObj.getEmail(), 
        dateTime = checkoutObj.getDateTime(),
        partyName = checkoutObj.getPartyName())

def calculate_order_amount():
    def switch(item):
        if item == "facePaint":
            return 10000 * int(checkoutObj.getCount())
        elif item == "glitterTattoos":
            return 5000 * int(checkoutObj.getCount())
        elif item == "paintNight":
            if int(checkoutObj.getCount()) < 15:
                return 3500 * int(checkoutObj.getCount())
            else:
                return 3000 * int(checkoutObj.getCount())
    return switch(checkoutObj.getSelection())

def convert_price(input):
    return str(input)[:-2] + ".00"

def get_payment_selection():
    def switch(item):
        if item == "facePaint":
            return "Face Painting"
        elif item == "glitterTattoos":
            return "Glitter Tattoos"
        elif item == "paintNight":
            return "Painting Night"
    return switch(checkoutObj.getSelection())

@app.route('/create-payment-intent', methods=['POST'])
def create_payment():
    try:
        data = json.loads(request.data)
        # Create a PaymentIntent with the order amount and currency
        intent = stripe.PaymentIntent.create(
            amount=calculate_order_amount(),
            currency='usd',
            # In the latest version of the API, specifying the `automatic_payment_methods` parameter is optional because Stripe enables its functionality by default.
            automatic_payment_methods={
                'enabled': True,
            },
        )
        return jsonify({
            'clientSecret': intent['client_secret']
        })
    except Exception as e:
        return jsonify(error=str(e)), 403

#class for handling count and selected checkout item
class checkoutHandler:
    def __init__(self, count, selection, email, dateTime, partyName, partySize):
         self.count = count
         self.selection = selection
         self.email = email
         self.dateTime = dateTime
         self.partyName = partyName
    #count
    def getCount(self):
        return self.count 
    def setCount(self, x): 
        self.count = x 

    #partySize
    def getPartySize(self):
        return self.partySize
    def setPartySize(self, x): 
        self.partySize = x 

    #selection
    def getSelection(self): 
        return self.selection
    def setSelection(self, x): 
        self.selection = x

    #email
    def getEmail(self):
        return self.email
    def setEmail(self, x):
        self.email = x

    #dateTime
    def getDateTime(self):
        return self.dateTime
    def setDateTime(self, x):
        self.dateTime = x

    #party name
    def getPartyName(self):
        return self.partyName
    def setPartyName(self, x):
        self.partyName = x

checkoutObj = checkoutHandler(1, 'facePaint', "", "", "", 0)

@app.route('/selector-process', methods=['POST'])
def selProcess(): 
    data = request.get_json()

    selection = data['selection']
    count = data['count']
    partySize = data['partySize']

    checkoutObj.setSelection(selection)
    checkoutObj.setCount(count)
    checkoutObj.setPartySize(partySize)

    return jsonify(result=selection)

@app.route('/checkout-process', methods=['POST'])
def checkProcess(): 
    data = request.get_json()

    partyName = data['partyName']
    custEmail = data['email']
    dateTime = data['dateTime']

    checkoutObj.setEmail(custEmail)
    checkoutObj.setDateTime(dateTime)
    checkoutObj.setPartyName(partyName)

    msg = Message(subject=get_payment_selection(), sender=os.getenv('mail_address_1'), recipients=[os.getenv('mail_address_1'), os.getenv('mail_address_2'), custEmail])
    msg.body = "Successful payment from " + partyName + " of $" + str(convert_price(calculate_order_amount())) + "\n\n" + "Scheduled for " + dateTime + " for " + get_payment_selection()

    mail.send(msg)

    return jsonify(result=custEmail)

# FLASK MAIL

print(os.getenv('email_password'))

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.getenv('mail_address_1')
app.config['MAIL_PASSWORD'] = os.getenv('email_password')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

@app.route('/form', methods=["POST"])
def form():
    sender_name = request.form.get("name")
    sender_email = request.form.get("email")
    sender_subject = request.form.get("subject")
    sender_message = request.form.get("message")

    msg = Message(subject=sender_subject, sender=sender_email, recipients=[os.getenv('mail_address_1'), sender_email])
    msg.body = sender_name + " has sent a message from " + sender_email + "\n\n" + sender_message
    mail.send(msg)

    return render_template("form.html", sender_name = sender_name, sender_email = sender_email, sender_subject = sender_subject, sender_message = sender_message)
