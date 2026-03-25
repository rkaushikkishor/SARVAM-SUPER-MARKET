from flask import Flask, jsonify, request
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

# Load product database
with open("products.json") as f:
    products = json.load(f)

orders = []
revenue = 0

# Get product by barcode
@app.route("/product/<barcode>")
def get_product(barcode):
    if barcode in products:
        return jsonify(products[barcode])
    return jsonify({"error": "Product not found"}), 404


# Save order
@app.route("/order", methods=["POST"])
def save_order():
    global revenue
    data = request.json
    orders.append(data)
    revenue += data["total"]

    return jsonify({
        "message": "Order saved",
        "orders": len(orders),
        "revenue": revenue
    })


# Analytics
@app.route("/analytics")
def analytics():
    return jsonify({
        "orders": len(orders),
        "revenue": revenue
    })


app.run(debug=True)