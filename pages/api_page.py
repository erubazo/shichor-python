import time
import datetime
import json
from http import HTTPStatus
import requests
from selenium.webdriver.common.by import By
from data.test_data import Test_data


class ApiPage:
    def __init__(self, driver=None, base_url=None):
        self.driver = driver
        # Use provided base_url or fall back to Test_data.Base_URL
        self.base_url = base_url if base_url is not None else Test_data.Base_URL
        print(f"API Page initialized with base URL: {self.base_url}")

        # Verify the API URL is valid on initialization
        self._verify_api_url()

        # Only initialize BasePage if a driver is provided
        if self.driver is not None:
            from pages.base_page import BasePage
            self.base_page = BasePage(driver)

    def _verify_api_url(self):
        """Verify that the API URL is valid and the service is running"""
        try:
            # Check if the URL format seems valid
            if not self.base_url.startswith(('http://', 'https://')):
                print(f"Warning: API URL may not be valid: {self.base_url}")

            # Try a HEAD request to check if the server is available
            try:
                print(f"Testing connection to API server at {self.base_url}...")
                response = requests.head(self.base_url, timeout=3)
                print(f"API server is available. Status: {response.status_code}")
            except requests.exceptions.ConnectionError:
                print(f"ERROR: Cannot connect to API server at {self.base_url}")
                print("Is your local API server running? Check that the service is started.")
            except Exception as e:
                print(f"Error checking API server availability: {e}")
        except Exception as e:
            print(f"Error verifying API URL: {e}")

    @property
    def main_page(self):
        if self.driver is None:
            raise ValueError("Driver is required to use main_page. Initialize ApiPage with a driver.")
        from pages.main_page import MainPage
        return MainPage(self.driver)

    def get_hotels(self):
        """Get hotel data from API"""
        try:
            print(f"Making API request to: {self.base_url}")
            response = requests.get(f"{self.base_url}", timeout=10)
            print(f"API Response status: {response.status_code}")

            # Log response headers and preview content
            print(f"Response Headers: {json.dumps(dict(response.headers), indent=2)}")

            if response.status_code == 200:
                try:
                    preview = response.json()
                    print(f"Response preview: {json.dumps(preview, indent=2)[:500]}...")
                except json.JSONDecodeError:
                    print(f"Response is not valid JSON. First 100 chars: {response.text[:100]}")
                except Exception as e:
                    print(f"Error parsing response: {e}")

            return response
        except requests.exceptions.ConnectionError as e:
            print(f"Connection Error: Could not connect to API at {self.base_url}")
            print(f"Error details: {e}")
            print("Make sure your API server is running at the specified URL.")
            return None
        except requests.exceptions.Timeout:
            print(f"Timeout Error: API at {self.base_url} took too long to respond")
            return None
        except Exception as e:
            print(f"Error getting hotel data: {e}")
            return None

    def test_get_hotels(self):
        response = requests.get(self.base_url)
        assert response.status_code == HTTPStatus.OK
        assert "application/json" in response.headers["Content-Type"]
        response_body = response.json()
        assert response_body["totalElements"] == 2

    def test_get_hotel(self,id: int, name: str):
        response = requests.get(f"{self.base_url}/{id}")
        response_body = response.json()
        assert response_body["name"] == name

    def test_post(self, json_data: dict):
        """
        Create a new hotel by sending POST request

        Args:
            json_data (dict): Hotel data to create

        Returns:
            requests.Response: Response object or None if failed
        """
        try:
            print(f"Sending POST request to {self.base_url}")
            print(f"Request data: {json.dumps(json_data, indent=2)}")

            # Set proper headers for JSON request
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }

            # Send the request with proper JSON encoding
            response = requests.post(
                self.base_url,
                data=json.dumps(json_data),  # Convert dict to JSON string
                headers=headers,
                timeout=10
            )

            print(f"POST response status: {response.status_code}")
            print(f"Response Headers: {json.dumps(dict(response.headers), indent=2)}")

            # Try to parse and log response data
            try:
                if response.text:
                    response_data = response.json()
                    print(f"Response data: {json.dumps(response_data, indent=2)[:500]}...")
                else:
                    print("Response body is empty")
            except json.JSONDecodeError:
                print(f"Response is not JSON. Content: {response.text[:200]}")

            # Check status code
            if response.status_code == HTTPStatus.CREATED:
                print("Hotel created successfully!")
            else:
                print(f"Warning: Expected status {HTTPStatus.CREATED}, got {response.status_code}")

            return response

        except requests.exceptions.ConnectionError as e:
            print(f"Connection Error: Could not connect to API at {self.base_url}")
            print(f"Error details: {e}")
            return None
        except Exception as e:
            print(f"Error in POST request: {e}")
            return None

    def test_delete_single_hotel(self):
        response = requests.get(self.base_url)
        response_body = response.json()
        total_elements = response_body["totalElements"]
        response = requests.delete(
            f"{self.base_url}/{response_body['content'][0]['id']}"
        )
        assert response.status_code == HTTPStatus.NO_CONTENT
        response_body = requests.get(self.base_url).json()
        assert response_body["totalElements"] == total_elements - 1
