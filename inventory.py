import os
import json

class Inventory:
    # Target file paths point straight to the persistent JSON layer on disk
    DATA_FILE = "product.json"

    @classmethod
    def _load_data(cls):
        """Helper method to pull current catalog data records straight from the JSON file."""
        if not os.path.exists(cls.DATA_FILE):
            # Fallback to an empty storage tracker array if the file doesn't exist yet
            return []
        try:
            with open(cls.DATA_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            # Guard against empty or corrupted files crashing the runtime engine
            return []

    @classmethod
    def _save_data(cls, data):
        """Helper method to commit current array mutations directly to disk storage."""
        try:
            with open(cls.DATA_FILE, "w") as f:
                json.dump(data, f, indent=2)
        except IOError:
            # Silence low-level disk execution writes gracefully
            pass

    @classmethod
    def seed_data(cls):
        # Scan disk array records to prevent rewriting seed data if entries exist
        current_items = cls._load_data()
        if not current_items:
            # Initialize baseline inventory data configurations on pristine workspace setups
            cls.add_item("Fresh Milk", 20, price=2.50, barcode="123456", brand="Brookside")
            cls.add_item("Whole Wheat Bread", 15, price=1.80, barcode="789012", brand="Supaloaf")
            cls.add_item("Salted Butter", 30, price=4.20, barcode="345678", brand="KCC")

    @classmethod
    def get_all_items(cls):
        # Pull dynamic, live state data from disk instead of tracking obsolete in-memory objects
        return cls._load_data()

    @classmethod
    def get_item(cls, item_id):
        # Evaluate record matches using linear sequence scans against active disk dumps
        items = cls._load_data()
        return next((item for item in items if item["id"] == item_id), None)

    @classmethod
    def add_item(cls, name, quantity, price=0.0, barcode=None, brand=None, ingredients=None):
        items = cls._load_data()
        
        # Calculate sequential auto-incrementing key offsets relative to the highest existing ID row
        next_id = max([item["id"] for item in items], default=0) + 1

        new_item = {
            "id": next_id,
            "name": name,
            "quantity": int(quantity),
            "price": float(price),
            "barcode": barcode or "",
            "brand": brand or "Generic",
            "ingredients": ingredients or "N/A"
        }
        
        # Merge new entity trackers and safely export changes to storage files
        items.append(new_item)
        cls._save_data(items)
        return new_item

    @classmethod
    def update_item(cls, item_id, updates):
        items = cls._load_data()
        target_item = None
        
        # Find exact dictionary array elements by tracing structural property signatures
        for item in items:
            if item["id"] == item_id:
                target_item = item
                break
                
        if not target_item:
            return None
            
        # Isolate inbound field variations to match explicit schema boundaries
        valid_keys = ["name", "quantity", "price", "barcode", "brand", "ingredients"]
        for key, value in updates.items():
            if key in valid_keys:
                if key == "quantity":
                    target_item[key] = int(value)
                elif key == "price":
                    target_item[key] = float(value)
                else:
                    target_item[key] = value
                    
        # Persist modified states back to database files on the machine disk
        cls._save_data(items)
        return target_item

    @classmethod
    def delete_item(cls, item_id):
        items = cls._load_data()
        for idx, item in enumerate(items):
            if item["id"] == item_id:
                # Evict index entries and output copies back to tracking controllers
                deleted = items.pop(idx)
                cls._save_data(items)
                return deleted
        return None
