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

EXPOSE 8080

# CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8080"]
