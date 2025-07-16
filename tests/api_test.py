import random
from http import HTTPStatus
import pytest
from faker import Faker
import requests
import sys
import traceback
import json

import data
from pages.api_page import ApiPage
from pages.main_page import MainPage
from data.test_data import Test_data

@pytest.mark.usefixtures("setup_api_class")
class TestAPI:

    def setup_method(self):
        """Run before each test method"""
        print("\n--- API Test Setup ---")
        # Check if api_page is available from fixture
        if not hasattr(self, 'api_page'):
            print("Warning: api_page not found from fixture, creating manually")
            self.api_page = ApiPage(base_url=Test_data.Base_URL)

        print(f"Using API URL: {self.api_page.base_url}")

    def test_01_get_hotel(self):
        """Test GET hotels endpoint"""
        print("\n--- Running test_01_get ---")
        try:
            # Make the API call
            response = self.api_page.get_hotels()

            # Check if response is None (connection failed)
            if response is None:
                pytest.fail("API request failed - got None response")

            # Check status code
            assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

            # Try to parse JSON
            try:
                data = response.json()
                print(f"API returned JSON data successfully")

                # Basic validation
                assert isinstance(data, dict), "Response is not a dictionary"
                print(f"Data keys: {list(data.keys())}")

            except Exception as e:
                print(f"Failed to parse response as JSON: {e}")
                print(f"Response content: {response.text[:500]}")
                pytest.fail("Failed to parse response as JSON")

            return data

        except Exception as e:
            print(f"Unexpected error in test_01_get: {e}")
            traceback.print_exc(file=sys.stdout)
            pytest.fail(f"Test failed with exception: {e}")

    def test_02_get_hotel_by_id(self):
        """Test GET hotel by ID endpoint"""
        print("\n--- Running test_02_get_hotel_by_id ---")
        try:
            # Get all hotels first to find an ID
            hotels_response = self.api_page.get_hotels()

            # Make sure we got a valid response
            if hotels_response is None:
                pytest.skip("Skipping test - couldn't get hotel list")

            # Make sure status code is good
            if hotels_response.status_code != 200:
                pytest.skip(f"Skipping test - got status code {hotels_response.status_code}")

            # Parse the response
            hotels_data = hotels_response.json()

            # Make sure we have at least one hotel
            assert "totalElements" in hotels_data, "Response missing totalElements field"
            assert "content" in hotels_data, "Response missing content field"
            assert hotels_data["totalElements"] > 0, "No hotels available to test"
            assert len(hotels_data["content"]) > 0, "No hotel content available"

            # Get the first hotel's ID
            hotel_id = hotels_data["content"][0]["id"]
            hotel_name = hotels_data["content"][0]["name"]

            print(f"Testing hotel: id={hotel_id}, name={hotel_name}")

            # Test the get_hotel method
            self.api_page.test_get_hotel(hotel_id, hotel_name)
            print(f"Successfully retrieved hotel with ID {hotel_id} and name {hotel_name}")

        except Exception as e:
            print(f"Unexpected error in test_02_get_hotel_by_id: {e}")
            traceback.print_exc(file=sys.stdout)
            pytest.fail(f"Test failed with exception: {e}")


    def test_03_post_hotel(self):
        """Test POST hotel endpoint"""
        print("\n--- Running test_03_post_hotel ---")
        try:
            # Generate random hotel data
            fake = Faker()
            new_hotel = {
                "name": fake.company(),
                "city": fake.city(),
                "address": fake.address(),
                "rating": random.randint(1, 5),
                "price": random.randint(100, 500)
            }

            print(f"Posting new hotel: {new_hotel}")

            # Call the API to create a new hotel with updated method
            response = self.api_page.test_post(new_hotel)

            # Check if response is None (connection failed)
            if response is None:
                pytest.fail("API request failed - got None response")

            # Validate the response
            assert response.status_code == HTTPStatus.CREATED, f"Expected status code {HTTPStatus.CREATED}, got {response.status_code}"

            # Check if the response has data
            if response.text:
                try:
                    response_data = response.json()
                    if isinstance(response_data, dict):
                        # Verify the hotel was created with our data
                        assert response_data.get("name") == new_hotel["name"], "Hotel name doesn't match"
                        assert response_data.get("city") == new_hotel["city"], "Hotel city doesn't match"
                        print(f"Hotel created successfully with ID: {response_data.get('id')}")
                except json.JSONDecodeError:
                    print("Warning: Could not parse response as JSON")

            print("Hotel created successfully")

        except Exception as e:
            print(f"Unexpected error in test_03_post_hotel: {e}")
            traceback.print_exc(file=sys.stdout)
            pytest.fail(f"Test failed with exception: {e}")


    def test_04_delete_single_hotel(self):
        """Test DELETE single hotel endpoint"""
        print("\n--- Running test_04_delete_single_hotel ---")
        try:
            # Get all hotels first to find an ID
            hotels_response = self.api_page.get_hotels()

            # Make sure we got a valid response
            if hotels_response is None:
                pytest.skip("Skipping test - couldn't get hotel list")

            # Make sure status code is good
            if hotels_response.status_code != 200:
                pytest.skip(f"Skipping test - got status code {hotels_response.status_code}")

            # Parse the response
            hotels_data = hotels_response.json()

            # Make sure we have at least one hotel
            assert "totalElements" in hotels_data, "Response missing totalElements field"
            assert "content" in hotels_data, "Response missing content field"
            assert hotels_data["totalElements"] > 0, "No hotels available to test"
            assert len(hotels_data["content"]) > 0, "No hotel content available"

            # Get the first hotel's ID
            hotel_id = hotels_data["content"][0]["id"]

            print(f"Testing deletion of hotel with ID {hotel_id}")

            # Test the delete method
            self.api_page.test_delete_single_hotel()
            print(f"Successfully deleted hotel with ID {hotel_id}")

        except Exception as e:
            print(f"Unexpected error in test_04_delete_single_hotel: {e}")
            traceback.print_exc(file=sys.stdout)
            pytest.fail(f"Test failed with exception: {e}")
