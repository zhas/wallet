# Wallet

## Description

This is implementation of test assignment.

The goal is to implement basic payment system with following requirements:

- system should handle large number of requests and stay consistent

- each client in system has one wallet

- wallet has balance

- clients can transfer money to each other

- system has only one currency USD

- all operations should be logged

- should contain next endpoints:

    - create client

    - create wallet

    - deposit

    - transfer

- service should be wrapped in docker container

**Note: this assignment does not cover authentication and permissions**

## Implementation details

- to improve server capability of serving large number of requests async web framework was chosen

- pessimistic locking approach used to avoid race conditions

- core functionality tested using pytest

###  Stack

- Language: Python 3.8+

- Web framework: FastAPI

- Web server: Uvicorn

- Relational database: Postgres

- Relational database async support: databases

- Relational database migrations: Alembic

- Relational ORM: SQLAlchemy

- Data parsing and validation: Pydantic

- Testing: Pytest

- Static type checker: Mypy


## Running
```
docker-compose up
```

Swagger: http://localhost:8000/docs


Endpoints: 
  - create-user POST http://localhost:8000/v1/user/
  - create-wallet POST http://localhost:8000/v1/wallet/
  - deposit POST http://localhost:8000/v1/wallet/deposit/
  - transfer POST http://localhost:8000/v1/wallet/transfer/
