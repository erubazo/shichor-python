# Shichor Automation Project

<img width="2529" height="1220" alt="image" src="https://github.com/user-attachments/assets/b9811da3-242c-4456-aeba-2ce6d07bc325" />


This project contains automated tests for the Shichor application. It uses Selenium for browser automation and Pytest as the test framework.

## Project Structure

The project is structured as follows:

-   `pages/`: Contains page object models.
    -   `base_page.py`: Base class for all page objects.
    -   `cookie_page.py`: Page object for handling cookies.
    -   `currency_page.py`: Page object for currency-related functionalities.
    -   `main_page.py`: Page object for the main page.
    -   `signin_page.py`: Page object for sign-in functionalities.
-   `tests/`: Contains test scripts.
    -   `base_test.py`: Base class for all tests, providing setup and teardown methods.
    -   `conftest.py`: Contains Pytest fixtures.
    -   `currency_test.py`: Tests for currency functionalities.
    -   `mainpage_test.py`: Tests for the main page functionalities.
    -   `sign_in_test.py`: Tests for sign-in functionalities.
-   `allure-results/`: Contains Allure test results (generated after test execution).

## Requirements

-   Python 3.7+
-   Selenium
-   Pytest
-   Faker
-   Requests
-   Allure (optional, for reporting)

## Setup

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd shichor-automation
    ```

2.  **Create a virtual environment (recommended):**

    ```bash
    python -m venv venv
    source venv/Scripts/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Running Tests

To run the tests, use the following command:

```bash
pytest tests/mainpage_test.py -v
pytest tests/sign_in_test.py -v
pytest tests/currency_test.pyy -v

