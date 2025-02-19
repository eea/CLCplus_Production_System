# CLCplus Backbone System

CLCplus Backbone System and Data Dissemination API.

*powered by*

![Figure 1:GeoVille Logo](01_Documentation/img/geoville_logo_150.png)

## Introduction

This repository provides all components, descriptions, configurations, sources and manuals of the CLCplus backbone system and data dissemination API.

### 1. Documentation

Product specification and user manual.

### 2. Authorization API

User Authentication, Authorization, and Management is done with the Authorization API connected with Keycloak.

Keycloak serves as the central authorization server that enables user authentication, authorization, and management,
based on the OAuth2 and OpenID Connect (OIDC) frameworks. It facilitates secure data exchange between clients and
servers by leveraging robust authorization mechanisms.

Keycloak's API provides a comprehensive set of endpoints required to perform essential authorization operations and flows.

### 3-4. Service and Products API

The Python based API gateway sits between the client and a collection of backend
services and serves as the entry point to the microservice infrastructure.
Hence, it communicates with Airflow and triggers the processes that compute and
retrieve the raster and vector products.
The RESTful API accepts all application programming interface (API) calls,
aggregates the various services required to fulfil them, and returns the appropriate result.
Moreover, it provides all endpoints which are required to interact with the system. The endpoints are divided into
namespaces or sections to group common operations (e.g.: geo-services, custom-relation-management
services, etc.). While the endpoints for processes are
within the 'section' namespace, the retrieval of the products is within the
'products' section of the API.

### 5. Airflow

Apache Airflow is a workflow management platform and is used to create data pipelines. This repository provides the configuratin of the airflow instance and the Airflow workers.

### 6. Airflow DAGs

This section contains the source codes of the Airflow Directed Acyclic Graphs (DAGs).
A DAG (Directed Acyclic Graph) is the core concept of Airflow,
collecting Tasks together, organized with dependencies and relationships
to say how they should run. To put it in a nutshell, a DAG is a Python based
workflow description while each Task within this workflow can be a containerized
application (Docker), a Bash Command or simply a Python function.

### 7. Database

Any modern backend solution needs a storage system to store data whilst processing particular tasks. As spatial information will be processed in the project, the tool chosen was a PostgreSQL database server with its extension PostGIS for spatial operations. A relational database model is required to persist the processed information in a structured manner. This directory provides database DDL files and database models.

### 8. Monitoring & Logging

The system monitoring is based on the Grafana software. Grafana is a multi-platform analytics and visualization tool. It provides charts, graphs, metrics, logs, traces and for monitoring the health state of a system.

The logging module is used to log and monitor all relevant messages of the backbone processing system. The moduel T module supports different log levels (INGO, WARNING, ERROR). It's written in Python and the module architecture is based on a message queueing system (RabbitMQ).

### 9. Additional Python Modules

The system architecture also includes helper functions and modules
to avoid duplicated code and a modular microservice infrastructure.  
The modules are:  

* **Vault Module**:
  The vault module is used to interact with the Vault Secrets Management Backend.  
  
* **Database Module**:  
  This module allows every interaction with a database. This includes reading, 
  writing and updating rows, but also much more.
  
* **Keycloack Module**:  
The Keycloak Module is used to interact with Keycloak for Identiy and Access Management.

### 10. System Components (third party software licenses)

List of all software modules and their licence models.
