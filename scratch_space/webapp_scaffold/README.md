# simple webapp scaffold

keep a high quality scaffold with all the necessary files and structure for a web application using FastAPI.

some inspiration can be taken from the following repository:
https://github.com/Pitrified/snap_fit/tree/feat/fastapi-scaffold/src/snap_fit/webapp

a difference from the above repository is that the settings should be compatible with the config/params structure used in the project
src/project_name/params/project_name_params.py --> will include an attribute for the webapp settings
src/project_name/params/webapp/... --> will include the value of the webapp settings, with prod/dev and local/render overrides
src/project_name/config/webapp/... --> will include the structure of the webapp settings

the app should be deployable to render, a sample render compatible app is available here:
https://github.com/render-examples/fastapi

high quality security practices should be followed, including but not limited to:
- input validation and sanitization
- secure handling of sensitive data
- protection against common web vulnerabilities (e.g., SQL injection, XSS, CSRF)
- use of HTTPS
- proper authentication and authorization mechanisms
- login and session management using google login
- rate limiting to prevent abuse

assume google client id is available as an environment variable, and provide instructions on how to set it up in the docs.
```
# Google OAuth Configuration
GOOGLE_CLIENT_ID=your_google_client_id_here
```

