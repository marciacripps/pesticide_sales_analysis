import sqlite3

conn = sqlite3.connect('pesticide_sales.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT,
    product_type TEXT,  -- "Herbicide", "Fungicide", "Insecticide"
    active_ingredient TEXT,
    price REAL
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    location TEXT
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    product_id INTEGER,
    purchase_date TEXT,
    quantity INTEGER,
    total_amount REAL,
    FOREIGN KEY (customer_id) REFERENCES customers (customer_id),
    FOREIGN KEY (product_id) REFERENCES products (product_id)
);
''')

conn.commit()
conn.close()

print("Db n tables made")
