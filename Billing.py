from datetime import datetime
import re
from fpdf import FPDF

def show_items():
    return '''
1. Rice = 50 Rs/kg        2. Sugar = 20 Rs/kg       3. Salt = 10 Rs/kg
4. Chilli = 45 Rs/kg      5. Onions = 25 Rs/kg      6. Garlic = 30 Rs/kg
7. Tamarind = 50 Rs/kg    8. Colgate = 70 Rs/pack   9. Soaps = 15 Rs/pack
10. Shampoo = 5 Rs/pack   11. Biscuits = 15 Rs/pack 12. Boost = 150 Rs/pack
13. Oil = 250 Rs/ltr      14. Tea Powder = 70 Rs/pack 15. Dal = 100 Rs/kg
16. Bread = 40 Rs/loaf    17. Milk = 60 Rs/ltr      18. Eggs = 6 Rs/pcs
19. Butter = 550 Rs/kg    20. Cheese = 600 Rs/kg    21. Detergent = 120 Rs/pack
22. Floor Cleaner = 90 Rs/bottle     23. Face Cream = 85 Rs/tube
24. Hair Oil = 110 Rs/bottle        25. Toothbrush = 25 Rs/pcs
26. Notebook = 30 Rs/pcs           27. Pen = 10 Rs/pcs
28. Mosquito Coil = 35 Rs/pack     29. Water Bottle = 20 Rs/ltr
30. Cold Drink = 40 Rs/bottle      31. Chips = 20 Rs/pack
32. Maggie = 15 Rs/pack            33. Cornflakes = 180 Rs/box
34. Ghee = 500 Rs/kg               35. Ice Cream = 60 Rs/cup
36. Tomato Ketchup = 90 Rs/bottle 37. Pickles = 60 Rs/bottle
38. Panner = 80 Rs/kg              39. Curd = 30 Rs/cup
40. Lemon = 5 Rs/pcs
'''

def get_item_data():
    return {
        'Rice': 50, 'Sugar': 20, 'Salt': 10, 'Chilli': 45, 'Onions': 25, 'Garlic': 30,
        'Tamarind': 50, 'Colgate': 70, 'Soaps': 15, 'Shampoo': 5, 'Biscuits': 15,
        'Boost': 150, 'Oil': 250, 'Tea Powder': 70, 'Dal': 100, 'Bread': 40, 'Milk': 60,
        'Eggs': 6, 'Butter': 550, 'Cheese': 600, 'Detergent': 120, 'Floor Cleaner': 90,
        'Face Cream': 85, 'Hair Oil': 110, 'Toothbrush': 25, 'Notebook': 30, 'Pen': 10,
        'Mosquito Coil': 35, 'Water Bottle': 20, 'Cold Drink': 40, 'Chips': 20,
        'Maggie': 15, 'Cornflakes': 180, 'Ghee': 500, 'Ice Cream': 60,
        'Tomato Ketchup': 90, 'Pickles': 60, 'Panner': 80, 'Curd': 30, 'Lemon': 5
    }

def get_unit_conversions():
    return {
        'kg': 1, 'g': 0.001, 'ltr': 1, 'liter': 1, 'ml': 0.001,
        'pack': 1, 'bottle': 1, 'each': 1, 'cup': 1, 'loaf': 1,
        'tube': 1, 'box': 1, 'egg': 1, 'pcs': 1, 'piece': 1
    }

def parse_quantity_input(raw_input, unit_types):
    match = re.match(r'(\d+(?:\.\d+)?)\s*([a-zA-Z]+)', raw_input)
    if match:
        qty_val = float(match.group(1))
        unit = match.group(2).lower()
        if unit in unit_types:
            return qty_val, unit, qty_val * unit_types[unit]
    return None, None, None

