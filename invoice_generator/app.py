import os
import re
from flask import Flask, render_template, request, send_file, flash, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime

from database import insert_invoice, create_tables
from invoice_generator import generate_invoice

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Set this securely in production

os.makedirs("static/invoices", exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        company_name = request.form.get("company_name")
        address = request.form.get("address")
        city = request.form.get("city")
        gst_number = request.form.get("gst_number")
        contact = request.form.get("contact")
        customer_name = request.form.get("customer_name")
        authorized_signatory = request.form.get("authorized_signatory")
        logo = request.files.get("logo")

        # Validate inputs
        if not re.fullmatch(r"[6-9]\d{9}", contact):
            flash("Invalid contact number. It must be 10 digits starting with 6-9.")
            return redirect(url_for("home"))
        if not re.fullmatch(r"\d{2}[A-Z]{5}\d{4}[A-Z]{1}[A-Z\d]{1}Z[A-Z\d]{1}", gst_number):
            flash("Invalid GST number format.")
            return redirect(url_for("home"))

        # Handle logo upload
        logo_path = ""
        if logo and logo.filename:
            filename = secure_filename(logo.filename)
            logo_path = os.path.join("static", filename)
            logo.save(logo_path)

        # Parse items
        try:
            item_names = request.form.getlist("item_name[]")
            prices = list(map(float, request.form.getlist("price[]")))
            quantities = list(map(float, request.form.getlist("quantity[]")))
            items = list(zip(item_names, prices, quantities))
        except ValueError:
            flash("Invalid price or quantity format in items.")
            return redirect(url_for("home"))

        # Get current datetime
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Save to DB and generate PDF
        invoice_id = insert_invoice(company_name, address, city, gst_number, date_time, contact,
                                    customer_name, authorized_signatory, logo_path, items)
        pdf_path = generate_invoice(invoice_id, company_name, address, city, gst_number, date_time,
                                    contact, customer_name, authorized_signatory, logo_path, items)

        return send_file(pdf_path, as_attachment=True)

    return render_template("index.html")

if __name__ == "__main__":
    create_tables()
    app.run(debug=True)
