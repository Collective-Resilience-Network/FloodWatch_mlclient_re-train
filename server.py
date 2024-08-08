from flask import Flask, request, jsonify
import csv

app = Flask(__name__)
CSV_FILE_PATH = 'image_labels.csv'

@app.route('/update_csv', methods=['POST'])
def update_csv():
    data = request.json
    image_id_to_remove = data['image_id']

    # Read the existing CSV data
    with open(CSV_FILE_PATH, 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)

    # Filter out the row with the specified image ID
    updated_rows = [row for row in rows if row[0] != image_id_to_remove]

    # Write the updated data back to the CSV
    with open(CSV_FILE_PATH, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(updated_rows)

    return jsonify({'message': 'CSV updated successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)  # Use port 8000
