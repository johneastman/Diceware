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
import requests
import hashlib


def check_password(password_text):
    """Check whether a password has been leaked.

    Passwords are checked using the haveibeenpwned password api:
    https://haveibeenpwned.com/Passwords
    """
    # Retrieve a hash of the password text using SHA-1
    password_hash = get_password_hash(password_text)

    # first: first 5 characters to be sent to the api for checking.
    # rest:  The remaining characters in the hash, which are checked to see if the
    #        password has been found elsewhere.
    first, rest = password_hash[:5], password_hash[5:]

    # Retrieve all hashes that start with the characters in 'first'. The remaining
    # characters in the hashes are returned
    response_body = get_response_body(f"https://api.pwnedpasswords.com/range/{first}")

    # Each hash-occurrence pair is on a new line, so split the string into a list where each element is a separate line
    hash_occurrences = list(filter(lambda l: len(l) == 2, [result.rstrip().split(":") for result in response_body.split("\n")]))

    # Create a dictionary matching all the hashes with their occurrences
    results = {rest_hash: int(occurrence) for rest_hash, occurrence in hash_occurrences}

    # Return the number of occurrences associated with the hash from the given password. If that hash is not in the
    # dictionary, return 0
    return results.get(rest, 0)


def get_password_hash(password):
    return hashlib.sha1(password.encode()).hexdigest().upper()


def get_response_body(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"URL: {url}; Status Code: {response.status_code}; Body: {response.text}")
    return response.text


if __name__ == "__main__":
    # Example of how this function can be used
    password = "password"
    num_occurrences = check_password(password)
    print(num_occurrences)
