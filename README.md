# SmartStock

![Python](https://img.shields.io/badge/Python-3.14-blue)
![Django](https://img.shields.io/badge/Django-6.0-green)
![Django REST Framework](https://img.shields.io/badge/DRF-REST%20Framework-red)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18-blue)
![Tests](https://img.shields.io/badge/tests-173%20passed-success)
![OpenAPI](https://img.shields.io/badge/OpenAPI-validated-orange)

SmartStock is a RESTful backend API for inventory and product management,
built with Django, Django REST Framework and PostgreSQL.

The project was designed as a backend portfolio project focused on clean
architecture, separation of responsibilities, authentication, authorization,
testing and API documentation.

---

## Overview

SmartStock provides a backend system for managing products, categories,
inventory movements and system reports.

The application exposes a REST API protected by JWT authentication and
role-based permissions.

The project follows a layered architecture that separates API concerns from
business logic and data access.

### Main features

- Product management
- Category management
- Inventory management
- Stock entry and exit operations
- Stock adjustments
- Low-stock detection
- Soft deletion and product restoration
- JWT authentication
- Role-based authorization
- Search, filtering and ordering
- Pagination
- Inventory reports
- Dashboard endpoints
- PostgreSQL database
- OpenAPI documentation
- Automated testing
- Transaction-safe inventory operations
- Custom exception handling
- API throttling

---

# Architecture

The project follows a layered backend architecture:

```text
                Client
                  |
                  v
            REST API / Views
                  |
                  v
              Serializers
                  |
                  v
               Services
                  |
        +---------+---------+
        |                   |
        v                   v
   Validators          Selectors
        |                   |
        +---------+---------+
                  |
                  v
             Repositories
                  |
                  v
             Django ORM
                  |
                  v
             PostgreSQL

