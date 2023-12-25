# Use an official Python runtime as a parent image
FROM python:3.11

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /finance_app

# Copy the Poetry files to the working directory
COPY pyproject.toml poetry.lock .

# Install Poetry and project dependencies
RUN pip install poetry && poetry config virtualenvs.create false && poetry install

# Copy the Django project files to the working directory
COPY . /finance_app/

# Copy the entrypoint script into the container
COPY entrypoint.sh /finance_app/entrypoint.sh

# Grant execute permissions to the entrypoint script
RUN chmod +x /finance_app/entrypoint.sh

# Set the entry point to the script
ENTRYPOINT ["/finance_app/entrypoint.sh"]
