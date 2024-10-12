import sqlite3
from faker import Faker
import random

fake = Faker()
conn = sqlite3.connect('pesticide_sales.db')
cursor = conn.cursor()

products = [
    # Herbicides
    ('Roundup', 'Herbicide', 'Glyphosate'),
    ('Prowl', 'Herbicide', 'Pendimethalin'),
    ('Aatrex', 'Herbicide', 'Atrazine'),
    ('Weedone', 'Herbicide', '2,4-Dichlorophenoxyacetic acid'),
    ('XtendiMax', 'Herbicide', 'Dicamba'),
    ('Dual II Magnum', 'Herbicide', 'Metolachlor'),
    ('Treflan', 'Herbicide', 'Trifluralin'),
    ('Arsenal', 'Herbicide', 'Imazapyr'),
    ('Stinger', 'Herbicide', 'Clopyralid'),
    ('Hyvar X', 'Herbicide', 'Bromacil'),
    ('Fusilade', 'Herbicide', 'Fluazifop-P-butyl'),
    ('Select Max', 'Herbicide', 'Clethodim'),
    ('Liberty', 'Herbicide', 'Glufosinate-ammonium'),
    ('Sencor', 'Herbicide', 'Metribuzin'),
    ('Assure II', 'Herbicide', 'Quizalofop-P-ethyl'),
    ('Betasan', 'Herbicide', 'Bensulide'),
    
    # Fungicides
    ('Quadris', 'Fungicide', 'Azoxystrobin'),
    ('Banner Maxx', 'Fungicide', 'Propiconazole'),
    ('Bravo', 'Fungicide', 'Chlorothalonil'),
    ('Dithane', 'Fungicide', 'Mancozeb'),
    ('Captan', 'Fungicide', 'Captan'),
    ('Rally', 'Fungicide', 'Myclobutanil'),
    ('Inspire', 'Fungicide', 'Difenoconazole'),
    ('Luna Sensation', 'Fungicide', 'Fluopyram'),
    ('Folicur', 'Fungicide', 'Tebuconazole'),
    ('CuPRO', 'Fungicide', 'Copper Oxychloride'),
    ('Flint', 'Fungicide', 'Trifloxystrobin'),
    ('Medallion', 'Fungicide', 'Fludioxonil'),
    ('Pristine', 'Fungicide', 'Boscalid'),
    ('Headline', 'Fungicide', 'Pyraclostrobin'),
    ('Topsin M', 'Fungicide', 'Carbendazim'),
    ('Ridomil Gold', 'Fungicide', 'Metalaxyl'),
    ('Reason', 'Fungicide', 'Fenamidone'),
    
    # Insecticides
    ('Admire', 'Insecticide', 'Imidacloprid'),
    ('Talstar', 'Insecticide', 'Bifenthrin'),
    ('Entrust', 'Insecticide', 'Spinosad'),
    ('Warrior II', 'Insecticide', 'Lambda-cyhalothrin'),
    ('Fyfanon', 'Insecticide', 'Malathion'),
    ('Permethrin SFR', 'Insecticide', 'Permethrin'),
    ('Termidor', 'Insecticide', 'Fipronil'),
    ('DeltaGard', 'Insecticide', 'Deltamethrin'),
    ('Lorsban', 'Insecticide', 'Chlorpyrifos'),
    ('Sevin', 'Insecticide', 'Carbaryl'),
    ('Demon WP', 'Insecticide', 'Cypermethrin'),
    ('Avid', 'Insecticide', 'Abamectin'),
    ('Actara', 'Insecticide', 'Thiamethoxam'),
    ('Assail', 'Insecticide', 'Acetamiprid'),
    ('Lannate', 'Insecticide', 'Methomyl'),
    ('Asana XL', 'Insecticide', 'Esfenvalerate'),
    ('Radiant', 'Insecticide', 'Spinetoram'),    
    
]

for product_name, product_type, active_ingredient in products:
    cursor.execute('''
    INSERT INTO products (product_name, product_type, active_ingredient, price)
    VALUES (?, ?, ?, ?)
    ''', (product_name, product_type, active_ingredient, round(random.uniform(10, 100), 2)))

locations = ['Branch Office A', 'Branch Office B', 'Branch Office C']

for _ in range(100):
    location = random.choice(locations)
    cursor.execute('''
    INSERT INTO customers (first_name, last_name, email, location)
    VALUES (?, ?, ?, ?)
    ''', (fake.first_name(), fake.last_name(), fake.email(), location))

product_ids = [row[0] for row in cursor.execute('SELECT product_id FROM products').fetchall()]
customer_ids = [row[0] for row in cursor.execute('SELECT customer_id FROM customers').fetchall()]

for _ in range(1000): 
    product_id = random.choice(product_ids)
    customer_id = random.choice(customer_ids)
    quantity = random.randint(1, 20)
    price = cursor.execute('SELECT price FROM products WHERE product_id = ?', (product_id,)).fetchone()[0]
    total_amount = round(price * quantity, 2)
    purchase_date = fake.date_this_year()

    cursor.execute('''
    INSERT INTO transactions (customer_id, product_id, purchase_date, quantity, total_amount)
    VALUES (?, ?, ?, ?, ?)
    ''', (customer_id, product_id, purchase_date, quantity, total_amount))

conn.commit()
conn.close()

print("DB populate done")
