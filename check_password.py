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
    # Retrieve a hash of the password using SHA-1
    password_hash = hashlib.sha1(password_text.encode()).hexdigest().upper()

    # first: first 5 characters to be sent to the api for checking.
    # rest:  The remaining characters in the hash, which are checked to see if the
    #        password has been found elsewhere.
    first, rest = password_hash[:5], password_hash[5:]

    url = f"https://api.pwnedpasswords.com/range/{first}"

    # Retrieve all hashes that start with the characters in 'first'. The remaining
    # characters in the hashes are returned
    response = requests.get(url)

    # Put each hash and the number of times found in a list, and retrieve
    # the hash-frequency pairs matching the 'rest' hash
    results = [result.rstrip() for result in response.text.split("\n")]
    results = [result.split(":") for result in results]
    results = [result for result in results if result[0] == rest]

    # Return the hash-frequency pairs
    return results

if __name__ == "__main__":
    # Example of how this function can be used
    password = "wgouhaliwbeigubeaiuhb"
    results = check_password(password)

    '''
    if len(results) == 0:
        print(f"'{password}' was not found")
    else:
        for _, num_appearances in results:
            print(f"'{password}' was found {num_appearances} times")
    '''
