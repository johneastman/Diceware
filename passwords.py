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
import argparse
import json
import os
import re
import requests
import secrets

from check_password import check_password


def is_pwned(passphrase) -> bool:
    if len(passphrase) <= 0:
        raise Exception("Length of passphrase must be longer than 0")
    return check_password(passphrase) > 0


def generate_passphrase(num_words, delimiter):
    """Generate a passphrase using the Diceware algorithm.

    This passphrase will have 'self.num_words' words in it, delimited by 'self.delimiter'.

    :return: the generated passphrase
    :rtype: str
    """
    passwords = get_passwords()

    words = []
    for _ in range(num_words):
        # Generate a 5-character string of numbers from 1 to 6 (inclusive)
        # Note: 'secrets.randbelow(6)' generates a number between 0 and 5, but because the dice rolls are from 1 to 6,
        # we need to add one to the number returned by that method.
        key = "".join(str(secrets.randbelow(6) + 1) for _ in range(5))
        words.append(passwords[key])

    # Join each word in 'words' together, delimited by 'delimiter'
    return delimiter.join(words)


def get_passwords():
    """Load password, die-roll pairs from the given file.

    Passphrases and associated die-rolls are put in 'self.passwords'.
    """
    file_path = os.path.join(os.path.dirname(__file__), "words.json")

    if os.path.exists(file_path):
        print("Loading words from local file...")
        with open(file_path, "r") as file:
            data = json.load(file)
        return data

    print("Retrieving words from the web...")
    response = requests.get("https://theworld.com/%7Ereinhold/diceware.wordlist.asc")
    if response.status_code != 200:
        raise Exception("Failed to retrieve diceware word list.")
    lines = response.text.splitlines()
    words = [line.strip().split() for line in lines if re.search("^\\d{5}", line)]

    data = {key: value for (key, value) in words}
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)
    return data


def setup_parser():
    parser = argparse.ArgumentParser(
        description="A utility for generating passwords and checking if passwords have been leaked")

    parser.add_argument("-n", type=int, default=5,
                        help="The number of words in the passphrase")

    parser.add_argument("-d", type=str, default=" ",
                        help="The delimiter that goes between each word")

    parser.add_argument("-c", type=str, default="",
                        help="Check if a password has been leaked via the Pwned Passwords api")

    return parser


if __name__ == "__main__":
    parser = setup_parser()
    args = parser.parse_args()

    if len(args.c) > 0:
        # checking if a given password has been pwned
        print(is_pwned(args.c))
    else:
        # Generating a new password
        passphrase = generate_passphrase(args.n, args.d)
        print(passphrase)
