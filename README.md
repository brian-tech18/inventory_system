# Inventory Management CLI

A Flask-based inventory management system that allows users to manage products through a Command-Line Interface (CLI) or RESTful API. Products can be created, updated, deleted, searched, and imported using an external barcode API.

## Features

- Add a new product
- View all products
- View a product by ID
- Update a product
- Delete a product
- Search products by barcode
- Import products from an external API
- Interactive Command-Line Interface (CLI)
- RESTful API
- Unit tests with pytest

## Technologies Used

- Python 3
- Flask
- Pytest
- JSON
- Requests

## Installation

Clone the repository:

```bash
git clone https://github.com/mainamuchiru/inventory-management-cli.git
cd inventory-management-cli
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Flask API

From the project root, run:

```bash
python3 -m app.routes.routes
```

The server will start on:

```
http://127.0.0.1:5000
```

## Running the CLI

Start the interactive command-line application:

```bash
python3 cli/cli.py
```
## Project Structure
```
inventory-management-cli/
├── app/
│   ├── crud/
│   │   ├── __init__.py
│   │   └── crud.py
│   ├── models/
│   │   └── product.py
│   ├── routes/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── external_api.py
│   └── __init__.py
├── cli/
│   └── cli.py
├── tests/
│   └── test_app.py
├── utils/
├── product.json
├── requirements.txt
├── .gitignore
└── README.md
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Welcome message |
| GET | `/inventory` | Get all products |
| GET | `/inventory/<id>` | Get product by ID |
| POST | `/inventory` | Add a product |
| PATCH | `/inventory/<id>` | Update a product |
| DELETE | `/inventory/<id>` | Delete a product |
| GET | `/search/<barcode>` | Search for a product using a barcode |
| POST | `/inventory/import/<barcode>` | Import a product from the external API |

## Running Tests

Run all tests with either:

```bash
pytest

or

python3 -m pytest tests -v
```

## Author

Brian Kimani

