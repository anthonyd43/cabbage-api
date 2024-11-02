# Cabbage API

Cabbage API is a transaction management API built with FastAPI and Plaid. It connects to various financial accounts (credit card, savings, and checking) through Plaid to retrieve, transform, and provide structured payment transaction data.

## Key Features

- **Transaction Retrieval**: Fetch transaction data securely from linked financial accounts.
- **Data Transformation**: Process and structure raw transaction data into a user-friendly format for analysis and reporting.
- **Seamless Integration**: Designed to be easily used with the Cabbage front end to visualize spending habits in an intuitive calendar view.

## Technologies

- **FastAPI**: Backend framework for creating and managing endpoints.
- **Plaid**: API to connect to user bank and credit card accounts for secure data retrieval.

## Installation & Usage

1. **Set Up Dependencies**: Install requirements with `poetry install`.
2. **Configure Environment Variables**: Add Plaid and other necessary API keys.

---