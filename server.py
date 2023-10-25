from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Database configuration
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="0511",
    database="db_inventory"
)
cursor = db.cursor()

@app.route('/api/qr_data', methods=['GET'])
def get_qr_data():
    try:
        cursor.execute("SELECT * FROM tbl_lib")
        result = cursor.fetchall()
        qr_values = [a[1] for a in result]
        return jsonify(qr_values)
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)})

if __name__ == '__main__':
    app.run(debug=True)
