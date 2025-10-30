import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

os.makedirs("static/invoices", exist_ok=True)

def generate_invoice(invoice_id, company_name, address, city, gst_number, date_time,
                     contact, customer_name, authorized_signatory, logo_path, items):
    file_path = f"static/invoices/{customer_name}_invoice_{invoice_id}.pdf"
    c = canvas.Canvas(file_path, pagesize=letter)

    # Company info and logo
    c.setFont("Helvetica-Bold", 16)
    if logo_path and os.path.exists(logo_path):
        c.drawImage(logo_path, 40, 700, width=100, height=50)

    c.drawString(150, 750, company_name)
    c.setFont("Helvetica", 12)
    c.drawString(150, 730, f"{address}, {city}")
    c.drawString(150, 710, f"GST No: {gst_number}")

    # Invoice info
    c.drawString(40, 680, f"Invoice ID: {invoice_id}")
    c.drawString(40, 660, f"Date & Time: {date_time}")
    c.drawString(40, 640, f"Customer Name: {customer_name}")
    c.drawString(40, 620, f"Contact: {contact}")

    # Table headers
    y = 580
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, y, "Item Name")
    c.drawString(200, y, "Price")
    c.drawString(320, y, "Quantity")
    c.drawString(450, y, "Total Price")
    c.line(40, y - 10, 550, y - 10)

    total = 0
    c.setFont("Helvetica", 12)
    for item in items:
        y -= 30
        item_name, price, qty = item
        total_price = price * qty
        total += total_price
        c.drawString(40, y, item_name)
        c.drawString(200, y, f"Rs. {price:.2f}")
        c.drawString(320, y, f"{qty}")
        c.drawString(450, y, f"Rs. {total_price:.2f}")

    # Summary
    gst = total * 0.05
    grand_total = total + gst
    y -= 30
    c.line(40, y, 550, y)
    y -= 20
    c.setFont("Helvetica-Bold", 12)
    c.drawString(320, y, "Subtotal:")
    c.drawString(450, y, f"Rs. {total:.2f}")
    y -= 20
    c.drawString(320, y, "GST (5%):")
    c.drawString(450, y, f"Rs. {gst:.2f}")
    y -= 20
    c.setFont("Helvetica-Bold", 14)
    c.drawString(320, y, "Total Bill:")
    c.drawString(450, y, f"Rs. {grand_total:.2f}")

    # Signatory
    c.setFont("Helvetica", 12)
    c.drawString(400, 150, f"Authorized Signatory: {authorized_signatory}")

    c.save()
    return file_path
