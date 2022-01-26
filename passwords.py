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
import secrets
import argparse

from check_password import check_password


class Diceware:

    def __init__(self, args):

        # Arguments from argparse
        self.num_words = args.n
        self.delimiter = args.d
        self.passphrase = args.c if len(args.c) > 0 else ""

        self.report_name = "report.txt"

        self.passwords = {}

        self.load()

    def check_pwned(self, passphrase):
        """Returns a formatted sentence stating the number of times a password
        was found to have been leaked (see 'check_password.py' for more info).
        """
        results = check_password(passphrase)
        num_times = results[0][1] if len(results) > 0 else "0"
        return f"'{passphrase}' was found {num_times} times elsewhere"

    def generate(self):
        """Generate info about a passphrase.

        If 'self.passphrase' is an empty string, generate a password and check
        if it has been pwned. Otherwise, just check if 'self.passphrase' has
        been pwned.
        """
        if len(self.passphrase) > 0:
            # Only check if a password has been pwned.
            text = self.check_pwned(self.passphrase)
        else:
            # Generate password and check if that password has been pwned.
            passphrase = self.generate_passphrase()
            pwned_message = self.check_pwned(passphrase)
            text = f"Your new passphrase: {passphrase}\n{pwned_message}"
        self.generate_report(text)

    def generate_passphrase(self):
        """Generate a passphrase.

        This passphrase will have 'self.num_words' words in it, delimited by
        'self.delimiter'.
        """
        words = []
        for _ in range(self.num_words):

            # Generate a 5-character string of numbers from 1 to 6 (inclusive)
            key = "".join(str(secrets.randbelow(6) + 1) for _ in range(5))
            words.append(self.passwords[key])

        # Join each word in 'words' together, delimited by 'delimiter'
        return self.delimiter.join(words)

    def generate_report(self, text):
        """Generate a report on a generated/given password."""
        with open(self.report_name, "w") as file:
            file.write(text)

    def load(self):
        """Load password, die-roll pairs from "diceware.txt".

        Passphrases and associated die-rolls are put in 'self.passwords'.
        """
        with open("diceware.txt", "r") as file:
            data = [line.strip().split(" ") for line in file.readlines()]
        self.passwords = {key: value for (key, value) in data}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generating random passwords")

    parser.add_argument("-n", type=int, default=5,
                        help="The number of words in the passphrase")

    parser.add_argument("-d", type=str, default=" ",
                        help="The delimiter that goes between each word")

    parser.add_argument("-c", type=str, default="",
                        help="Check if a password has been leaked via the Pwned Passwords api")

    args = parser.parse_args()

    dw = Diceware(args)
    dw.generate()
