# Use Python base image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy all files into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Allure Behave Plugin (Required for Allure reports)
RUN pip install allure-behave

# Install Playwright dependencies
RUN apt-get update && apt-get install -y xvfb
RUN playwright install --with-deps

# Set the environment variable for Behave to find the "features" directory
ENV PYTHONPATH="/app"

# Run Behave tests when container starts
CMD ["behave", "--format=pretty", "--no-skipped", "--color", "features/"]
