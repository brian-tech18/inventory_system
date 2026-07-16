class Inventory:
    # We define these as class-level variables because we want our data to persist 
    # across different web requests. If we put them inside an __init__ constructor, 
    # every fresh route call would create a blank list and our data would disappear.
    items = []
    next_id = 1

    def __init__(self):
        # We leave this constructor empty because we don't want callers creating 
        # separate instance objects that would break our single data storage array.
        pass

    @classmethod
    def seed_data(cls):
        # We check if the list is empty before adding default items because we don't 
        # want to duplicate our baseline data every time the server restarts or reloads.
        if not cls.items:
            cls.add_item("Milk", 10, 2.50, "12345", "DairyCo", "Water, Milk Fat")
            cls.add_item("Bread", 5, 1.99, "67890", "BakeryHome", "Wheat Flour, Yeast")

    @classmethod
    def get_all_items(cls):
        # We return the whole list because our GET routing endpoints need a full 
        # array payload to display the complete store tracking logs to the user.
        return cls.items

    @classmethod
    def get_item(cls, item_id):
        # We loop through the records to find a match because item IDs are unique keys.
        # Returning None if no match is found allows our web server to easily trigger a 404 error.
        for item in cls.items:
            if item["id"] == item_id:
                return item
        return None

    @classmethod
    def add_item(cls, name, quantity, price=0.0, barcode=None, brand=None, ingredients=None):
        # We manually construct a dictionary structure because JSON frameworks need 
        # basic key-value data mappings to serialize records cleanly without crashing.
        item = {
            "id": cls.next_id,
            "name": name,
            "quantity": int(quantity),  # We cast to int to guarantee we don't store broken string fractions
            "price": float(price),      # We cast to float so financial calculations remain precise
            "barcode": barcode or "N/A",
            "brand": brand or "Generic",
            "ingredients": ingredients or "N/A"
        }
        cls.items.append(item)
        
        # We increment our counter variable because we must ensure the next product added 
        # receives a totally unique tracking key to prevent collision bugs.
        cls.next_id += 1
        return item

    @classmethod
    def update_item(cls, item_id, updates):
        # We retrieve the item first because we cannot update something that doesn't exist.
        item = cls.get_item(item_id)
        if not item:
            return None
            
        # We loop through specific keys because a PATCH request is allowed to be partial.
        # This approach ensures we only overwrite fields the user explicitly asked to change.
        for key in ["name", "quantity", "price", "barcode", "brand", "ingredients"]:
            if key in updates:
                if key == "quantity":
                    item[key] = int(updates[key])
                elif key == "price":
                    item[key] = float(updates[key])
                else:
                    item[key] = updates[key]
        return item

    @classmethod
    def delete_item(cls, item_id):
        # We search for the item before dropping it because we need to return its details 
        # to the calling function so the user interface can confirm exactly what was wiped out.
        item = cls.get_item(item_id)
        if not item:
            return None
            
        # We recreate the list omitting the target ID because list filters are the safest 
        # way to mutate in-memory arrays without dealing with index shifting errors.
        cls.items = [i for i in cls.items if i["id"] != item_id]
        return item
