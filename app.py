from flask import Flask, render_template, request, jsonify
import pandas as pd
import json

app = Flask(__name__)

# Sample Data Load
def load_data():
    try:
        return pd.read_csv('sales_data.csv')
    except:
        # Fallback dummy data agar CSV na mile
        data = {
            'Date': ['2026-01-05', '2026-01-08', '2026-01-12', '2026-02-10', '2026-02-15'],
            'Product': ['Laptop', 'Chair', 'Shirt', 'Smartphone', 'Desk'],
            'Category': ['Electronics', 'Furniture', 'Clothing', 'Electronics', 'Furniture'],
            'Region': ['West', 'North', 'South', 'East', 'North'],
            'Sales': [65000, 15000, 12000, 45000, 22000],
            'Quantity': [5, 10, 20, 3, 4],
            'Profit': [10000, 3500, 3000, 8000, 4500],
            'Salesperson': ['Priya', 'Rahul', 'Sneha', 'Amit', 'Rahul'],
            'Customer': ['TechCorp', 'Urban Living', 'FashionHub', 'RetailPlus', 'Metro Space']
        }
        df = pd.DataFrame(data)
        df.to_csv('sales_data.csv', index=False)
        return df

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/data', methods=['GET'])
def get_data():
    df = load_data()
    return jsonify(df.to_dict(orient='records'))

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and file.filename.endswith('.csv'):
        df = pd.read_csv(file)
        df.to_csv('sales_data.csv', index=False)
        return jsonify({'message': 'File uploaded successfully', 'rows': len(df)})
    return jsonify({'error': 'Only CSV files supported'}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)