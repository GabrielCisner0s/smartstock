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
```
# The main responsibilities are separated into different layers:

API / Views — HTTP requests and responses
Serializers — data validation and serialization
Services — business logic and application workflows
Validators — business validation rules
Selectors — read-oriented queries
Repositories — database access abstraction
Models — database entities
Permissions — authorization rules

# Project Structure
```text
smartstock/
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── pagination.py
│
├── core/
│   ├── handlers.py
│   ├── services.py
│   └── api/
│       └── schemas.py
│
├── users/
│   ├── api/
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── managers.py
│   ├── models.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── services.py
│   └── tests/
│
├── products/
│   ├── api/
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── filters.py
│   ├── models.py
│   ├── permissions.py
│   ├── repositories.py
│   ├── selectors.py
│   ├── services.py
│   ├── validators.py
│   ├── migrations/
│   └── tests/
│
├── inventory/
│   ├── api/
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── models.py
│   ├── permissions.py
│   ├── repositories.py
│   ├── selectors.py
│   ├── serializers.py
│   ├── services.py
│   ├── validators.py
│   ├── migrations/
│   └── tests/
│
├── reports/
│   ├── api/
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── selectors.py
│   ├── services.py
│   └── tests/
│
├── pytest.ini
├── requirements.txt
├── schema.yml
├── .env.example
└── manage.py

```
# Technologies

Technology	Purpose
Python	Backend programming language
Django	Web framework
Django REST Framework	REST API development
PostgreSQL	Relational database
Simple JWT	Authentication
django-filter	API filtering
drf-spectacular	OpenAPI documentation
pytest	Automated testing
pytest-django	Django testing integration
Factory Boy / Faker	Test data generation
Git	Version control

# Authentication

SmartStock uses JWT authentication.

The authentication flow includes:
```text
Register
   |
   v
Login
   |
   v
Access Token + Refresh Token
   |
   v
Authenticated API requests
   |
   v
Refresh Token

```
# User Roles

The system supports three user roles:
```text
Role	Description
ADMIN	Administrative operations
SUPERVISOR	Inventory and management operations
EMPLOYEE	Regular operational access

Permissions are enforced at the API level using custom DRF permission
classes.

```
# Products

The product module provides CRUD operations and business rules for inventory
items.

Each product contains information such as:
```text

SKU
Name
Description
Category
Price
Current stock
Minimum stock
Status
Creation/update information
Soft deletion state

```
# Reports and Dashboards

SmartStock includes reporting functionality for inventory and system-level
information.

# Inventory dashboard

Provides inventory movement indicators such as:

Entries
Exits
Adjustments
Stock-related metrics

# General dashboard

Provides a general overview of relevant system information and product and
inventory metrics.

# API Documentation

SmartStock uses OpenAPI documentation generated with
drf-spectacular.

# Security

The project includes several security-related features:
```text
JWT authentication
Role-based permissions
Authenticated API by default
API throttling
Environment-based secrets
PostgreSQL database
Custom exception handling
Input validation
Protected inventory operations
Transactional stock updates

```
Sensitive configuration values are loaded from environment variables rather
than being stored directly in the source code.

# Design Principles

SmartStock was developed with emphasis on:
```text

Separation of concerns
Single responsibility
Reusable services
Explicit business rules
Testability
Database consistency
API documentation
Maintainable project structure

```
The architecture allows business logic to remain independent from HTTP
request handling as much as possible.

# Project Status

SmartStock currently provides a functional backend API for product,
category, inventory, authentication and reporting operations.

The project is being developed as a backend portfolio project with a focus
on Python and Django development.

# Roadmap

Future improvements may include:
```text

Docker support
CI/CD with GitHub Actions
Production deployment
Redis integration
Background tasks
Advanced inventory analytics
Automated API integration tests
Improved observability and logging
Frontend client
Role administration endpoints

```
# Author

Gabriel Alejandro Cisneros

Backend Developer / Programmer

# License

This project is currently intended as a portfolio and educational project.
```text


