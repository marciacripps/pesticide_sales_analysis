from flask import Flask, render_template, send_from_directory, abort
import sqlite3
import os

app = Flask(__name__)

DATABASE = 'data/pesticide_sales.db'


def get_db_connection():
    try:
        conn = sqlite3.connect(DATABASE)
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to the database: {e}")
        abort(500)  


@app.route('/')
def index():
    return render_template('index.html')



@app.route('/download-product-sales')
def download_csv():
    csv_folder = os.path.join(app.root_path, 'static')
    try:
        return send_from_directory(csv_folder, 'product_sales.csv', as_attachment=True)
    except FileNotFoundError:
        print("CSV file not found.")
        abort(404)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
