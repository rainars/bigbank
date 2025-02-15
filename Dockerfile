# Use Python base image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy all files into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright and required browsers
RUN pip install playwright
RUN playwright install --with-deps

# Install behave-html-formatter for HTML reports
RUN pip install behave-html-formatter

# Set environment variable for Behave
ENV PYTHONPATH="/app"

# Run Behave tests and generate an HTML report
#CMD ["behave", "--format=behave_html_formatter:HTMLFormatter", "--outfile=/app/test-reports/report.html"]
CMD ["behave", "--format=behave_html_formatter:HTMLFormatter", "--outfile=/app/test-reports/report.html", "--format=allure_behave.formatter:AllureFormatter", "-o", "/app/test-reports/allure-results"]
