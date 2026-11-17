# Security

The local demo is for development only. It intentionally does not implement authentication, refresh tokens, RBAC, encrypted source credentials, upload endpoints, audit trails or a production secret manager. Do not store real credentials in source control. Use `.env` locally and a managed secret store in deployed environments. Restrict network exposure and rotate all sample credentials.
