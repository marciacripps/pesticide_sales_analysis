from flask import Flask, render_template, send_from_directory
import sqlite3
import os

app = Flask(__name__)

# Route for the Tableau dashboard
@app.route('/')
def index():
    return render_template('index.html')

# Route for displaying top products with more detailed queries
@app.route('/top-products')
def top_products():
    conn = sqlite3.connect('data/pesticide_sales.db')
    cursor = conn.cursor()

    # Top 5 products overall by sales
    query_overall = '''
    SELECT product_name, SUM(total_amount) AS total_sales
    FROM transactions
    JOIN products ON transactions.product_id = products.product_id
    GROUP BY product_name
    ORDER BY total_sales DESC
    LIMIT 5;
    '''
    top_products_overall = cursor.execute(query_overall).fetchall()

    # Top 5 products by branch (location)
    query_by_branch = '''
    SELECT c.location, p.product_name, SUM(t.total_amount) AS total_sales
    FROM transactions t
    JOIN products p ON t.product_id = p.product_id
    JOIN customers c ON t.customer_id = c.customer_id
    GROUP BY c.location, p.product_name
    ORDER BY total_sales DESC
    LIMIT 5;
    '''
    top_products_by_branch = cursor.execute(query_by_branch).fetchall()

    # Top 5 herbicides
    query_herbicides = '''
    SELECT product_name, SUM(total_amount) AS total_sales
    FROM transactions
    JOIN products ON transactions.product_id = products.product_id
    WHERE product_type = 'Herbicide'
    GROUP BY product_name
    ORDER BY total_sales DESC
    LIMIT 5;
    '''
    top_herbicides = cursor.execute(query_herbicides).fetchall()

    # Top 5 fungicides
    query_fungicides = '''
    SELECT product_name, SUM(total_amount) AS total_sales
    FROM transactions
    JOIN products ON transactions.product_id = products.product_id
    WHERE product_type = 'Fungicide'
    GROUP BY product_name
    ORDER BY total_sales DESC
    LIMIT 5;
    '''
    top_fungicides = cursor.execute(query_fungicides).fetchall()

    # Top 5 insecticides
    query_insecticides = '''
    SELECT product_name, SUM(total_amount) AS total_sales
    FROM transactions
    JOIN products ON transactions.product_id = products.product_id
    WHERE product_type = 'Insecticide'
    GROUP BY product_name
    ORDER BY total_sales DESC
    LIMIT 5;
    '''
    top_insecticides = cursor.execute(query_insecticides).fetchall()

    conn.close()

    # Pass all the results to the template
    return render_template('top_products.html', 
                           top_products_overall=top_products_overall,
                           top_products_by_branch=top_products_by_branch,
                           top_herbicides=top_herbicides,
                           top_fungicides=top_fungicides,
                           top_insecticides=top_insecticides)

# Route to download the CSV file
@app.route('/download-product-sales')
def download_csv():
    # The static folder is where the CSV file will be stored
    csv_folder = os.path.join(app.root_path, 'static')
    return send_from_directory(csv_folder, 'product_sales.csv', as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
