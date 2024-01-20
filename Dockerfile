# Use a Python base image
FROM python:3.10.12

# Set the working directory inside the container
WORKDIR /app

# Copy the contents of your app to the container's working directory
COPY . /app

# Install required dependencies from requirements.txt
RUN pip install --upgrade pip   

RUN pip install -r requirements.txt

# Expose the port that dash uses
EXPOSE 8050

# Run Voilà when the container starts
CMD ["python", "app.py"]