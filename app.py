from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
import os

app = Flask(__name__)

# Initialize an empty DataFrame for expenses
expenses = pd.DataFrame(columns=['Date', 'Category', 'Description', 'Amount'])

@app.route('/')
def index():
    """Render the main HTML page."""
    return render_template('index.html')

@app.route('/add_expense', methods=['POST'])
def add_expense():
    """Add an expense to the DataFrame and return the updated table."""
    global expenses
    data = request.json
    try:
        # Validate and add the expense
        new_expense = pd.DataFrame({
            'Date': [pd.to_datetime(data['date'])],
            'Category': [data['category']],
            'Description': [data['description']],
            'Amount': [float(data['amount'])]
        })
        expenses = pd.concat([expenses, new_expense], ignore_index=True)

        # Convert the updated DataFrame to JSON
        return expenses.to_json(orient='records')
    except Exception as e:
        return jsonify({'error': f"Error: {e}"}), 400

@app.route('/save_to_csv', methods=['GET'])
def save_to_csv():
    """Save the expenses DataFrame to a CSV file and send it for download."""
    global expenses
    try:
        if expenses.empty:
            return jsonify({'error': 'No expenses to save!'}), 400
        
        # Format the Date column to a proper string format
        expenses['Date'] = expenses['Date'].dt.strftime('%Y-%m-%d')
        
        # Save to CSV
        file_path = 'expenses.csv'
        expenses.to_csv(file_path, index=False)

        # Send the file as a downloadable response
        return send_file(file_path, as_attachment=True)

    except Exception as e:
        return jsonify({'error': f"Error: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True)