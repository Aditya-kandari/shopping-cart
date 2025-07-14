from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'


# Database setup
def init_db():
    conn = sqlite3.connect('grocery_store.db')
    cursor = conn.cursor()

    # Create products table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL,
            image_url TEXT DEFAULT '/static/images/default.jpg'
        )
    ''')

    # Create cart table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cart (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            quantity INTEGER,
            added_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products (id)
        )
    ''')

    # Create orders table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            total_amount REAL NOT NULL,
            order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'pending'
        )
    ''')

    # Create order_items table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            product_id INTEGER,
            quantity INTEGER,
            price REAL,
            FOREIGN KEY (order_id) REFERENCES orders (id),
            FOREIGN KEY (product_id) REFERENCES products (id)
        )
    ''')

    # Insert sample data if products table is empty
    cursor.execute('SELECT COUNT(*) FROM products')
    if cursor.fetchone()[0] == 0:
        sample_products = [
            ('Apple - 1Kg', 'Fruits', 180, 50),
            ('Banana - 1 Dozen', 'Fruits', 60, 30),
            ('Milk - 1L', 'Dairy', 31, 25),
            ('Bread', 'Bakery', 55, 40),
            ('Eggs - 1 Dozen', 'Dairy', 75, 20),
            ('Chicken Breast - 1Kg', 'Meat', 250, 15),
            ('Rice - 1Kg', 'Grains', 40, 35),
            ('Tomatoes - 1Kg', 'Vegetables', 30, 45),
            ('Potatoes - 1Kg', 'Vegetables', 40, 60),
            ('Cheese - 100g', 'Dairy', 80, 18),
            ('Pasta - 1Kg', 'Grains', 90, 55),
            ('Orange Juice - 400Ml', 'Beverages', 33, 22)
        ]

        cursor.executemany(
            'INSERT INTO products (name, category, price, stock) VALUES (?, ?, ?, ?)',
            sample_products
        )

    conn.commit()
    conn.close()


# Routes
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/products')
def get_products():
    conn = sqlite3.connect('grocery_store.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products ORDER BY category, name')
    products = []
    for row in cursor.fetchall():
        products.append({
            'id': row[0],
            'name': row[1],
            'category': row[2],
            'price': row[3],
            'stock': row[4],
            'image_url': row[5]
        })
    conn.close()
    return jsonify(products)


@app.route('/api/cart')
def get_cart():
    conn = sqlite3.connect('grocery_store.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT c.id, p.name, p.price, c.quantity, (p.price * c.quantity) as total,
               p.id as product_id, p.category
        FROM cart c
        JOIN products p ON c.product_id = p.id
    ''')
    cart_items = []
    for row in cursor.fetchall():
        cart_items.append({
            'cart_id': row[0],
            'name': row[1],
            'price': row[2],
            'quantity': row[3],
            'total': row[4],
            'product_id': row[5],
            'category': row[6]
        })
    conn.close()
    return jsonify(cart_items)


@app.route('/api/cart/add', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)

    conn = sqlite3.connect('grocery_store.db')
    cursor = conn.cursor()

    # Check if item already in cart
    cursor.execute('SELECT id, quantity FROM cart WHERE product_id = ?', (product_id,))
    existing = cursor.fetchone()

    if existing:
        # Update quantity
        new_quantity = existing[1] + quantity
        cursor.execute('UPDATE cart SET quantity = ? WHERE id = ?', (new_quantity, existing[0]))
    else:
        # Add new item
        cursor.execute('INSERT INTO cart (product_id, quantity) VALUES (?, ?)', (product_id, quantity))

    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Item added to cart'})


@app.route('/api/cart/update', methods=['POST'])
def update_cart():
    data = request.get_json()
    cart_id = data.get('cart_id')
    quantity = data.get('quantity')

    conn = sqlite3.connect('grocery_store.db')
    cursor = conn.cursor()

    if quantity <= 0:
        cursor.execute('DELETE FROM cart WHERE id = ?', (cart_id,))
    else:
        cursor.execute('UPDATE cart SET quantity = ? WHERE id = ?', (quantity, cart_id))

    conn.commit()
    conn.close()
    return jsonify({'success': True})


@app.route('/api/cart/clear', methods=['POST'])
def clear_cart():
    conn = sqlite3.connect('grocery_store.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM cart')
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Cart cleared'})


@app.route('/api/checkout', methods=['POST'])
def checkout():
    data = request.get_json()
    customer_name = data.get('customer_name', 'Anonymous')

    conn = sqlite3.connect('grocery_store.db')
    cursor = conn.cursor()

    # Get cart items
    cursor.execute('''
        SELECT c.product_id, c.quantity, p.price
        FROM cart c
        JOIN products p ON c.product_id = p.id
    ''')
    cart_items = cursor.fetchall()

    if not cart_items:
        conn.close()
        return jsonify({'success': False, 'message': 'Cart is empty'})

    # Calculate total
    total_amount = sum(item[1] * item[2] for item in cart_items)

    # Create order
    cursor.execute(
        'INSERT INTO orders (customer_name, total_amount) VALUES (?, ?)',
        (customer_name, total_amount)
    )
    order_id = cursor.lastrowid

    # Add order items
    for product_id, quantity, price in cart_items:
        cursor.execute(
            'INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (?, ?, ?, ?)',
            (order_id, product_id, quantity, price)
        )

        # Update stock
        cursor.execute(
            'UPDATE products SET stock = stock - ? WHERE id = ?',
            (quantity, product_id)
        )

    # Clear cart
    cursor.execute('DELETE FROM cart')

    conn.commit()
    conn.close()

    return jsonify({
        'success': True,
        'message': f'Order #{order_id} placed successfully!',
        'order_id': order_id,
        'total': total_amount
    })


@app.route('/admin')
def admin():
    return render_template('admin.html')


@app.route('/api/admin/tables')
def get_tables():
    conn = sqlite3.connect('grocery_store.db')
    cursor = conn.cursor()

    tables_data = {}

    # Get products
    cursor.execute('SELECT * FROM products')
    tables_data['products'] = {
        'columns': ['ID', 'Name', 'Category', 'Price', 'Stock', 'Image URL'],
        'data': cursor.fetchall()
    }

    # Get cart
    cursor.execute('''
        SELECT c.id, p.name, c.quantity, c.added_date, p.price
        FROM cart c
        JOIN products p ON c.product_id = p.id
    ''')
    tables_data['cart'] = {
        'columns': ['Cart ID', 'Product Name', 'Quantity', 'Added Date', 'Price'],
        'data': cursor.fetchall()
    }

    # Get orders
    cursor.execute('SELECT * FROM orders ORDER BY order_date DESC')
    tables_data['orders'] = {
        'columns': ['Order ID', 'Customer Name', 'Total Amount', 'Order Date', 'Status'],
        'data': cursor.fetchall()
    }

    # Get order items
    cursor.execute('''
        SELECT oi.id, oi.order_id, p.name, oi.quantity, oi.price
        FROM order_items oi
        JOIN products p ON oi.product_id = p.id
        ORDER BY oi.order_id DESC
    ''')
    tables_data['order_items'] = {
        'columns': ['Item ID', 'Order ID', 'Product Name', 'Quantity', 'Price'],
        'data': cursor.fetchall()
    }

    conn.close()
    return jsonify(tables_data)


if __name__ == '__main__':
    # Initialize database
    init_db()

    # Create templates and static directories if they don't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)

    print("Starting Grocery Shopping Cart Application...")
    print("Visit: http://localhost:5000 for the shopping interface")
    print("Visit: http://localhost:5000/admin for database tables view")

    app.run(debug=True, port=5000)
