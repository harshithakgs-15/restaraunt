from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)

PRICES = {
    "Fries": 25,
    "Lunch": 40,
    "Burger": 35,
    "Pizza": 50,
    "CheeseBurger": 30,
    "Drinks": 35
}

def calculate_totals(order):
    try:
        fries = int(order.get("fries", 0))
        lunch = int(order.get("lunch", 0))
        burger = int(order.get("burger", 0))
        pizza = int(order.get("pizza", 0))
        cheese = int(order.get("cheese", 0))
        drinks = int(order.get("drinks", 0))

        cost = (fries * PRICES["Fries"] +
                lunch * PRICES["Lunch"] +
                burger * PRICES["Burger"] +
                pizza * PRICES["Pizza"] +
                cheese * PRICES["CheeseBurger"] +
                drinks * PRICES["Drinks"])

        service_charge = round(cost / 99, 2)
        tax = round(cost * 0.33, 2)
        total = round(cost + service_charge + tax, 2)

        return {
            "cost": f"Rs. {cost:.2f}",
            "service_charge": f"Rs. {service_charge:.2f}",
            "tax": f"Rs. {tax:.2f}",
            "subtotal": f"Rs. {cost:.2f}",
            "total": f"Rs. {total:.2f}"
        }
    except ValueError:
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    result = {}
    order_id = random.randint(10000, 99999)
    if request.method == 'POST':
        if 'reset' in request.form:
            return redirect(url_for('index'))
        result = calculate_totals(request.form)
    return render_template("index.html", result=result, order_id=order_id)

@app.route('/price')
def price():
    return render_template("price.html", prices=PRICES)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Render provides PORT via env var
    app.run(debug=True, host='0.0.0.0', port=port)
