import sys
import argparse
import requests

# Base endpoint configuration tracks our local development server instance
BASE_URL = "http://127.0.0.1:5000"

def main():
    # Use native argument parser engine to handle text flags directly on execution
    parser = argparse.ArgumentParser(description="Retail Inventory Administration System CLI Tool")
    subparsers = parser.add_subparsers(dest="command")

    # Define simple action commands that execute without trailing data tokens
    subparsers.add_parser("list")
    
    # Configure precise single resource lookup flag parameters
    get_parser = subparsers.add_parser("get")
    get_parser.add_argument("id", type=int)

    # Core object creation arguments map directly to database schema constraints
    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("name", type=str)
    add_parser.add_argument("quantity", type=int)
    add_parser.add_argument("--price", type=float, default=0.0)
    add_parser.add_argument("--barcode", type=str)
    add_parser.add_argument("--brand", type=str)

    # Target fields for inline modifications on existing records
    update_parser = subparsers.add_parser("update")
    update_parser.add_argument("id", type=int)
    update_parser.add_argument("--quantity", type=int)
    update_parser.add_argument("--price", type=float)

    # Core deletion parsing options matching target resource unique identifiers
    delete_parser = subparsers.add_parser("delete")
    delete_parser.add_argument("id", type=int)

    # Direct variable routing parameters for barcode scanning checks
    search_parser = subparsers.add_parser("search")
    search_parser.add_argument("barcode", type=str)

    # Inbound synchronization tracking parameters for upstream imports
    import_parser = subparsers.add_parser("import")
    import_parser.add_argument("barcode", type=str)

    args = parser.parse_args()

    # Throw active usage guide instructions if user starts tool blank
    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        # Evaluate execution branch pathways based on active command tokens
        if args.command == "list":
            # Target inventory route namespace array to fetch all live data records
            res = requests.get(f"{BASE_URL}/inventory")
            print(res.text)

        elif args.command == "get":
            # Dynamic path expansion targets structural sub-routing pathways
            res = requests.get(f"{BASE_URL}/inventory/{args.id}")
            print(res.text)

        elif args.command == "add":
            # Build construction dict payload dynamically from runtime options
            payload = {"name": args.name, "quantity": args.quantity, "price": args.price}
            if args.barcode: 
                payload["barcode"] = args.barcode
            if args.brand: 
                payload["brand"] = args.brand
                
            res = requests.post(f"{BASE_URL}/inventory", json=payload)
            print(res.text)

        elif args.command == "update":
            # Isolate active change variables to keep existing parameters un-mutated
            payload = {}
            if args.quantity is not None: payload["quantity"] = args.quantity
            if args.price is not None: payload["price"] = args.price
            
            res = requests.patch(f"{BASE_URL}/inventory/{args.id}", json=payload)
            print(res.text)

        elif args.command == "delete":
            # Route payload destruction events straight to corresponding backend entry point
            res = requests.delete(f"{BASE_URL}/inventory/{args.id}")
            print(res.text)

        elif args.command == "search":
            # Match clean path structural variables defined in rewritten server routing file
            res = requests.get(f"{BASE_URL}/search/{args.barcode}")
            print(res.text)

        elif args.command == "import":
            # Trigger downstream persistence creation based on remote barcode scans
            res = requests.post(f"{BASE_URL}/inventory/import/{args.barcode}")
            print(res.text)

    except requests.exceptions.ConnectionError:
        # Prevent shell engine from dumping scary trace blocks when backend server is off
        print("Network Connection Error: Please verify that your Flask server application is currently running.")

if __name__ == "__main__":
    main()
