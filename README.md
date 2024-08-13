# NYU DevOps Promotions Service

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://python.org/)
![Workflow](https://github.com/CSCI-GA-2820-SU24-001/promotions/actions/workflows/workflow.yml/badge.svg)
![Codecov](https://codecov.io/github/CSCI-GA-2820-SU24-001/promotions/graph/badge.svg?)

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

## Contents

The project contains the following:

```text
.gitignore          - this will ignore vagrant and other metadata files
.flaskenv           - Environment variables to configure Flask
.gitattributes      - File to gix Windows CRLF issues
 Containers
dot-env-example     - copy to .env to use environment variables
pyproject.toml      - Poetry list of Python libraries required

.devcontainers/     - Folder with support for VSCode Remote
Dockerfile          - Docker image definition for this project
k8s/                - Kubernetes Deployment files
.tekton/            - Tekton CD pipeline files and definitions

service/                        - Main application code
├── __init__.py                 - package initializer
├── config.py                   - configuration parameters
├── models.py                   - module with business models
├── routes.py                   - module with service routes
├── common                      - common code package
│   ├── cli_commands.py         - Flask command to recreate all tables
│   ├── error_handlers.py       - HTTP error handling code
│   ├── log_handlers.py         - logging setup code
│   └── status.py               - HTTP status constants
└── static
    ├── css                     - CSS files
    ├── images                  - Image files
    ├── js
    │   ├── bootstrap.min.js    - Bootstrap library
    │   ├── jquery-3.6.0.min.js - jQuery library
    │   └── rest_api.js         - REST api calls to the backend used by the web interface
    └── index.html              - Main HTML file for the web interface
    
tests/                     - test cases package
├── __init__.py            - package initializer
├── factories.py           - Factory for testing with fake objects
├── test_cli_commands.py   - test suite for the CLI
├── test_models.py         - test suite for business models
└── test_routes.py         - test suite for service routes

features/                  - BDD Tests
├── steps
│   └── promotion_steps.py - step definitions
├── environment.py - BDD environment setup
└── promotions.feature - test definitions for BDD tests
```

## API Endpoints

### Table of Endpoints

| Endpoint               | HTTP Method | Description                                      |
|------------------------|-------------|--------------------------------------------------|
| `/api/health`          | `GET`       | Performs healthcheck on the service                         |
| `/api/promotions`          | `GET`       | Retrieve all promotions (supports query filters)                         |
| `/api/promotions`          | `POST`      | Create a new promotion                           |
| `/api/promotions/<id>`     | `GET`       | Retrieve a promotion by its ID                   |
| `/api/promotions/<id>`     | `PUT`       | Update a promotion by its ID                     |
| `/api/promotions/<id>`     | `DELETE`    | Delete a promotion by its ID                     |           |
| `/api/promotions/activate/<id>` | `PUT`    | Activate a promotion by its ID                |
| `/api/promotions/deactivate/<id>` | `PUT`    | Deactivate a promotion by its ID                |

#### Swagger API Documentation
For detailed documentation, please deploy the service and access the swagger docs at ```<service>/apidocs```

## Starting the service

### Starting the service locally
1. Ensure all dependencies are installed by running

``` 
poetry install 
```

2. The service can then be started by running 
```
honcho start
```

### Starting the service in a Kubernetes cluster

1. Create a Kubernetes cluster
```
make cluster
```
2. Build the Docker image
```
make build-image
```
3. Tag and push the Docker image to the cluster-registry
```
make push-image
```
4. Deploy the application and database to the cluster
```
make deploy
```

### Accessing the service locally
Once the service has been deployed, you can access it at ```http://localhost:8080```

## Run the Tests

### Unit Tests
Please ensure that postgres is running at port 5432 in the devcontainer

Tests can be run using the command
```
make test
```

### Integration Tests
Please ensure that the service and an instance of postgres is running before running integration tests.

Integration tests can be run using
```
behave
```

## License

Copyright (c) 2016, 2024 [John Rofrano](https://www.linkedin.com/in/JohnRofrano/). All rights reserved.

Licensed under the Apache License. See [LICENSE](LICENSE)

This repository is part of the New York University (NYU) masters class: **CSCI-GA.2820-001 DevOps and Agile Methodologies** created and taught by [John Rofrano](https://cs.nyu.edu/~rofrano/), Adjunct Instructor, NYU Courant Institute, Graduate Division, Computer Science, and NYU Stern School of Business.
