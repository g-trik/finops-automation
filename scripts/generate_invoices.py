"""
Generates 12 PDF invoices covering all validation scenarios.
"""
 
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas
import os
 
OUTPUT_DIR = "../samples/invoices"
os.makedirs(OUTPUT_DIR, exist_ok=True)
 
 
def create_invoice(filename, vendor, invoice_number, invoice_date,
                   due_date, currency, subtotal, vat, total,
                   bill_to="ING Bank N.V.\nAccounts Payable\nBijlmerplein 888\n1102 MG Amsterdam",
                   note=""):
    path = os.path.join(OUTPUT_DIR, filename)
    c = canvas.Canvas(path, pagesize=A4)
    width, height = A4
 
    # Vendor info
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 50, vendor)
    c.setFont("Helvetica", 10)
    c.drawString(50, height - 65, "Herengracht 182")
    c.drawString(50, height - 80, "1016 BR Amsterdam")
    c.drawString(50, height - 95, "Netherlands")
    c.drawString(50, height - 110, "VAT: NL859234567B01")
 
    # INVOICE title
    c.setFont("Helvetica-Bold", 24)
    c.drawRightString(width - 50, height - 50, "INVOICE")
 
    # Bill To
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, height - 145, "Bill To:")
    c.setFont("Helvetica", 10)
    y = height - 160
    for line in bill_to.split("\n"):
        c.drawString(50, y, line)
        y -= 15
 
    # Invoice details
    c.drawString(350, height - 145, f"Invoice Number: {invoice_number}")
    c.drawString(350, height - 160, f"Invoice Date: {invoice_date}")
    c.drawString(350, height - 175, f"Due Date: {due_date}")
    c.drawString(350, height - 190, f"Currency: {currency}")
 
    # Test note
    if note:
        c.setFont("Helvetica-Oblique", 9)
        c.drawString(50, height - 215, f"■ TEST NOTE: {note}")
 
    # Divider
    c.setStrokeColor(colors.black)
    c.setLineWidth(0.5)
    c.line(50, height - 225, width - 50, height - 225)
 
    # Table header
    y = height - 245
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "#")
    c.drawString(80, y, "Description")
    c.drawString(330, y, "Qty")
    c.drawString(370, y, "Unit Price")
    c.drawRightString(width - 50, y, "Total")
    c.line(50, y - 5, width - 50, y - 5)
 
    # Single line item
    y -= 22
    c.setFont("Helvetica", 10)
    c.drawString(50, y, "1")
    c.drawString(80, y, "Professional Services")
    c.drawString(330, y, "1")
    c.drawString(370, y, f"{currency} {subtotal:,.2f}")
    c.drawRightString(width - 50, y, f"{currency} {subtotal:,.2f}")
 
    # Totals
    y -= 35
    c.line(50, y + 10, width - 50, y + 10)
    c.setFont("Helvetica", 10)
    c.drawRightString(width - 120, y, "Subtotal:")
    c.drawRightString(width - 50, y, f"{currency} {subtotal:,.2f}")
    y -= 18
    c.drawRightString(width - 120, y, "VAT (21%):")
    c.drawRightString(width - 50, y, f"{currency} {vat:,.2f}")
    y -= 18
    c.setFont("Helvetica-Bold", 11)
    c.drawRightString(width - 120, y, "TOTAL DUE:")
    c.drawRightString(width - 50, y, f"{currency} {total:,.2f}")
 
    # Payment details
    y -= 50
    c.setFont("Helvetica", 9)
    c.drawString(50, y, f"Bank: ABN AMRO | IBAN: NL91 ABNA 0417 1643 00 | BIC: ABNANL2A")
    y -= 15
    c.drawString(50, y, f"Reference: {invoice_number} | Payment terms: Net 30 days")
 
    c.save()
    print(f"✓ {filename}")
 
 
# SCENARIO 1 — Clean, normal invoice under threshold
create_invoice(
    filename="01_clean_normal_5000.pdf",
    vendor="DataSync Solutions B.V.",
    invoice_number="INV-2026-00100",
    invoice_date="20 March 2026",
    due_date="19 April 2026",
    currency="EUR",
    subtotal=4132.23,
    vat=867.77,
    total=5000.00,
    note="EXPECTED: CLEAN — normal invoice under threshold"
)
 
# SCENARIO 2 — High value invoice > €10,000
create_invoice(
    filename="02_flagged_high_value_15000.pdf",
    vendor="Enterprise Cloud GmbH",
    invoice_number="INV-2026-00200",
    invoice_date="21 March 2026",
    due_date="20 April 2026",
    currency="EUR",
    subtotal=12396.69,
    vat=2603.31,
    total=15000.00,
    note="EXPECTED: FLAGGED — high value > €10,000"
)
 
# SCENARIO 3 — Past due date
create_invoice(
    filename="03_flagged_past_due_date.pdf",
    vendor="RetroTech Systems N.V.",
    invoice_number="INV-2026-00300",
    invoice_date="01 January 2026",
    due_date="31 January 2026",
    currency="EUR",
    subtotal=2644.63,
    vat=555.37,
    total=3200.00,
    note="EXPECTED: FLAGGED — due date 31 Jan 2026 is in the past"
)
 
