# Shichor Automation

This repository contains automated tests for the Shichor web application using Python and popular testing frameworks. The project is organized for maintainability and scalability, supporting UI and functional testing.

<img width="1902" height="857" alt="image" src="https://github.com/user-attachments/assets/2bd45083-149e-405d-9782-32b26f323b7c" />

## Project Structure

```
config.ini                # Configuration file for environment variables and settings
requriements.txt          # Python dependencies

pages/                    # Page Object Model classes
    base_page.py
    cookie_page.py
    currency_page.py
    main_page.py
    signin_page.py
    ...

tests/                    # Test cases
    base_test.py
    conftest.py
    currency_test.py
    mainpage_test.py
    sign_in_test.py
    ...

utils/                    # Utility modules
    config.py
    ...

data/                     # Test data files
```

## Getting Started

### Prerequisites
- Python 3.10+
- Google Chrome (or compatible browser)
- ChromeDriver (if using Selenium)
- Selenium WebDriver

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/shichor-automation.git
   cd shichor-automation
   ```
2. Install dependencies:
   ```bash
   pip install -r requriements.txt
   ```
3. Configure environment variables in `config.ini` as needed.

### Running Tests
To run all tests in the `tests/` directory:
```bash
pytest tests/
```
To run a specific test file:
```bash
pytest tests/mainpage_test.py
pytest tests/currency_test.py
pytest tests/sign_in_test.py
```
To generate Allure results:
```bash
pytest --alluredir=results
```
To view Allure reports:
```bash
allure serve results
```

## Key Features
- Page Object Model for maintainable test code
- Selenium WebDriver for browser automation
- Allure reporting integration
- Modular test structure
- Easy configuration via `config.ini`
