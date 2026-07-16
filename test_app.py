import unittest
from app import app
from inventory import Inventory

class TestInventorySystem(unittest.TestCase):
    def setUp(self):
        # We completely clear and refresh our class variables before every single test 
        # because we need a guaranteed clean slate so our tests don't leak state into each other.
        Inventory.items = []
        Inventory.next_id = 1
        Inventory.seed_data()
        self.api = Inventory
        # We initialize Flask's test client tool because it simulates actual web requests 
        # hitting our routes without needing to spin up a heavy live server process.
        self.client = app.test_client()

    def test_core_creation(self):
        item = self.api.add_item("Test Unit", 5, price=1.5, barcode="9999")
        self.assertEqual(item["name"], "Test Unit")
        self.assertEqual(item["quantity"], 5)

    def test_core_modification(self):
        updated = self.api.update_item(1, {"price": 10.99})
        self.assertEqual(updated["price"], 10.99)

    def test_core_deletion(self):
        deleted = self.api.delete_item(1)
        self.assertEqual(deleted["id"], 1)
        self.assertIsNone(self.api.get_item(1))

    def test_get_all_endpoint(self):
        res = self.client.get("/items")
        self.assertEqual(res.status_code, 200)

    def test_route_creation_and_mutation_flow(self):
        # We isolate variables using standard assignment tools to wipe out the hyphen bug completely.
        payload = {"name": "Test Run Drink", "quantity": 10, "price": 2.50}
        
        # We explicitly use res.get_json() instead of response.json properties 
        # because the Werkzeug test response object requires helper method calls to access dicts without crashes.
        create_res = self.client.post("/items", json=payload)
        self.assertEqual(create_res.status_code, 201)
        
        item_data = create_res.get_json()
        target_id = item_data["item"]["id"]

        patch_res = self.client.patch(f"/items/{target_id}", json={"quantity": 12})
        self.assertEqual(patch_res.status_code, 200)
        self.assertEqual(patch_res.get_json()["item"]["quantity"], 12)

        del_res = self.client.delete(f"/items/{target_id}")
        self.assertEqual(del_res.status_code, 200)

if __name__ == "__main__":
    # We call unittest.main() because we need the Python file to trigger the test runner automatically 
    # when we execute it straight from our terminal using 'python test_app.py'.
    unittest.main()
