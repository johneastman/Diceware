import random

class Diceware:

    def __init__(self):
        self.passwords = {}
        
        self.load()
        
        
    def generate(self, num_words, delimiter):
        '''
        Generate a password.
        '''
        password = ""
        for i in range(num_words):
            
            key = ""
            for j in range(5):
                key += str(random.randint(1, 6))
            
            if i != num_words - 1:
                password += self.passwords[key] + delimiter
            else:
                password += self.passwords[key]
            
        return password
        
        
    def load(self):
        '''
        Load data from "diceware.wordlist.asc" into memory. Create a 
        dictionary that pairs the code with a string of characters. 
        '''
        with open("diceware.wordlist.asc", "r") as f:
    
            split_passwords = f.read().split("\n")
            
            for pair in split_passwords:
                key, value = pair.split("\t")
                self.passwords[key] = value
                
                
    def main(self):
        
        while True:
            
            _input = input(">>> ")
            
            if _input == "exit":
                break
            elif _input.startswith("g"):
                print(self.generate(4, " "))


if __name__ == "__main__":
    dw = Diceware()
    p = dw.generate(4, " ")
    print(p)