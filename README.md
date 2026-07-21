# Inventory Management System

A Flask-based inventory management system that allows users to manage products through a Command-Line Interface (CLI) or RESTful API. Products can be created, updated, deleted, searched, and imported using the OpenFoodFacts barcode API.

## Features

- Add, update, delete, and list inventory products
- Search products locally or look them up via external barcode API
- Import external barcode data straight into local JSON storage
- Interactive Command-Line Interface (CLI)
- RESTful API built with Flask
- Unit tests written with standard `unittest`

## Tech Stack

- Python 3
- Flask
- Requests
- JSON Storage

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone git@github.com:brian-tech18/inventory_system.git
   cd inventory_system
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Flask API

From the project root, start the server:
```bash
python3 app.py
```
The server will start on: `http://127.0.0.1:5000`

## Running the CLI

Open a separate terminal window (with the virtual environment activated) and execute CLI commands:

```bash
# List all items
python3 cli.py list

# Get a specific item by ID
python3 cli.py get 1

# Add a new item
python3 cli.py add "Coffee Beans" 12 --price 8.50

# Update an item
python3 cli.py update 1 --price 10.99

# Search item by barcode
python3 cli.py search 345678

# Delete an item
python3 cli.py delete 1
```

## Project Structure

```text
inventory_system/
├── tests/
│   ├── __init__.py
│   └── test_app.py
├── .gitignore
├── api.py
├── app.py
├── cli.py
├── inventory.py
├── product.json
├── README.md
└── requirements.txt
```

## API Endpoints

*Base URL: `http://127.0.0.1:5000`*

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| **GET** | `/` | API status message |
| **GET** | `/inventory` | Get all products |
| **GET** | `/inventory/<id>` | Get product by ID |
| **POST** | `/inventory` | Add a product |
| **PATCH** | `/inventory/<id>` | Update a product |
| **DELETE** | `/inventory/<id>` | Delete a product |
| **GET** | `/search/<barcode>` | Search for a product using a barcode |
| **POST** | `/inventory/import/<barcode>` | Import a product from the external API |

## Running Tests

Run the full test suite with:
```bash
python3 -m unittest tests/test_app.py
```

## Author

Brian Kimani Khalid
