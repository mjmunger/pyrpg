#!/usr/bin/env python3

import random
import sys
import mmap
import time


class rpg:
    # Default options are all false.

    use_upper = False
    use_lower = False
    use_symbol = False
    use_digits = False
    use_space = False
    use_brackets = False
    use_minus = False
    use_underline = False
    use_pattern = False
    use_words = False

    remove_homoglyphs = False

    list_upper = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
                  "U", "V", "W", "X", "Y", "Z"]

    list_lower = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
                  "u", "v", "w", "x", "y", "z"]

    list_symbol = ["!", "@", "#", "$", "%", "^", "&", "*"]
    list_digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    list_space = [" "]
    list_brackets = ["{", "}", "[", "]", "(", ")", "<", ">"]

    list_minus = ["-"]
    list_underline = ["_"]

    list_homoglyphs = ["1", "i", "I", "O", "0", 'l']

    list_punctuation = [".", ",", ";", ":"]

    list_vowels_upper = ['A','E','I','O','U']
    list_vowels_lower = ['a','e','i','o','u']

    list_consonant_lower = ["b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "q", "r", "s", "t", "v", "w", "x", "y", "z"]
    list_consonant_upper= ["B", "C", "D", "F", "G", "H", "J", "K", "L", "M", "N", "P", "Q", "R", "S", "T", "V", "W", "X", "Y", "Z"]

    list_final_charset = []

    password_length = 16

    debug = False

    start_time = None
    end_time = None
    show_time = False

    password_pattern = None

    def __init__(self, options):
        self.start_time = time.time()
        self.setup(options)

    def setup(self, options):

        if len(options) == 1:
            self.show_help()
            exit(1)

        charater_set = options[1]

        self.use_upper = True if "u" in charater_set else False
        self.use_lower = True if "l" in charater_set else False
        self.use_symbol = True if "s" in charater_set else False
        self.use_space = True if "c" in charater_set else False
        self.use_digits = True if "d" in charater_set else False
        self.use_brackets = True if "b" in charater_set else False
        self.use_minus = True if "m" in charater_set else False
        self.use_underline = True if "n" in charater_set else False
        self.remove_homoglyphs = True if "e" in charater_set else False
        self.show_time = True if "t" in charater_set else False

        # Using a pattern *essentially* negates all previous options.
        self.use_pattern = True if "p" in charater_set else False

        # Using "words" negates all previous options
        self.use_words = True if "w" in charater_set else False;

        self.debug = True if "g" in charater_set else False

        if self.debug:
            print("use_upper: %s" % self.use_upper)
            print("use_lower: %s" % self.use_lower)
            print("use_symbol: %s" % self.use_symbol)
            print("use_digits: %s" % self.use_digits)
            print("use_space: %s" % self.use_space)
            print("use_brackets: %s" % self.use_brackets)
            print("use_minus: %s" % self.use_minus)
            print("use_underline: %s" % self.use_underline)
            print("use_pattern: %s" % self.use_pattern)

        # Sanity checking

        if not len(options) == 3:
            self.error_out("You must specify a length or pattern for your password")

        if self.use_pattern and len(options) == 2:
            self.error_out("You've asked me to generate based on a pattern, but not pattern given.")

        if self.use_pattern:
            self.password_pattern = options[2]
        else:
            self.password_length = int(options[2])

    def error_out(self, message):
        print(message)
        self.show_help()
        exit(1)

    def show_help(self):
        print("""
        PyRPG - The Python random password generator
        
        Usage:
        prpg [character set options] [length | pattern]
        
        Character set options:
        u    Include upper case characters: A-Z
        l    Include lower case characters: a-z
        s    Include symbol characters: !@#$%^&*
        d    Include digits: 0-9
        b    Include bracket characters: {}[]()<>
        m    Include the minus character: -
        n    Include the underscore character: _
        
        Extended options:
        w    Generate a password based on words
        p    Generate the password based on the given pattern (requires the pattern argument)
        e    Exclude look-alike characters (homoglyphs): 1iIO0
        
        Fun stuff:
        t    Show how long it took to generate the passwords.
        
        For all character sets (except pattern generation, "p"), you must specify the password length as the second
        argument. For all options except w and p, the length specification will specify the string character length. For
        w (word based password), the length argument will specify the number of words in the resulting password.
        
        When p is specified, the second argument must be a pattern, not a length. (See "Pattern" below).
         
        Pattern:
        
        The pattern defines the layout of the resulting password. Each character in the pattern dictates a character
        class that will be substituted at that position in the pattern. Characters that do not represent a given character
        class will be substituted as-is.
        
        For example:
        
          uull-dddd will result in:
            Two upper case characters for the first two characters of the pattern, followed by:
            Two lower case characters for the next two characters, followed by:
            "-" followed by:
            Four digits
            
        Use the following place holders to define your pattern:
        
        Base class place holders:
        
        u  Upper case characters: A-Z 
        l  Lower case characters: a-z
        s  Symbols: !@#$%^&*
        d  Digits: 0-9
        b  Bracket characters: {}[]()<>
        m  The minus character: -
        n  The underscore character: _
        p  Punctuation: ,.;:
        
        Combination and sub-class place holders:
        
        a  lower-case alphanumeric: a-z and 0-9
        A  Upper-case alphanumeric: A-Z and 0-9
        M  Mixed-case alphanumeric: a-z, A-Z, and 0-9
        h  Lower case hex character: 0-9 and a-f
        H  Upper case hex character: 0-9 and A-F
        v  Lower case vowel: aeiou
        V  Upper case vowel: AEIOU
        Z  Mixed case vowel: AEIOU and aeiou
        c  Lower case consonant: bcdfghjklmnpqrstvwxyz
        C  Upper case consonant: BCDFGHJKLMNPQRSTVWXYZ
        z  Mixed case consonant: bcdfghjklmnpqrstvwxyz and BCDFGHJKLMNPQRSTVWXYZ
        
        Special placeholders
        \    Escapes the proceeding character, and tells the generator to print it "as-is".
        {n}  Print the previous character n times.
        
        EXAMPLES
        
        Random MAC address:
          
          ./prpg.py p 'h{2}\:h{2}\:h{2}\:h{2}\:h{2}\:h{2}\:'
          
        Random three word pass phrase:
        
          ./prpg.py w 3
        
        For support, problems, and issues, file an issue on github:
          https://github.com/mjmunger/pyrpg
         
        """)

    def render_charset(self):
        character_set = []

        if self.use_upper:
            character_set = character_set + self.list_upper
        if self.use_lower:
            character_set = character_set + self.list_lower
        if self.use_symbol:
            character_set = character_set + self.list_symbol
        if self.use_digits:
            character_set = character_set + self.list_digits
        if self.use_space:
            character_set = character_set + self.list_space
        if self.use_brackets:
            character_set = character_set + self.list_brackets
        if self.use_minus:
            character_set = character_set + self.list_minus
        if self.use_underline:
            character_set = character_set + self.list_underline

        # Remove homoglpys
        if self.remove_homoglyphs:
            character_set = [char for char in character_set if char not in self.list_homoglyphs]

        self.list_final_charset = character_set

    def generate_pattern_based_password(self):
        chars = []
        repeat = 0

        pattern = iter(self.password_pattern)

        for p in pattern:
            # If the character is escaped, use as-is.
            if p == '\\':
                p = next(pattern)
                chars.append(p)

            # Repeat characters
            if p == "{":
                p = next(pattern)
                repeat = int(p)

                for i in range(1, repeat):
                    chars.append(p)

                # skip the last }
                p = next(pattern)

            if p == "u":
                chars.append(random.choice(self.list_upper))

            if p == "l":
                chars.append(random.choice(self.list_lower))

            if p == "s":
                chars.append(random.choice(self.list_symbol))

            if p == "d":
                chars.append(random.choice(self.list_digits))

            if p == "b":
                chars.append(random.choice(self.list_brackets))

            if p == "m":
                chars.append(random.choice(self.list_minus))

            if p == "n":
                chars.append(random.choice(self.list_underline))

            if p == "p":
                chars.append(random.choice(self.list_punctuation))

            if p == "a":
                chars.append(random.choice(self.list_lower + self.list_digits))

            if p == "A":
                chars.append(random.choice(self.list_upper + self.list_digits))

            if p == "M":
                chars.append(random.choice(self.list_lower + self.list_digits + self.list_upper))

            if p == "h":
                chars.append(random.choice(self.list_digits + self.list_lower[:6]))

            if p == "H":
                chars.append(random.choice(self.list_digits + self.list_upper[:6]))

            if p == "v":
                chars.append(random.choice(self.list_vowels_lower))

            if p == "V":
                chars.append(random.choice(self.list_vowels_upper))

            if p == "Z":
                chars.append(random.choice(self.list_vowels_lower + self.list_vowels_upper))

            if p == "c":
                chars.append(random.choice(self.list_consonant_lower))

            if p == "C":
                chars.append(random.choice(self.list_consonant_upper))

            if p == "z":
                chars.append(random.choice(self.list_consonant_lower + self.list_consonant_upper))

            # Default is to ignore the item.

        return "".join(chars)

    def generate_random_password(self):
        chars = []
        for x in range(0,self.password_length):
            chars.append(random.choice(self.list_final_charset))

        return "".join(chars)

    def generate_pass_phrase(self):
        path = 'words.txt'
        with open(path) as infile:
            m = mmap.mmap(infile.fileno(), 0, access=mmap.ACCESS_READ)

        if self.debug:
            print("Counting words in dictionary...")

        # Index the file
        index = []
        while True:
            buffer = m.readline().decode("utf-8").strip()
            if buffer == "":
                break
            index.append(buffer)

        if self.debug:
            print("Total words in dictionary: %s " % len(index))

        words = []

        for x in range(0, self.password_length):
            words.append(random.choice(index))

        return " ".join(words)

    def generate_password(self):
        if self.use_pattern:
            return self.generate_pattern_based_password()

        if self.use_words:
            return self.generate_pass_phrase()

        return self.generate_random_password()

    def render_password(self):
        self.render_charset()
        print(self.generate_password())

        if self.show_time:
            print("\nPassword generated in %s seconds" % (time.time() - self.start_time))

r = rpg(sys.argv)
r.render_password()