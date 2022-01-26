import unittest
from unittest.mock import patch
import string
import random

import requests

from check_password import check_password


class CheckPasswordTest(unittest.TestCase):

    def get_mock_data(self):
        return string.ascii_lowercase, 22

    @patch("check_password.get_response_body")
    @patch("check_password.get_password_hash")
    def test_check_password_when_password_pwned(self, mock_password_hash, mock_response_body):
        mock_hash, expected_occurrences = self.get_mock_data()
        mock_password_hash.return_value = mock_hash
        mock_response_body.return_value = f"{mock_hash[5:]}:{expected_occurrences}\n"

        actual_occurrences = check_password("password")

        self.assertEqual(expected_occurrences, actual_occurrences)

    @patch("check_password.get_response_body")
    @patch("check_password.get_password_hash")
    def test_check_password_when_password_not_pwned(self, mock_password_hash, mock_response_body):
        mock_hash, expected_occurrences = self.get_mock_data()
        mock_password_hash.return_value = string.ascii_uppercase
        mock_response_body.return_value = f"{mock_hash[5:]}:{expected_occurrences}\n"

        actual_occurrences = check_password("password")

        self.assertEqual(0, actual_occurrences)

    @patch("check_password.requests.get")
    @patch("check_password.get_password_hash")
    def test_check_password_when_response_not_200(self, mock_password_hash, mock_response):
        mock_status_code = 404
        mock_response_body = "not found"

        mock_hash, expected_occurrences = self.get_mock_data()
        mock_password_hash.return_value = mock_hash

        # Setup mock response object with status code and text (via _content) set
        mock_response_object = requests.Response()
        mock_response_object.status_code = mock_status_code
        mock_response_object._content = mock_response_body.encode("utf-8")
        mock_response.return_value = mock_response_object

        with self.assertRaises(Exception) as context:
            check_password("password")

        expected_error_message = f"URL: https://api.pwnedpasswords.com/range/{mock_hash[:5]}; "
        expected_error_message += f"Status Code: {mock_status_code}; "
        expected_error_message += f"Body: {mock_response_body}"

        self.assertEqual(expected_error_message, str(context.exception))


if __name__ == "__main__":
    unittest.main()
