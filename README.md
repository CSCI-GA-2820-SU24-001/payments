# NYU DevOps Promotions Service

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://python.org/)
![Workflow](https://github.com/CSCI-GA-2820-SU24-001/promotions/actions/workflows/workflow.yml/badge.svg)

## Overview

The Promotions Service is a representation of special promotions or sales that are applied to a product or the entire store. Examples of promotions include "buy 1 get 1 free" and "20% off". Discount promotions typically apply for a given duration, such as a sale lasting for one week only.

## Project Setup

This project use docker container, VScode. To deploy locally, you can clone this repo, change into the repo directory then use "code ." to start the remote container in VScode ( remote connection extension is required).

These should be copied using a bash shell as follows:

```bash
    git clone https://github.com/CSCI-GA-2820-SU24-001/promotions.git
    cd promotions
    code .
```

## API Endpoints

### Table of Endpoints

| Endpoint               | HTTP Method | Description                                      |
|------------------------|-------------|--------------------------------------------------|
| `/promotions`          | `GET`       | Retrieve all promotions                          |
| `/promotions`          | `POST`      | Create a new promotion                           |
| `/promotions/<id>`     | `GET`       | Retrieve a promotion by its ID                   |
| `/promotions/<id>`     | `PUT`       | Update a promotion by its ID                     |
| `/promotions/<id>`     | `DELETE`    | Delete a promotion by its ID                     |
| `/promotions/name/<name>` | `GET`    | Retrieve promotions by their name                |

### Endpoints Description

- **`GET /promotions`**
  - Retrieves a list of all promotions in the database.
  - **Response Example**:
    ```json
    [
        {
            "promotion_id": 1,
            "promotion_name": "20% off",
            "promotion_description": "20% off on all products",
            "promotion_type": "PERCENTAGE",
            "promotion_scope": "ENTIRE_STORE",
            "start_date": "2024-01-01T00:00:00",
            "end_date": "2024-01-07T23:59:59",
            "promotion_value": 20.0,
            "promotion_code": "SAVE20",
            "created_by": "uuid",
            "modified_by": "uuid",
            "created_when": "2024-01-01T00:00:00",
            "modified_when": "2024-01-01T00:00:00"
        }
    ]
    ```

- **`POST /promotions`**
  - Creates a new promotion.
  - **Request Body Example**:
    ```json
    {
        "promotion_name": "20% off",
        "promotion_description": "20% off on all products",
        "promotion_type": "PERCENTAGE",
        "promotion_scope": "ENTIRE_STORE",
        "start_date": "2024-01-01T00:00:00",
        "end_date": "2024-01-07T23:59:59",
        "promotion_value": 20.0,
        "promotion_code": "SAVE20",
        "created_by": "uuid",
        "modified_by": "uuid",
        "created_when": "2024-01-01T00:00:00",
        "modified_when": "2024-01-01T00:00:00"
    }
    ```

- **`GET /promotions/<id>`**
  - Retrieves a promotion by its ID.
  - **Response Example**:
    ```json
    {
        "promotion_id": 1,
        "promotion_name": "20% off",
        "promotion_description": "20% off on all products",
        "promotion_type": "PERCENTAGE",
        "promotion_scope": "ENTIRE_STORE",
        "start_date": "2024-01-01T00:00:00",
        "end_date": "2024-01-07T23:59:59",
        "promotion_value": 20.0,
        "promotion_code": "SAVE20",
        "created_by": "uuid",
        "modified_by": "uuid",
        "created_when": "2024-01-01T00:00:00",
        "modified_when": "2024-01-01T00:00:00"
    }
    ```

- **`PUT /promotions/<id>`**
  - Updates a promotion by its ID.
  - **Request Body Example**:
    ```json
    {
        "promotion_name": "25% off",
        "promotion_description": "25% off on all products",
        "promotion_type": "PERCENTAGE",
        "promotion_scope": "ENTIRE_STORE",
        "start_date": "2024-01-01T00:00:00",
        "end_date": "2024-01-07T23:59:59",
        "promotion_value": 25.0,
        "promotion_code": "SAVE25",
        "created_by": "uuid",
        "modified_by": "uuid",
        "created_when": "2024-01-01T00:00:00",
        "modified_when": "2024-01-01T00:00:00"
    }
    ```

- **`DELETE /promotions/<id>`**
  - Deletes a promotion by its ID.
  - **Response Example**:
    ```json
    {
        "message": "Promotion with id 1 was deleted successfully"
    }
    ```

- **`GET /promotions/name/<name>`**
  - Retrieves promotions by their name.
  - **Response Example**:
    ```json
    [
        {
            "promotion_id": 1,
            "promotion_name": "20% off",
            "promotion_description": "20% off on all products",
            "promotion_type": "PERCENTAGE",
            "promotion_scope": "ENTIRE_STORE",
            "start_date": "2024-01-01T00:00:00",
            "end_date": "2024-01-07T23:59:59",
            "promotion_value": 20.0,
            "promotion_code": "SAVE20",
            "created_by": "uuid",
            "modified_by": "uuid",
            "created_when": "2024-01-01T00:00:00",
            "modified_when": "2024-01-01T00:00:00"
        }
    ]
    ```

These API endpoints allow users to manage promotions effectively, including creating, retrieving, updating, and deleting promotions.


## Contents

The project contains the following:

```text
.gitignore          - this will ignore vagrant and other metadata files
.flaskenv           - Environment variables to configure Flask
.gitattributes      - File to gix Windows CRLF issues
.devcontainers/     - Folder with support for VSCode Remote Containers
dot-env-example     - copy to .env to use environment variables
pyproject.toml      - Poetry list of Python libraries required by your code

service/                   - service python package
├── __init__.py            - package initializer
├── config.py              - configuration parameters
├── models.py              - module with business models
├── routes.py              - module with service routes
└── common                 - common code package
    ├── cli_commands.py    - Flask command to recreate all tables
    ├── error_handlers.py  - HTTP error handling code
    ├── log_handlers.py    - logging setup code
    └── status.py          - HTTP status constants

tests/                     - test cases package
├── __init__.py            - package initializer
├── factories.py           - Factory for testing with fake objects
├── test_cli_commands.py   - test suite for the CLI
├── test_models.py         - test suite for business models
└── test_routes.py         - test suite for service routes
```

## License

Copyright (c) 2016, 2024 [John Rofrano](https://www.linkedin.com/in/JohnRofrano/). All rights reserved.

Licensed under the Apache License. See [LICENSE](LICENSE)

This repository is part of the New York University (NYU) masters class: **CSCI-GA.2820-001 DevOps and Agile Methodologies** created and taught by [John Rofrano](https://cs.nyu.edu/~rofrano/), Adjunct Instructor, NYU Courant Institute, Graduate Division, Computer Science, and NYU Stern School of Business.
