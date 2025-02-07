# Use a Python base image
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the contents of your app to the container's working directory
COPY . /app

# Install required dependencies from requirements.txt
RUN uv sync --frozen

# Expose the port that dash uses
EXPOSE 8050

# Run Voilà when the container starts
CMD ["uv", "run", "app.py"]