from __future__ import print_function
from flask import render_template, request, Flask
import os
import stripe

from pprint import pprint
# set the project root directory as the static folder, you can set others.
app = Flask(__name__)
app.config['SECRET_KEY'] = 'this-is-a-stripe-application'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Provide your Stripe keys here

STRIPE_SECRET_KEY = ''
PUBLISHABLE_SECRET_KEY = ''
CURRENCY = 'usd' # Change it if you need

if not STRIPE_SECRET_KEY:
    print("Please provide STRIPE_SECRET_KEY")
    exit(-1)

if not PUBLISHABLE_SECRET_KEY:
    print("Please provide PUBLISHABLE_SECRET_KEY ")
    exit(-1)

stripe.api_key = STRIPE_SECRET_KEY

# Provide your domain name here
YOUR_DOMAIN = 'http://localhost:5000'


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        amount = request.form.get('amount')
        email = request.form.get('email')
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            mode='payment',
            line_items=[{
                'price_data': {
                    'currency': CURRENCY,
                    'product_data': {
                        'name': 'Test Payment',
                    },
                    'unit_amount': int(float(amount)*100),
                },
                'quantity': 1,
            }],
            success_url=YOUR_DOMAIN + '/success',
            cancel_url=YOUR_DOMAIN + '/cancel',
        )

        return render_template('checkout.html', key=PUBLISHABLE_SECRET_KEY,
                               amount=amount, currency=CURRENCY.upper(),
                               checkout_session_id=checkout_session.id)
    return render_template("index.html")


@app.route('/cancel', methods=['GET'])
def cancel():
    return render_template('cancel.html')


@app.route('/success', methods=['GET'])
def charge():
    return render_template('success.html')


if __name__ == "__main__":
    app.run(debug=True)


