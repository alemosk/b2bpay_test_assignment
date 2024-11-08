# B2BPay Project (B2Broker Test Assignment)

## About
This project is a test assignment from B2Broker, implemented as a product called B2BPay.
B2BPay (Business to Business Pay) is a payment system that allows clients to store balances in their wallets and perform deposits and withdrawals.

The MVP, as requested by the client, includes only the wallet and transaction logic accessible through the JSON:API protocol.

## Project Setup
The project was developed and tested on x86_64 architecture using Linux Mint 22.

### Cloning from GitHub
```shell
$ git clone git@github.com:alemosk/b2bpay_test_assignment.git b2bpay_app
$ cd b2bpay_app
```

### Configuration
The project reads settings from a `.env` file.

An example configuration is available in `.env_example`.
Copy this file and review the settings.
```shell
$ cp .env_example .env
```

## Running the Project Using Docker Compose
Docker installation instructions are available [here](https://docs.docker.com/engine/install/).

This application has pre-built Docker containers available on `docker.io`.
```shell
$ docker compose pull
$ docker compose up -d
```

Alternatively, to build the project locally, use the following commands:
```shell
$ docker compose build
$ docker compose up -d
```

### Running Tests
```shell
$ docker compose exec -it b2bpay pytest
```

## Running on a Local Machine (Linux)
### Installing the Required Python Version with pyenv
Follow the pyenv installation guide [here](https://github.com/pyenv/pyenv?tab=readme-ov-file#installation).
```shell
$ pyenv install 3.11.10
```

### Setting Up the Python Environment
```shell
$ python -m venv venv
$ source venv/bin/activate
$ pip install -U pip setuptools
$ pip install -r requirements.txt
```

### Creating the Database
This project is configured to use MySQL. You need to create the database if it’s running on localhost.
```mysql
CREATE DATABASE b2bpay;
CREATE DATABASE b2bpay_test;
```

### Applying Migrations
```shell
$ alembic upgrade head
```

### Running Tests
```shell
$ pytest
```

### Running the Project
Depending on your configuration, the project will run on the specified port on localhost. For example:
`http://localhost:8000`
```shell
$ python manage.py runserver 127.0.0.1:8000
```

## Usage

### Wallet Creation
```shell
$ curl -X POST http://localhost:8000/finances/wallets/ \
     -H "Content-Type: application/vnd.api+json" \
     -d '{
           "data": {
             "type": "Wallet",
             "attributes": {
               "label": "USD wallet"
             }
           }
         }'

$ curl -X POST http://localhost:8000/finances/wallets/ \
     -H "Content-Type: application/vnd.api+json" \
     -d '{
           "data": {
             "type": "Wallet",
             "attributes": {
               "label": "EUR"
             }
           }
         }'

$ curl -X POST http://localhost:8000/finances/wallets/ \
     -H "Content-Type: application/vnd.api+json" \
     -d '{
           "data": {
             "type": "Wallet",
             "attributes": {
               "label": "EUR wallet"
             }
           }
         }'
```

### Wallet Update
```shell
$ curl -X PATCH http://localhost:8000/finances/wallets/2/ \
     -H "Content-Type: application/vnd.api+json" \
     -d '{
           "data": {
             "type": "Wallet",
             "id": "2",
             "attributes": {
               "label": "EUR wallet"
             }
           }
         }'
```

### Wallet Deletion
```shell
$ curl -X DELETE http://localhost:8000/finances/wallets/3/ \
     -H "Content-Type: application/vnd.api+json"
```

> Note: You cannot delete a wallet if it contains transactions.

### Transaction Creation
```shell
$ curl -X POST http://localhost:8000/finances/transactions/ \
     -H "Content-Type: application/vnd.api+json" \
     -d '{
           "data": {
             "type": "Transaction",
             "attributes": {
               "txid": "42388c7c-9dde-11ef-b606-c7f588dc9cd2",
               "wallet": 1,
               "amount": 100.00
             }
           }
         }'

$ curl -X POST http://localhost:8000/finances/transactions/ \
     -H "Content-Type: application/vnd.api+json" \
     -d '{
           "data": {
             "type": "Transaction",
             "attributes": {
               "txid": "71dc5472-9dde-11ef-ba90-cf5053652253",
               "wallet": 1,
               "amount": -25.00
             }
           }
         }'

$ curl -X POST http://localhost:8000/finances/transactions/ \
     -H "Content-Type: application/vnd.api+json" \
     -d '{
           "data": {
             "type": "Transaction",
             "attributes": {
               "txid": "cf178e2c-9dde-11ef-9aed-cfcde3094368",
               "wallet": 2,
               "amount": 25.00
             }
           }
         }'
```

### Transaction Modification and Deletion
Transaction editing and deletion are not supported because this is considered a bad practice in financial applications, where consistent data and reporting to regulatory authorities are essential.

### Wallet Filters
The `id` and `balance` fields support `lt`, `gt`, `gte`, `lte`, and `in` filter methods in addition to equality.

The `label` field supports the `startswith` filter method in addition to equality.

Examples:
- http://localhost:8000/finances/wallets/?filter[id]=1
- http://localhost:8000/finances/wallets/?filter[id.gt]=1
- http://localhost:8000/finances/wallets/?filter[id.in]=1,2

### Wallet Pagination
Example:
- http://localhost:8000/finances/wallets/?page[size]=1&page[number]=2

### Wallet Sorting
Ascending and descending sorting are supported by `id`, `balance`, and `label` fields.

Examples:
- http://localhost:8000/finances/wallets/?sort=balance
- http://localhost:8000/finances/wallets/?sort=-id

### Transaction Filters
The `id`, `amount`, and `wallet` fields support `lt`, `gt`, `gte`, `lte`, and `in` filter methods in addition to equality.

The `txid` field supports the `startswith` filter method in addition to equality.

Examples:
- http://localhost:8000/finances/transactions/?filter[amount]=25
- http://localhost:8000/finances/transactions/?filter[amount.lt]=10
- http://localhost:8000/finances/transactions/?filter[txid.startswith]=71

### Transaction Pagination
Example:
- http://localhost:8000/finances/transactions/?page[size]=1&page[number]=2

### Transaction Sorting
Ascending and descending sorting are supported by `id`, `amount`, `txid`, and `wallet` fields.

Examples:
- http://localhost:8000/finances/transactions/?sort=-id
- http://localhost:8000/finances/transactions/?sort=txid

## Notes
I use Alembic for migrations in the app, while Django's native migration framework is used for testing. 
Unfortunately, I haven't found a quick solution to load the Alembic configuration in pytest fixtures with session scope.

I disabled the auth module to remove dependencies on other tables that were not specified in the task and 
are not required for the app's functionality.

In the transaction model, I used the maximum decimal value because the task did not specify limits. 
If this is revised in the future, this value could be adjusted accordingly.

I indexed every field in the database to demonstrate filtering methods. For fields used in filters, 
indexes are necessary to prevent performance issues when the data volume grows. 
I understand that indexes can impact database insert performance.

In git commit comments, I use the format `<Ticket number>: comment`. In my experience, the content of the comments i
s generally less significant than the ticket number, which is essential for future incident investigations.

For this project, I use `flake8` for linting and `isort` for sorting imports.
