from flask import Flask, jsonify, request
from inventory import Inventory
from api import InventoryAPI

app = Flask(__name__)

# We feed our core static Inventory class layer directly into the engine interface on bootup 
# because we must make sure all web routing calls talk to the exact same list data location.
api = InventoryAPI(Inventory)

# We use the exact plural endpoint name /items to match our client expectations and test runs.
@app.route("/items", methods=["GET"])
def get_items():
    # We wrap the results inside jsonify() because web browsers and HTTP client scripts 
    # require structured text formatting headers to parse data strings cleanly over the network.
    return jsonify(api.get_all_items()), 200

@app.route("/items/<int:item_id>", methods=["GET"])
def get_item(item_id):
    item = api.get_item(item_id)
    # We check for a None return value because attempting to serve an empty resource signature 
    # would break client side decoders; we throw an official 404 message block instead.
    if not item:
        return jsonify({"error": "Target item registry not found"}), 404
    return jsonify(item), 200

@app.route("/items", methods=["POST"])
def add_item():
    # We parse the body configuration parameters safely to prevent server side execution crashes 
    # if an administrator submits a broken or completely blank object payload package.
    data = request.get_json() or {}
    if "name" not in data or "quantity" not in data:
        return jsonify({"error": "Missing critical parameters: name and quantity are required"}), 400
    
    # We use normal assignment equals signs (=) here instead of bad subtraction hyphens (-) 
    # because we want our runtime compiler to pass assignment variables into the method parameters correctly.
    item = api.create_item(
        name=data.get("name"),
        quantity=data.get("quantity"),
        price=data.get("price", 0.0),
        barcode=data.get("barcode"),
        brand=data.get("brand"),
        ingredients=data.get("ingredients")
    )
    return jsonify({"message": "Item registered successfully", "item": item}), 201

@app.route("/items/<int:item_id>", methods=["PATCH"])
def update_item(item_id):
    updates = request.get_json() or {}
    item = api.update_item(item_id, updates)
    if not item:
        return jsonify({"error": "Modification block: Target item does not exist"}), 404
    return jsonify({"message": "Item edited successfully", "item": item}), 200

@app.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    item = api.delete_item(item_id)
    if not item:
        return jsonify({"error": "Deletion block: Target item does not exist"}), 404
    return jsonify({"message": "Item completely removed from core storage", "item": item}), 200

@app.route("/items/fetch", methods=["GET"])
def fetch_external():
    # We collect optional query line URL strings because our portal user might search 
    # using either a numerical barcode sequence string or a plain text name query.
    barcode = request.args.get("barcode")
    name = request.args.get("name")
    
    product = api.fetch_product_details(barcode=barcode, product_name=name)
    if product.get("status") == 1:
        return jsonify(product), 200
    return jsonify(product), 404

if __name__ == "__main__":
    # We keep debug=True active during development because we need our local terminal window 
    # to automatically refresh and print clear trace error summaries whenever we change code lines.
    app.run(debug=True, port=5000)
