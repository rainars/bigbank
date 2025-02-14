# 🏦 BigBank Loan Calculator API Tests

Automated API tests for the **BigBank Loan Calculator**, ensuring accuracy, reliability, and compliance of loan calculations.  
These tests run inside a **Docker container via GitHub Actions**, and generate **Allure Reports** for easy analysis.

---

## ✅ Key Features
- 🚀 **Runs in Docker (GitHub Actions)** – No local setup required
- 📊 **Loan Calculation Accuracy** – Verifies monthly payments, APRC, fees
- 🛠 **Allure & HTML Reports** – Easy test analysis & debugging

## ⚙️ CI/CD Pipeline (GitHub Actions)

✅ **GitHub Actions Workflow** - [View Here](https://github.com/rainars/test/actions)  
The tests are automatically executed **inside Docker** on every **push/pull request** to the repository.

### 📌 Steps:
1. 🏗 **Builds Docker Image**
2. 🏃 **Runs API Tests using Behave**
3. 📊 **Generates Allure & HTML Reports**
4. 🚀 **Deploys Reports to GitHub Pages**: [Live Report](https://rainars.github.io/bigbank/#)

---

## 🛠 Running Tests Locally (Docker)

To run the tests **inside Docker** without setting up dependencies locally:

```sh
# 1️⃣ Build the Docker container
docker build -t bigbank-tests .

# 2️⃣ Run tests inside the container
docker run --rm bigbank-tests