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
"""
import unittest
from unittest.mock import patch

from passwords import generate_passphrase, is_pwned, setup_parser


class PasswordsTest(unittest.TestCase):

    passwords = {"11111": "a", "22222": "b", "33333": "c"}

    @patch("passwords.secrets.randbelow")
    @patch("passwords.get_passwords")
    def test_generate_passphrase_with_one_word(self, mock_passwords, mock_number_generator):
        mock_passwords.return_value = self.passwords
        mock_number_generator.side_effect = [0, 0, 0, 0, 0]

        actual_passphrase = generate_passphrase(1, " ")
        self.assertEqual("a", actual_passphrase)

    @patch("passwords.secrets.randbelow")
    @patch("passwords.get_passwords")
    def test_generate_passphrase_with_two_words(self, mock_passwords, mock_number_generator):
        mock_passwords.return_value = self.passwords
        mock_number_generator.side_effect = [0, 0, 0, 0, 0, 2, 2, 2, 2, 2]

        actual_passphrase = generate_passphrase(2, " ")
        self.assertEqual("a c", actual_passphrase)

    @patch("passwords.secrets.randbelow")
    @patch("passwords.get_passwords")
    def test_generate_passphrase_with_custom_delimiter(self, mock_passwords, mock_number_generator):
        mock_passwords.return_value = self.passwords
        mock_number_generator.side_effect = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]

        actual_passphrase = generate_passphrase(2, "-")
        self.assertEqual("a-b", actual_passphrase)

    def test_is_pwned_when_passphrase_is_empty_string(self):
        with self.assertRaises(Exception) as context:
            is_pwned("")

        self.assertEqual("Length of passphrase must be longer than 0", str(context.exception))


if __name__ == "__main__":
    unittest.main()
