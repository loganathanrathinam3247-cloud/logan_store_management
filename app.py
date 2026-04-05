from flask import Flask, render_template, request, redirect, url_for, session, flash
import time

app = Flask(__name__)
app.secret_key = 'super_secret_key_shop'

# 50 data set creation access dict
stock_data = {
    "101": {"name": "Apple", "price": 30, "quantity": 100},
    "102": {"name": "Banana", "price": 10, "quantity": 200},
    "103": {"name": "Orange", "price": 20, "quantity": 150},
    "104": {"name": "Mango", "price": 50, "quantity": 80},
    "105": {"name": "Grapes", "price": 60, "quantity": 120},
    "106": {"name": "Watermelon", "price": 100, "quantity": 40},
    "107": {"name": "Pineapple", "price": 80, "quantity": 50},
    "108": {"name": "Papaya", "price": 40, "quantity": 60},
    "109": {"name": "Pomegranate", "price": 70, "quantity": 90},
    "110": {"name": "Guava", "price": 25, "quantity": 110},
    "111": {"name": "Tomato", "price": 15, "quantity": 300},
    "112": {"name": "Potato", "price": 20, "quantity": 400},
    "113": {"name": "Onion", "price": 25, "quantity": 350},
    "114": {"name": "Carrot", "price": 40, "quantity": 150},
    "115": {"name": "Cabbage", "price": 30, "quantity": 100},
    "116": {"name": "Cauliflower", "price": 35, "quantity": 90},
    "117": {"name": "Spinach", "price": 12, "quantity": 200},
    "118": {"name": "Brinjal", "price": 22, "quantity": 180},
    "119": {"name": "Ladies Finger", "price": 28, "quantity": 160},
    "120": {"name": "Capsicum", "price": 45, "quantity": 140},
    "121": {"name": "Milk", "price": 25, "quantity": 200},
    "122": {"name": "Bread", "price": 35, "quantity": 80},
    "123": {"name": "Eggs(1Dozen)", "price": 60, "quantity": 150},
    "124": {"name": "Butter", "price": 120, "quantity": 60},
    "125": {"name": "Cheese", "price": 150, "quantity": 50},
    "126": {"name": "Yogurt", "price": 30, "quantity": 100},
    "127": {"name": "Rice(1kg)", "price": 50, "quantity": 500},
    "128": {"name": "Wheat(1kg)", "price": 40, "quantity": 400},
    "129": {"name": "Dal", "price": 90, "quantity": 300},
    "130": {"name": "Sugar", "price": 45, "quantity": 250},
    "131": {"name": "Salt", "price": 20, "quantity": 300},
    "132": {"name": "Tea Powder", "price": 250, "quantity": 100},
    "133": {"name": "Coffee Powder", "price": 300, "quantity": 80},
    "134": {"name": "Cooking Oil(1L)", "price": 150, "quantity": 200},
    "135": {"name": "Ghee", "price": 400, "quantity": 50},
    "136": {"name": "Biscuit", "price": 10, "quantity": 500},
    "137": {"name": "Chocolate", "price": 20, "quantity": 400},
    "138": {"name": "Chips", "price": 15, "quantity": 300},
    "139": {"name": "Juice", "price": 40, "quantity": 150},
    "140": {"name": "Soft Drink", "price": 35, "quantity": 200},
    "141": {"name": "Soap", "price": 25, "quantity": 300},
    "142": {"name": "Shampoo", "price": 150, "quantity": 150},
    "143": {"name": "Toothpaste", "price": 50, "quantity": 200},
    "144": {"name": "Toothbrush", "price": 20, "quantity": 250},
    "145": {"name": "Detergent", "price": 120, "quantity": 180},
    "146": {"name": "Dishwash", "price": 60, "quantity": 100},
    "147": {"name": "Floor Cleaner", "price": 80, "quantity": 120},
    "148": {"name": "Tissue Paper", "price": 40, "quantity": 150},
    "149": {"name": "Garbage Bags", "price": 50, "quantity": 100},
    "150": {"name": "Matchbox", "price": 2, "quantity": 500}
}

transactions_history = []

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'adminbba':
            session['logged_in'] = True
            return redirect(url_for('menu'))
        else:
            flash('Invalid Credentials! Try admin / adminbba', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/menu')
def menu():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('menu.html')

@app.route('/stock')
def stock():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    # Calculation of total unique items and total stock quantity
    total_items = len(stock_data)
    total_stock = sum(item['quantity'] for item in stock_data.values())
    return render_template('stock.html', stock=stock_data, total_items=total_items, total_stock=total_stock)

@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        name = request.form['name']
        price = int(request.form['price'])
        quantity = int(request.form['quantity'])
        
        new_id = str(max([int(k) for k in stock_data.keys()] + [100]) + 1)
        stock_data[new_id] = {'name': name, 'price': price, 'quantity': quantity}
        flash('Item added successfully!', 'success')
        return redirect(url_for('stock'))
        
    return render_template('add_item.html')

@app.route('/edit_item/<pid>', methods=['GET', 'POST'])
def edit_item(pid):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    if pid not in stock_data:
        flash('Item not found!', 'danger')
        return redirect(url_for('stock'))
        
    if request.method == 'POST':
        stock_data[pid]['name'] = request.form['name']
        stock_data[pid]['price'] = int(request.form['price'])
        stock_data[pid]['quantity'] = int(request.form['quantity'])
        flash('Item updated successfully!', 'success')
        return redirect(url_for('stock'))
        
    return render_template('edit_item.html', pid=pid, item=stock_data[pid])

@app.route('/sales', methods=['GET', 'POST'])
def sales():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        customer_name = request.form['customer_name']
        product_ids = request.form.getlist('product_id')
        quantities = request.form.getlist('quantity')
        
        purchased_items = []
        total_amount = 0
        error = False

        for i in range(len(product_ids)):
            pid = product_ids[i]
            qty = int(quantities[i])
            if qty <= 0:
                continue
            
            if pid in stock_data:
                if stock_data[pid]['quantity'] >= qty:
                    # Update stock automatically
                    stock_data[pid]['quantity'] -= qty
                    item_total = stock_data[pid]['price'] * qty
                    total_amount += item_total
                    purchased_items.append({
                        'name': stock_data[pid]['name'],
                        'price': stock_data[pid]['price'],
                        'quantity': qty,
                        'total': item_total
                    })
                else:
                    flash(f"Not enough stock for {stock_data[pid]['name']}. Available: {stock_data[pid]['quantity']}", "danger")
                    error = True
        
        if not error and purchased_items:
            # Time module use
            current_time = time.strftime('%Y-%m-%d %H:%M:%S')
            transaction = {
                'customer_name': customer_name,
                'purchased_items': purchased_items,
                'total_amount': total_amount,
                'time': current_time
            }
            # Record sales transaction
            transactions_history.append(transaction)
            
            # Flash success to trigger bill generation view
            session['last_bill'] = transaction
            flash('Sale successful! Bill generated.', 'success')
            return redirect(url_for('bill'))
    
    return render_template('sales.html', stock=stock_data)

@app.route('/bill')
def bill():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    transaction = session.get('last_bill')
    if not transaction:
        return redirect(url_for('sales'))
        
    return render_template('bill.html', bill=transaction)

@app.route('/history')
def history():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('history.html', history=transactions_history)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
