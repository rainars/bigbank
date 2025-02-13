# Use Python base image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy all files into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright dependencies
RUN apt-get update && apt-get install -y xvfb
RUN playwright install --with-deps

# Install Allure Behave formatter
RUN pip install allure-behave

# Set the environment variable for Behave to find the "features" directory
ENV PYTHONPATH="/app"

# Run Behave tests when container starts
CMD ["behave", "--format=pretty", "--no-skipped", "--color", "features/"]
