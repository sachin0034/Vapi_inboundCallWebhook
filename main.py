from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# Load and prepare CSV data
csv_path = 'CallerDataReal.csv'
df = pd.read_csv(csv_path)

# Normalize phone numbers function
def normalize_phone_number(phone_number):
    # Remove country code (assumes country code starts with '+')
    return phone_number.lstrip('+')[1:]

# Convert DataFrame to a dictionary for faster lookups
data = {}
for index, row in df.iterrows():
    normalized_number = normalize_phone_number(str(row['Customer Number']))
    data[normalized_number] = row

@app.route('/incoming_call', methods=['POST'])
def handle_incoming_call():
    call_data = request.json
    incoming_number = call_data.get('caller_number')  # Extract caller number from the Vapi request
    normalized_number = normalize_phone_number(incoming_number)
    
    if normalized_number in data:
        user_info = data[normalized_number]
        response_message = f"Hello {user_info['FirstName']} {user_info['LastName']}, how can I assist you today?"
        # Here you can add more logic to handle specific queries
    else:
        response_message = "Hello, how can I assist you today?"

    # Send response back to Vapi
    return jsonify({"message": response_message})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

