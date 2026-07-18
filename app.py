from flask import Flask, jsonify, request
from inventory import Inventory
from api import InventoryAPI

app = Flask(__name__)

# Single global instance shares array state across all inbound threads
api = InventoryAPI(Inventory)

@app.route("/", methods=["GET"])
def welcome():
    # Base status heartbeat probe for frontend container health checks
    return jsonify({"message": "Welcome to the Inventory Management API"}), 200

@app.route("/inventory", methods=["GET"])
def get_items():
    # Dumps complete memory register array straight to the client serializer
    return jsonify(api.get_all_items()), 200

@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_item(item_id):
    # Lookup target record reference pointer matching url parameter id
    item = api.get_item(item_id)
    if not item:
        # Prevent client json parser engines from reading empty object blobs
        return jsonify({"error": "Target item registry not found"}), 404
    return jsonify(item), 200

@app.route("/inventory", methods=["POST"])
def add_item():
    # Fallback to empty dictionary prevents json attribute access exception crashes
    data = request.get_json() or {}
    if "name" not in data or "quantity" not in data:
        # Explicit validation ensures core entity constraints are strictly fulfilled
        return jsonify({"error": "Missing critical parameters: name and quantity are required"}), 400
    
    # Map raw client payload directly into class construction parameters
    item = api.create_item(
        name=data.get("name"),
        quantity=data.get("quantity"),
        price=data.get("price", 0.0),
        barcode=data.get("barcode"),
        brand=data.get("brand"),
        ingredients=data.get("ingredients")
    )
    return jsonify(item), 201

@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def update_item(item_id):
    # Capture dynamic slice of changed properties without resetting missing attributes
    updates = request.get_json() or {}
    item = api.update_item(item_id, updates)
    if not item:
        # Trap invalid id targets gracefully before data mutation triggers run
        return jsonify({"error": "Modification block: Target item does not exist"}), 404
    return jsonify(item), 200

@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    # Evict target array dictionary pointer out of runtime instance stack
    item = api.delete_item(item_id)
    if not item:
        return jsonify({"error": "Deletion block: Target item does not exist"}), 404
    return jsonify(item), 200

@app.route("/search/<string:barcode>", methods=["GET"])
def search_barcode(barcode):
    # Scan internal memory tracking lists first to see if item already exists locally
    local_items = api.get_all_items()
    match = next((item for item in local_items if item["barcode"] == barcode), None)
    
    if match:
        return jsonify(match), 200

    # Perform isolated scanning routine targeting the barcode string attribute
    product = api.fetch_product_details(barcode=barcode)
    if product.get("status") == 1:
        # Extract internal nested object directly to output clean payload structure
        return jsonify(product["product"]), 200
    return jsonify({"error": "Product not found"}), 404

@app.route("/inventory/import/<string:barcode>", methods=["POST"])
def import_barcode(barcode):
    # Fetch data structure from external openfoodfacts upstream index endpoints
    product_data = api.fetch_product_details(barcode=barcode)
    if product_data.get("status") != 1:
        return jsonify({"error": "Failed to import from external API"}), 404
    
    # Unwrap upstream variables and pass values into internal persistent structure
    prod = product_data["product"]
    item = api.create_item(
        name=prod["name"],
        quantity=1,
        price=0.0,
        barcode=prod["barcode"],
        brand=prod["brand"],
        ingredients=prod["ingredients"]
    )
    return jsonify(item), 201

if __name__ == "__main__":
    # Dev server environment flag forces live module reloads on save adjustments
    app.run(debug=True, port=5000)
