# Use Python base image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy all files into the container
COPY . /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    xvfb \
    libnss3 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm-dev \
    libasound2 \
    libpangocairo-1.0-0 \
    libatk1.0-0 \
    --no-install-recommends && rm -rf /var/lib/apt/lists/*

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright & its dependencies
RUN playwright install --with-deps

# Ensure `greenlet` is installed (Fix for "No module named greenlet._greenlet")
RUN pip install --force-reinstall greenlet

# Copy tests explicitly (ensures they exist)
COPY tests /app/tests

# Set the environment variable for Behave to find the "features" directory
ENV PYTHONPATH="/app"

# Debugging step to verify dependencies before running tests
RUN python -c "import playwright.sync_api; print('✅ Playwright Installed Successfully')"

# Run Behave tests with xvfb to support headless mode
CMD ["xvfb-run", "--auto-servernum", "behave", "--format=pretty", "--no-skipped", "--color", "features/"]
