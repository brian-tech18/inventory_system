import requests

# We define these URL string configurations as clear global constants because changing 
# API version routes or staging domains in the future shouldn't force us to hunt through methods.
OPENFOODFACTS_PRODUCT_URL = "https://openfoodfacts.org{barcode}.json"
OPENFOODFACTS_SEARCH_URL = "https://openfoodfacts.org"

# We must explicitly declare a descriptive User-Agent header string because the OpenFoodFacts 
# server firewall automatically blocks default Python scripts to protect their system from bad bots.
OFF_HEADERS = {
    "User-Agent": "MoringaStudentInventoryProject/1.0 (studentwork@school.edu)"
}

class InventoryAPI:
    def __init__(self, inventory_instance):
        # We pass the storage class module definition here because our business logic 
        # wrapper layer needs a shared channel to push data records straight into the list storage.
        self.inventory = inventory_instance
        self.inventory.seed_data()

    def get_all_items(self):
        return self.inventory.get_all_items()

    def get_item(self, item_id):
        return self.inventory.get_item(item_id)

    def create_item(self, name, quantity, price=0.0, barcode=None, brand=None, ingredients=None):
        return self.inventory.add_item(name, quantity, price, barcode, brand, ingredients)

    def update_item(self, item_id, updates):
        return self.inventory.update_item(item_id, updates)

    def delete_item(self, item_id):
        return self.inventory.delete_item(item_id)

    def fetch_product_details(self, barcode=None, product_name=None):
        # We isolate the barcode option first because barcode searches look up exact individual items, 
        # which is much faster and more accurate than scanning text descriptions.
        if barcode:
            url = OPENFOODFACTS_PRODUCT_URL.format(barcode=barcode)
            try:
                # We apply a strict timeout limit because we don't want our entire application 
                # to lock up indefinitely if the external internet network goes down or runs slowly.
                response = requests.get(url, headers=OFF_HEADERS, timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    # OpenFoodFacts returns status 1 or "1" when an item is officially found in their index.
                    if data.get("status") == 1 or data.get("status") == "1":
                        prod = data.get("product", {})
                        # We return a standardized dictionary format because our internal system components 
                        # expect consistent naming keys (like 'name' instead of 'product_name') to avoid data mapping crashes.
                        return {
                            "status": 1,
                            "product": {
                                "name": prod.get("product_name", "Unknown Item"),
                                "brand": prod.get("brands", "Generic"),
                                "barcode": barcode,
                                "ingredients": prod.get("ingredients_text", "N/A")
                            }
                        }
            except requests.RequestException:
                # We suppress raw network crashes here because we want to return a clean error dictionary 
                # that our frontend can display politely, instead of letting Python crash.
                pass
        
        elif product_name:
            # We bundle query terms into a params dictionary because the requests library handles 
            # safe character escaping and urlencoding automatically for us behind the scenes.
            query_params = {
                "search_terms": product_name,
                "json": 1,
                "page_size": 1
            }
            try:
                response = requests.get(OPENFOODFACTS_SEARCH_URL, headers=OFF_HEADERS, params=query_params, timeout=5)
                if response.status_code == 200:
                    products = response.json().get("products", [])
                    if products:
                        first_prod = products[0]  # We grab index zero because we only need the best primary match
                        return {
                            "status": 1,
                            "product": {
                                "name": first_prod.get("product_name", product_name),
                                "brand": first_prod.get("brands", "Generic"),
                                "barcode": first_prod.get("code", "N/A"),
                                "ingredients": first_prod.get("ingredients_text", "N/A")
                            }
                        }
            except requests.RequestException:
                pass

        return {"status": 0, "error": "Product data could not be recovered from the external service"}
