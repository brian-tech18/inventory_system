import unittest
import os
import json
from app import app
from inventory import Inventory

class TestInventorySystem(unittest.TestCase):
    def setUp(self):
        # Point tests to a temporary JSON file so product.json is not modified
        Inventory.DATA_FILE = "test_product.json"
        
        # Reset test JSON file to clean seed data
        initial_data = [
            {
                "id": 1,
                "name": "Fresh Milk",
                "quantity": 20,
                "price": 2.50,
                "barcode": "123456",
                "brand": "Brookside",
                "ingredients": "N/A"
            }
        ]
        with open(Inventory.DATA_FILE, "w") as f:
            json.dump(initial_data, f)
            
        self.api = Inventory
        self.client = app.test_client()

    def tearDown(self):
        # Clean up temporary test file after runs
        if os.path.exists("test_product.json"):
            os.remove("test_product.json")
            
        # Restore original DATA_FILE reference
        Inventory.DATA_FILE = "product.json"

    def test_core_creation(self):
        item = self.api.add_item("Test Unit", 5, price=1.5, barcode="9999")
        self.assertEqual(item["name"], "Test Unit")
        self.assertEqual(item["quantity"], 5)

    def test_core_modification(self):
        updated = self.api.update_item(1, {"price": 10.99})
        self.assertIsNotNone(updated)
        self.assertEqual(updated["price"], 10.99)

    def test_core_deletion(self):
        deleted = self.api.delete_item(1)
        self.assertEqual(deleted["id"], 1)
        self.assertIsNone(self.api.get_item(1))

    def test_get_all_endpoint(self):
        res = self.client.get("/inventory")
        self.assertEqual(res.status_code, 200)

    def test_route_creation_and_mutation_flow(self):
        payload = {"name": "Test Run Drink", "quantity": 10, "price": 2.50}
        
        create_res = self.client.post("/inventory", json=payload)
        self.assertEqual(create_res.status_code, 201)
        
        item_data = create_res.get_json()
        target_id = item_data["id"]

        patch_res = self.client.patch(f"/inventory/{target_id}", json={"quantity": 12})
        self.assertEqual(patch_res.status_code, 200)
        self.assertEqual(patch_res.get_json()["quantity"], 12)

        del_res = self.client.delete(f"/inventory/{target_id}")
        self.assertEqual(del_res.status_code, 200)

if __name__ == "__main__":
    unittest.main()