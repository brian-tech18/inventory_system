import unittest
import sys
import os

# Append the parent directory to system paths so tests can find app.py cleanly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
from inventory import Inventory

class TestInventorySystem(unittest.TestCase):
    def setUp(self):
        # Refresh and flush class array variables to prevent state leak contamination
        Inventory.items = []
        Inventory.next_id = 1
        Inventory.seed_data()
        self.api = Inventory
        
        # Instantiate localized engine wrapper to run headless request pipeline simulation calls
        self.client = app.test_client()

    def test_core_creation(self):
        item = self.api.add_item("Test Unit", 5, price=1.5, barcode="9999")
        self.assertEqual(item["name"], "Test Unit")
        self.assertEqual(item["quantity"], 5)

    def test_core_modification(self):
        # Dynamically resolve live array states to avoid un-subscriptable None type crashes
        items = self.api.get_all_items()
        target_id = items[0]["id"] if items else 1
        
        updated = self.api.update_item(target_id, {"price": 10.99})
        self.assertIsNotNone(updated)
        self.assertEqual(updated["price"], 10.99)

    def test_core_deletion(self):
        items = self.api.get_all_items()
        target_id = items[0]["id"] if items else 1
        
        deleted = self.api.delete_item(target_id)
        self.assertEqual(deleted["id"], target_id)
        self.assertIsNone(self.api.get_item(target_id))

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