def generate_pdf_receipt(name, phone, now, items, total, gst, final_total):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "SM Super Market", ln=True, align='C')
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 8, "SRI CITY", ln=True, align='C')
    pdf.cell(0, 8, "-" * 60, ln=True)
    pdf.cell(0, 8, f"Customer Name : {name}", ln=True)
    pdf.cell(0, 8, f"Phone Number  : {phone}", ln=True)
    pdf.cell(0, 8, f"Date & Time   : {now}", ln=True)
    pdf.cell(0, 8, "-" * 60, ln=True)

    pdf.set_font("Arial", 'B', 12)
    pdf.cell(10, 10, "No", 1)
    pdf.cell(50, 10, "Item", 1)
    pdf.cell(40, 10, "Quantity", 1)
    pdf.cell(40, 10, "Rate", 1)
    pdf.cell(40, 10, "Total", 1, ln=True)

    pdf.set_font("Arial", '', 12)
    for i, (item, qty, rate, price) in enumerate(items, 1):
        pdf.cell(10, 10, str(i), 1)
        pdf.cell(50, 10, item, 1)
        pdf.cell(40, 10, qty, 1)
        pdf.cell(40, 10, f"Rs {rate}", 1)
        pdf.cell(40, 10, f"Rs {price:.2f}", 1, ln=True)

    pdf.cell(0, 8, "-" * 60, ln=True)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(140, 10, "Subtotal", 0)
    pdf.cell(0, 10, f"Rs {total:.2f}", ln=True)
    pdf.cell(140, 10, "GST (18%)", 0)
    pdf.cell(0, 10, f"Rs {gst:.2f}", ln=True)
    pdf.cell(140, 10, "Total Amount", 0)
    pdf.cell(0, 10, f"Rs {final_total:.2f}", ln=True)
    pdf.cell(0, 10, "-" * 60, ln=True)
    pdf.set_font("Arial", 'I', 12)
    pdf.cell(0, 10, "Thank you for shopping with us!", ln=True, align='C')
    pdf.output("receipt.pdf")

def main():
    name = input("Enter your name: ").strip()
    if not name:
        print("❌ Name cannot be empty.")
        return

    if input("To view the item list, press 1: ").strip() == '1':
        print(show_items())

    items_data = get_item_data()
    unit_types = get_unit_conversions()
    cart = []
    total_price = 0

    while True:
        item = input("Enter your item: ").strip().title()
        if item not in items_data:
            print("❌ Invalid item. Please check the spelling or list.")
            continue

        while True:
            qty_input = input("Enter the quantity (e.g., 2 kg, 500 ml): ").strip().lower()
            qty_val, unit, qty_converted = parse_quantity_input(qty_input, unit_types)
            if qty_converted is not None:
                break
            print("❌ Invalid quantity or unit. Please try again.")

        price = qty_converted * items_data[item]
        cart.append((item, f"{qty_val} {unit}", items_data[item], price))
        total_price += price

        if input("Add more items? (yes/no): ").strip().lower() != "yes":
            break

    phone = "Not Provided"
    if input("Do you want to enter your phone number? (yes/no): ").strip().lower() == "yes":
        phone_input = input("Enter your phone number (10 digits): ").strip()
        if re.match(r'^\d{10}$', phone_input):
            phone = phone_input
        else:
            print("⚠️ Invalid phone number. Skipping.")

    if input("Can I bill the items now? (yes/no): ").strip().lower() == "yes":
        now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        gst = total_price * 0.18
        final_total = total_price + gst

        print("\n" + "=" * 25 + " SM Super Market " + "=" * 25)
        print(" " * 30 + "SRI CITY")
        print(f"Name: {name:<30} Date: {now}")
        print(f"Phone Number: {phone}")
        print("-" * 80)
        print("S.No   Item                Quantity        Price")
        print("-" * 80)
        for i, (item, qty, _, cost) in enumerate(cart, 1):
            print(f"{i:<6} {item:<20} {qty:<15} Rs {cost:.2f}")
        print("-" * 80)
        print("Subtotal".ljust(65), f"Rs {total_price:.2f}")
        print("GST (18%)".ljust(65), f"Rs {gst:.2f}")
        print("Total Amount".ljust(65), f"Rs {final_total:.2f}")
        print("-" * 80)
        print(" " * 20 + "Thank you for visiting <----> Visit Again!")
        print("-" * 80)

        generate_pdf_receipt(name, phone, now, cart, total_price, gst, final_total)
        print("📄 Receipt generated as 'receipt.pdf'!")

if __name__ == "__main__":
    main()