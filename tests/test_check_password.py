"""A command-line tool for generating passwords using the Diceware method.

MIT License

Copyright (c) 2018 John Eastman

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Note: setting a list to mock_object.side_effect allows the mocked method to return each subsequent value every time
it is called. For example, the first time the method is called, the value returned will be the 0th element, the second
time the 1st element, etc.'
"""
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
