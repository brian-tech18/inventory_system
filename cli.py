import sys
import argparse
import requests

BASE_URL = "http://127.0.0.1:5000"

def main():
    # We use Python's built-in argparse tool because it reads command line flags 
    # directly on the execution line (like 'list' or 'delete 1') which avoids making messy while-loops.
    parser = argparse.ArgumentParser(description="Retail Inventory Administration System CLI Tool")
    subparsers = parser.add_subparsers(dest="command")

    # We register dedicated operational sub-command flags so our string argument parser 
    # knows exactly how to group incoming options without getting command variables mixed up.
    subparsers.add_parser("list")
    
    get_parser = subparsers.add_parser("get")
    get_parser.add_argument("id", type=int)

    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("name", type=str)
    add_parser.add_argument("quantity", type=int)
    add_parser.add_argument("--price", type=float, default=0.0)
    add_parser.add_argument("--barcode", type=str)
    add_parser.add_argument("--brand", type=str)

    update_parser = subparsers.add_parser("update")
    update_parser.add_argument("id", type=int)
    update_parser.add_argument("--quantity", type=int)
    update_parser.add_argument("--price", type=float)

    delete_parser = subparsers.add_parser("delete")
    delete_parser.add_argument("id", type=int)

    fetch_parser = subparsers.add_parser("fetch")
    fetch_parser.add_argument("--barcode", type=str)
    fetch_parser.add_argument("--name", type=str)

    args = parser.parse_args()

    try:
        # We break our execution pathways down using standard conditional statements 
        # because each unique console command must target a totally different REST route method.
        if args.command == "list":
            res = requests.get(f"{BASE_URL}/items")
            print(res.text)

        elif args.command == "get":
            res = requests.get(f"{BASE_URL}/items/{args.id}")
            print(res.text)

        elif args.command == "add":
            payload = {"name": args.name, "quantity": args.quantity, "price": args.price}
            if args.barcode: payload["barcode"] = args.barcode
            if args.brand: payload["brand"] = args.brand
            res = requests.post(f"{BASE_URL}/items", json=payload)
            print(res.text)

        elif args.command == "update":
            payload = {}
            if args.quantity is not None: payload["quantity"] = args.quantity
            if args.price is not None: payload["price"] = args.price
            # We use an equal sign (=) here to fix the broken hyphen subtraction typo (json-payload) 
            # so Flask receives our JSON dictionary variables clearly.
            res = requests.patch(f"{BASE_URL}/items/{args.id}", json=payload)
            print(res.text)

        elif args.command == "delete":
            res = requests.delete(f"{BASE_URL}/items/{args.id}")
            print(res.text)

        elif args.command == "fetch":
            params = {}
            if args.barcode: params["barcode"] = args.barcode
            if args.name: params["name"] = args.name
            # We completely omit legacy urlencode functions here because the requests library 
            # automatically formats our query strings correctly when we use the params keyword.
            res = requests.get(f"{BASE_URL}/items/fetch", params=params)
            print(res.text)

    except requests.exceptions.ConnectionError:
        # We catch connection issues here because we want to print a clear reminder 
        # to boot up the web server if we forget to turn on app.py in our alternate terminal window.
        print("Network Connection Error: Please verify that 'python app.py' is currently running.")

if __name__ == "__main__":
    main()
