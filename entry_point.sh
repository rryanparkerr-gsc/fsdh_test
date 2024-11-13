#/bin/bash

uvicorn app.api:app --host 127.0.0.1 --port 8000
# uvicorn app.api:app --reload