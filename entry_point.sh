#/bin/bash

uvicorn app.api:app --host 0.0.0.0 --port 8080
# uvicorn app.api:app --reload