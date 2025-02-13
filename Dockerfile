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

# Set the environment variable for Behave to find the "features" directory
ENV PYTHONPATH="/app"

# Debugging before executing tests
#CMD echo "Running tests..." && ls -la /app && xvfb-run --auto-servernum behave features/

# Run Behave tests when container starts
CMD ["behave", "--format=pretty", "--no-skipped", "--color", "features/"]