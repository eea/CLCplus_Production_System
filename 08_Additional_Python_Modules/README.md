# Additional Python Modules

---

## Contributors

* Johannes Schmid
* Michel Schwandner
* Rafael Reder

## Database Module

This module abstracts a PostgreSQL database connector and provides several functions to read from and
write into tables. The provided methods are:

 * read one row from a query
 * read all rows from a query
 * read many (a specific number of) rows from a query
 *execute commands such as insert, update, create, drop, delete, etc

---

## Vault Module

The vault module is a Python module which simplifies retrieving secrets from the Vault secrets management backend.
It returns the secrets stored under a given path when the correct login parameters are provided.

---

## Keycloak Module

This Python module provides the basic implementation to interact with Keycloak.
It allows the backend to do all Identity and Access Management related tasks.

---
