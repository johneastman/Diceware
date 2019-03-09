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
import time
import argparse

class Diceware:

    def __init__(self, args):

        self.num_words = args.n
        self.delimiter = args.d
        self.add_char  = args.c

        self.passwords = {}

        # For added security, rolling two more digits allow for adding
        # one of the following characters into the passphrase.
        self.character_table = ["~", "!", "#", "$", "%", "^",
                                "&", "*", "(", ")", "-", "=",
                                "+", "[", "]", "\\", "{", "}",
                                ":", ";" "<", ">", "?", "/",
                                "0", "1", "2", "3", "4", "5",
                                "6", "7", "8", "9"]

        self.load()


    def generate(self):
        """Generate the passphrase.

        This passphrase will have 'self.num_words' words in it, delimited by
        'self.delimiter'.
        """
        words = []
        for _ in range(self.num_words):

            # Generate a 5-character string of numbers from 1 to 6 (inclusive)
            key = "".join(str(secrets.randbelow(6) + 1) for _ in range(5))
            words.append(self.passwords[key])

        # Join each word in 'words' together, delimited by 'delimiter'
        passphrase = self.delimiter.join(words)

        if self.add_char:
            # If the user chooses to add a random character in their passphrase,
            # Select a random character from the generated passphrase and replace
            # that character with a randomly-selected character from
            # 'self.character_table'
            passphrase = list(passphrase)
            index = secrets.randbelow(len(passphrase))
            passphrase[index] = self.get_special_character()
            passphrase = "".join(passphrase)

        return passphrase


    def get_special_character(self):
        """Return a character from 'self.character_table'."""
        return secrets.choice(self.character_table)


    def load(self):
        """Load password, die-roll pairs from "diceware.wordlist.asc".

        Passphrases and associated die-rolls are put in 'self.passwords'.
        """
        with open("diceware.txt", "r") as file:

            data = [line.strip().split(" ") for line in file.readlines()]
            self.passwords = {key:value for (key, value) in data}


    def show_stats(self):

        entropy = 12.9 * self.num_words

        if self.add_char:
            entropy += 10

        print(f"Diceware Method = {entropy} bits")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Generating random passwords")

    parser.add_argument("-n", type=int, default=5,
                        help="The number of words in the passphrase")

    parser.add_argument("-d", type=str, default=" ",
                        help="The delimiter that goes between each word")

    parser.add_argument("-c", action='store_true',
                        help="A special character should be inserted in the passphrase")

    parser.add_argument("-s", action='store_true',
                        help="Show stats about your generated password")

    args = parser.parse_args()

    dw = Diceware(args)
    p = dw.generate()
    print(p)
    dw.show_stats()
