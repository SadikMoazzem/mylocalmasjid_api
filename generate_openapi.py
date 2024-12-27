import json
from mylocalmasjid_api.app import app

# Generate OpenAPI schema
openapi_schema = app.openapi()

# Write to file with proper formatting
with open('openapi.json', 'w') as f:
    json.dump(openapi_schema, f, indent=2) 