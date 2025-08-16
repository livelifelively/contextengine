# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install uv for package management
RUN pip install uv

# Copy the requirements files
COPY pyproject.toml uv.lock ./

# Install any needed packages specified in pyproject.toml
RUN uv pip install --system .

# Copy the rest of the application's code
COPY src/ /app/src/

# Make port 8008 available to the world outside this container
EXPOSE 8008

# Run the application
CMD ["python", "-m", "src.context_engine.main"]
