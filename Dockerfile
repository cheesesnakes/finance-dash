# Use a Python base image
FROM python:3.10.9

# Set the working directory inside the container
WORKDIR /app

# Copy the contents of your app to the container's working directory
COPY . /app

# Install required dependencies from requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that Voilà will use (default is 8866)
EXPOSE 8050

# Run Voilà when the container starts
CMD ["python", "app.py"]
