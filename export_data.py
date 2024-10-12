import sqlite3
import pandas as pd
import os

os.makedirs('data', exist_ok=True)

conn = sqlite3.connect('pesticide_sales.db')

queries = {
    "product_sales": '''
        SELECT product_name, product_type, SUM(total_amount) AS total_sales
        FROM transactions
        JOIN products ON transactions.product_id = products.product_id
        GROUP BY product_name, product_type
        ORDER BY total_sales DESC;
    ''',
    "top_customers": '''
        SELECT c.first_name || ' ' || c.last_name AS customer_name, SUM(t.total_amount) AS total_purchases
        FROM transactions t
        JOIN customers c ON t.customer_id = c.customer_id
        GROUP BY customer_name
        ORDER BY total_purchases DESC;
    ''',
    "sales_trends": '''
        SELECT strftime('%Y-%m', t.purchase_date) AS month, p.product_type, SUM(t.total_amount) AS monthly_sales
        FROM transactions t
        JOIN products p ON t.product_id = p.product_id
        GROUP BY month, p.product_type
        ORDER BY month, p.product_type;
    ''',
    "herbicide_sales_by_location": '''
        SELECT c.location, SUM(t.total_amount) AS total_herbicide_sales
        FROM transactions t
        JOIN products p ON t.product_id = p.product_id
        JOIN customers c ON t.customer_id = c.customer_id
        WHERE p.product_type = 'Herbicide'
        GROUP BY c.location
        ORDER BY total_herbicide_sales DESC;
    '''
}

for name, query in queries.items():
    df = pd.read_sql_query(query, conn)
    df.to_csv(f'data/{name}.csv', index=False)
    print(f"Exported data/{name}.csv")

conn.close()
