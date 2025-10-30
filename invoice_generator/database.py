import sqlite3

# Create tables if they don't exist
def create_tables():
    conn = sqlite3.connect("invoices.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS invoices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT,
            address TEXT,
            city TEXT,
            gst_number TEXT,
            date TEXT,
            contact TEXT,
            customer_name TEXT,
            authorized_signatory TEXT,
            logo_path TEXT
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_id INTEGER,
            item_name TEXT,
            price REAL,
            quantity REAL,
            total_price REAL,
            FOREIGN KEY (invoice_id) REFERENCES invoices(id)
        )
    """)
    
    conn.commit()
    conn.close()

# Insert invoice and its items
def insert_invoice(company_name, address, city, gst_number, date, contact, customer_name, authorized_signatory, logo_path, items):
    conn = sqlite3.connect("invoices.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO invoices (company_name, address, city, gst_number, date, contact, customer_name, authorized_signatory, logo_path)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (company_name, address, city, gst_number, date, contact, customer_name, authorized_signatory, logo_path))
    
    invoice_id = cursor.lastrowid
    
    for item in items:
        item_name, price, quantity = item
        total_price = float(price) * float(quantity)
        cursor.execute("""
            INSERT INTO items (invoice_id, item_name, price, quantity, total_price)
            VALUES (?, ?, ?, ?, ?)
        """, (invoice_id, item_name, price, quantity, total_price))
    
    conn.commit()
    conn.close()
    
    return invoice_id

# Initialize tables on first run
if __name__ == "__main__":
    create_tables()
