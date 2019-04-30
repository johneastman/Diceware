# Diceware
This is an implementation of the Diceware password generation methodology. This process involves rolling a six-sided die six times to generate a six-digit identifier, which is paired with a word in [diceware.txt](https://github.com/johneastman/Diceware/blob/master/diceware.txt). After completing this process five, the generated words are join together and separated by a delimiter ([source](http://world.std.com/~reinhold/diceware.html)).

I learned about Diceware from this Computerphile video (check out their channel [here](https://www.youtube.com/channel/UC9-y-6csu5WGm29I7JiwpnA)):

[![Diceware & Passwords - Computerphile](https://img.youtube.com/vi/Pe_3cFuSw1E/0.jpg)](https://www.youtube.com/watch?v=Pe_3cFuSw1E "Diceware & Passwords - Computerphile")

[Here](http://world.std.com/~reinhold/diceware.html) is the Diceware Passphrase Home Page.

## Usage
This program is a simple command-line tool that has the following options:

| Command | Description |
|:-------:|:------------|
| -n | Change the number of words in the passphrase (defaults to 5). |
| -d | Delimiter character (defaults to space). |
| -c | Check if a given passphrase has been leaked. If no passphrase is provided, the generated password will be checked. This feature is provided by the [Pwned Passwords API](https://haveibeenpwned.com/Passwords). |

To generate a passphrase, use:
```
python password.py
```

To change the number of words used to generate the passphrase, use:
```
python password.py -n 7
```

To change the delimiting character, use:
```
python password.py -d @
```

Finally, to check if `password1`, for example, been leaked, use:
```
python password.py -c password1
```

## Output
This program will generate a report (see an example: `report.txt`) that contains the password and the number of times (if any) the specified password was found elsewhere online.
