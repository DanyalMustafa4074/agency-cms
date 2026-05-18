from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os
from datetime import date

app = Flask(__name__)
CORS(app)

def get_db():
    return psycopg2.connect(
        host=os.environ.get('DB_HOST', 'db'),
        database=os.environ.get('DB_NAME', 'agencydb'),
        user=os.environ.get('DB_USER', 'admin'),
        password=os.environ.get('DB_PASS', 'admin123')
    )

def init_db():
    conn = get_db()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS clients (
                 id SERIAL PRIMARY KEY,
                 name TEXT NOT NULL,
                 contact TEXT NOT NULL,
                 service TEXT NOT NULL,
                 status TEXT NOT NULL,
                 fee INTEGER NOT NULL,
                 added TEXT NOT NULL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS invoices (
                 id SERIAL PRIMARY KEY,
                 inv_id TEXT NOT NULL,
                 client TEXT NOT NULL,
                 description TEXT NOT NULL,
                 amount INTEGER NOT NULL,
                 status TEXT NOT NULL,
                 due_date TEXT,
                 created TEXT NOT NULL)''')
    conn.commit()
    conn.close()

@app.route('/health')
def health():
    return jsonify({'status': 'ok'})

@app.route('/clients', methods=['GET'])
def get_clients():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM clients")
    rows = [dict(id=r[0], name=r[1], contact=r[2], service=r[3],
                 status=r[4], fee=r[5], added=r[6]) for r in c.fetchall()]
    conn.close()
    return jsonify(rows)

@app.route('/clients', methods=['POST'])
def add_client():
    d = request.json
    added = date.today().strftime('%d %b %Y')
    conn = get_db()
    c = conn.cursor()
    c.execute("INSERT INTO clients (name,contact,service,status,fee,added) VALUES (%s,%s,%s,%s,%s,%s)",
              (d['name'], d['contact'], d['service'], d['status'], d['fee'], added))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Client added successfully!'})

@app.route('/clients/<int:cid>', methods=['DELETE'])
def delete_client(cid):
    conn = get_db()
    c = conn.cursor()
    c.execute("DELETE FROM clients WHERE id=%s", (cid,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Client removed!'})

@app.route('/invoices', methods=['GET'])
def get_invoices():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM invoices")
    rows = [dict(id=r[0], inv_id=r[1], client=r[2], description=r[3],
                 amount=r[4], status=r[5], due_date=r[6], created=r[7]) for r in c.fetchall()]
    conn.close()
    return jsonify(rows)

@app.route('/invoices', methods=['POST'])
def add_invoice():
    d = request.json
    created = date.today().strftime('%d %b %Y')
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM invoices")
    count = c.fetchone()[0] + 1
    inv_id = f"INV-{str(count).zfill(4)}"
    c.execute("INSERT INTO invoices (inv_id,client,description,amount,status,due_date,created) VALUES (%s,%s,%s,%s,%s,%s,%s)",
              (inv_id, d['client'], d['description'], d['amount'], d['status'], d.get('due_date','—'), created))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Invoice created successfully!'})

@app.route('/invoices/<int:iid>', methods=['DELETE'])
def delete_invoice(iid):
    conn = get_db()
    c = conn.cursor()
    c.execute("DELETE FROM invoices WHERE id=%s", (iid,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Invoice deleted!'})

@app.route('/invoices/<int:iid>/status', methods=['PATCH'])
def toggle_status(iid):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT status FROM invoices WHERE id=%s", (iid,))
    row = c.fetchone()
    if not row:
        conn.close()
        return jsonify({'error': 'Not found'}), 404
    cycle = {'Unpaid': 'Paid', 'Paid': 'Pending', 'Pending': 'Unpaid'}
    new_status = cycle.get(row[0], 'Unpaid')
    c.execute("UPDATE invoices SET status=%s WHERE id=%s", (new_status, iid))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Status updated!', 'status': new_status})

if __name__ == '__main__':
    import time
    for i in range(10):
        try:
            init_db()
            print("Database connected!")
            break
        except Exception as e:
            print(f"Waiting for database... ({i+1}/10)")
            time.sleep(3)
    app.run(host='0.0.0.0', port=5000, debug=True)