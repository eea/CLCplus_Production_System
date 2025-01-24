# Authorization API

---

## Contributors
* Michel Schwandner
* Rafael Reder

## General Description
User authentication, authorization, and management are now based on the Keycloak Identity
and Access Management framework. Keycloak provides a comprehensive platform for securing
applications and services with support for OAuth 2.0 and OpenID Connect protocols.
It enables third-party applications to obtain limited access to HTTP services on behalf
of a resource owner by facilitating an approval interaction between the resource owner
and the HTTP service. Additionally, Keycloak can allow third-party applications to gain
access on their own behalf.

Keycloak acts as the Authorization Server and provides endpoints for managing
authorization flows, issuing tokens, refreshing tokens, and revoking tokens.
When a resource owner (user) authenticates, Keycloak issues an access token to the client.

## What it offers
* Authorisation and authentication
* Token generation
* Creating OAuth clients
* User login
* Access token generation
* Token validation
* Scopes creation and management
