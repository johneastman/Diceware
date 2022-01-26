import unittest
from unittest.mock import patch
import string

import requests

from check_password import check_password


class CheckPasswordTest(unittest.TestCase):

    mock_hash = string.ascii_lowercase
    expected_occurrences = 22

    def get_mock_response_object(self, status_code, body):
        response = requests.Response()
        response.status_code = status_code
        response._content = body.encode("utf-8")
        return response

    @patch("check_password.requests.get")
    @patch("check_password.get_password_hash")
    def test_check_password_when_password_pwned(self, mock_password_hash, mock_response):
        mock_password_hash.return_value = self.mock_hash
        mock_response.return_value = self.get_mock_response_object(200, f"{self.mock_hash[5:]}:{self.expected_occurrences}\n")

        actual_occurrences = check_password("password")

        self.assertEqual(self.expected_occurrences, actual_occurrences)

    @patch("check_password.requests.get")
    @patch("check_password.get_password_hash")
    def test_check_password_when_password_not_pwned(self, mock_password_hash, mock_response):
        mock_password_hash.return_value = string.ascii_uppercase
        mock_response.return_value = self.get_mock_response_object(
            200, f"{self.mock_hash[5:]}:{self.expected_occurrences}\n")

        actual_occurrences = check_password("password")

        self.assertEqual(0, actual_occurrences)

    @patch("check_password.requests.get")
    @patch("check_password.get_password_hash")
    def test_check_password_when_response_not_200(self, mock_password_hash, mock_response):
        mock_status_code = 404
        mock_response_body = "not found"

        mock_password_hash.return_value = self.mock_hash

        # Setup mock response object with status code and text (via _content) set
        mock_response.return_value = self.get_mock_response_object(mock_status_code, mock_response_body)

        with self.assertRaises(Exception) as context:
            check_password("password")

        expected_error_message = f"URL: https://api.pwnedpasswords.com/range/{self.mock_hash[:5]}; "
        expected_error_message += f"Status Code: {mock_status_code}; "
        expected_error_message += f"Body: {mock_response_body}"

        self.assertEqual(expected_error_message, str(context.exception))


if __name__ == "__main__":
    unittest.main()