# SCENARIO 4 — Missing vendor name
create_invoice(
    filename="04_flagged_missing_vendor.pdf",
    vendor="",
    invoice_number="INV-2026-00400",
    invoice_date="23 March 2026",
    due_date="22 April 2026",
    currency="EUR",
    subtotal=1487.60,
    vat=312.40,
    total=1800.00,
    note="EXPECTED: FLAGGED — missing vendor name"
)
 
# SCENARIO 5 — Unsupported currency JPY (high value)
create_invoice(
    filename="05_flagged_currency_jpy.pdf",
    vendor="Sakura Digital K.K.",
    invoice_number="INV-2026-00500",
    invoice_date="23 March 2026",
    due_date="22 April 2026",
    currency="JPY",
    subtotal=850000.00,
    vat=0.00,
    total=850000.00,
    note="EXPECTED: FLAGGED — unsupported currency JPY + high value"
)
 
# SCENARIO 6 — Zero amount
create_invoice(
    filename="06_flagged_zero_amount.pdf",
    vendor="NullValue Corp B.V.",
    invoice_number="INV-2026-00600",
    invoice_date="23 March 2026",
    due_date="22 April 2026",
    currency="EUR",
    subtotal=0.00,
    vat=0.00,
    total=0.00,
    note="EXPECTED: FLAGGED — zero amount invoice"
)
 
# SCENARIO 7 — Multiple flags (high value + past due + JPY)
create_invoice(
    filename="07_flagged_multiple_flags.pdf",
    vendor="BadData Inc.",
    invoice_number="INV-2026-00700",
    invoice_date="01 December 2025",
    due_date="01 January 2026",
    currency="JPY",
    subtotal=25000.00,
    vat=0.00,
    total=25000.00,
    note="EXPECTED: FLAGGED — high value + past due + JPY"
)
 
# SCENARIO 8 — Duplicate invoice number (same as scenario 1)
create_invoice(
    filename="08_flagged_duplicate_invoice_number.pdf",
    vendor="DataSync Solutions B.V.",
    invoice_number="INV-2026-00100",
    invoice_date="22 March 2026",
    due_date="21 April 2026",
    currency="EUR",
    subtotal=4132.23,
    vat=867.77,
    total=5000.00,
    note="EXPECTED: FLAGGED — duplicate of INV-2026-00100"
)
 
# SCENARIO 9 — VAT mismatch
create_invoice(
    filename="09_flagged_vat_mismatch.pdf",
    vendor="TechSpark Solutions B.V.",
    invoice_number="INV-2026-00900",
    invoice_date="25 March 2026",
    due_date="25 May 2026",
    currency="EUR",
    subtotal=6000.00,
    vat=500.00,        # wrong — should be 1260.00
    total=6500.00,
    note="EXPECTED: FLAGGED — VAT mismatch (declared 500, expected ~1128)"
)
 
# SCENARIO 10 — Scanned image only (no text extractable)
# This is a blank PDF simulating a scanned document
path = os.path.join(OUTPUT_DIR, "10_scanned_image_only.pdf")
c = canvas.Canvas(path, pagesize=A4)
c.setFont("Helvetica", 10)
c.drawString(50, 400, "[This page intentionally contains no machine-readable text]")
c.save()
print("✓ 10_scanned_image_only.pdf")
 
# SCENARIO 11 — Non-invoice document (contract)
path = os.path.join(OUTPUT_DIR, "11_non_invoice_contract.pdf")
c = canvas.Canvas(path, pagesize=A4)
width, height = A4
c.setFont("Helvetica-Bold", 18)
c.drawCentredString(width / 2, height - 100, "SERVICE AGREEMENT")
c.setFont("Helvetica", 11)
c.drawString(50, height - 150, "This Service Agreement is entered into as of 1 March 2026")
c.drawString(50, height - 170, "between Bright Future B.V. and ING Bank N.V.")
c.drawString(50, height - 200, "This is a contract, not an invoice.")
c.save()
print("✓ 11_non_invoice_contract.pdf")
 
# SCENARIO 12 — Clean valid invoice (correct VAT, future due date)
create_invoice(
    filename="12_clean_valid_invoice.pdf",
    vendor="Bright Future B.V.",
    invoice_number="INV-2026-00800",
    invoice_date="15 March 2026",
    due_date="20 June 2026",
    currency="EUR",
    subtotal=4750.00,
    vat=997.50,
    total=5747.50,
    note="EXPECTED: CLEAN — all fields valid, correct VAT, future due date"
)
 
print(f"\n✅ All 12 invoices generated in ./{OUTPUT_DIR}/")
print("\nScenarios covered:")
print("  01 — Clean normal invoice")
print("  02 — High value > €10,000")
print("  03 — Past due date")
print("  04 — Missing vendor name")
print("  05 — Unsupported currency (JPY) + high value")
print("  06 — Zero amount")
print("  07 — Multiple flags")
print("  08 — Duplicate invoice number")
print("  09 — VAT mismatch")
print("  10 — Scanned image (no extractable text)")
print("  11 — Non-invoice document (contract)")
print("  12 — Clean valid invoice")