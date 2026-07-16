# Inventory Management System Lab

A complete class-based Flask REST API tracking tool featuring core item CRUD paths, an argument-parsed command line administrator terminal client interface, and OpenFoodFacts data lookups.

## Project Structure

* `inventory.py` - Core object-oriented list array data store class variables.
* `api.py` - External integration management wrapper layout.
* `app.py` - Flask web router definitions map.
* `cli.py` - Argument-parsed command interface program.
* `test_app.py` - Local function and path routing verification tests.

## Running the Application

### 1. Fire up the backend storage web server:
```bash
python3 app.py
```

### 2. Open an alternate terminal window to manipulate items via the CLI:
```bash
python3 cli.py list
python3 cli.py get 1
python3 cli.py add "Orange Juice" 25 --price 3.15 --brand "FruitCo"
python3 cli.py update 1 --quantity 40 --price 3.99
python3 cli.py delete 1
python3 cli.py fetch --barcode 3017620422003
```

### 3. Run your automated verification tests:
```bash
python3 -m unittest test_app.py
```
