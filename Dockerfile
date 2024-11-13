# Choose our version of Python
FROM python:3.11

# Set up a working directory
WORKDIR /code

# Copy just the requirements into the working directory so it gets cached by itself
COPY ./requirements.txt /code/requirements.txt

# Install the dependencies from the requirements file
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the code into the working directory
COPY ./app /code/app

# CMD ["uvicorn", "app.api:app", "--host", "127.0.0.1", "--port", "8000"]
