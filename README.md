# PyRPG - Secure Python random password generator

Generate cryptographically secure random passwords with specified character sets, patterns, or lengths.

## Installation

PyRPG requires Python 3.6 above because it uses the `secrets` module for cryptographically secure random numbers*.

If you do not have Python 3.6, you can download and install it from [python.org](https://www.python.org/downloads/).

### Debian specific installation.

Debian stretch does not yet have Python 3.6 in an repository package, therefore, you can compile from scratch:

Prep your system:
```
apt build-dep python
apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev
```

Download Python 3.6 for Linux, and extract to /usr/src/, then:
```
./configure
make
make install
```

Secrets is part of the core library as of v3.6, so there is nothing else to install.

\* Note: "cryptographically secure" is a somewhat relative term. The secrets module actually "[...provides access to the most secure source of randomness that your operating system provides](https://docs.python.org/3/library/secrets.html#random-numbers)". Thus, if you do not have a good source of randomness on your computer, you will not get good secure numbers. This is entirely dependent on [your chipset](https://software.intel.com/en-us/articles/intel-digital-random-number-generator-drng-software-implementation-guide). 
## Usage:
`prpg [character set options] [length | pattern]`

### Character set options:

```
u    Include upper case characters: A-Z
l    Include lower case characters: a-z
s    Include symbol characters: !@#$%^&*
d    Include digits: 0-9
b    Include bracket characters: {}[]()<>
m    Include the minus character: -
n    Include the underscore character: _
```

### Extended options:
```
w    Generate a password based on words
p    Generate the password based on the given pattern (requires the pattern argument)
e    Exclude look-alike characters (homoglyphs): 1iIO0
```

### Fun stuff:
```
t    Show how long it took to generate the passwords.
g    Show debugging information
```

For all character sets (except pattern generation, "p"), you must specify the password length as the second
argument. For all options except w and p, the length specification will specify the string character length. For
w (word based password), the length argument will specify the number of words in the resulting password.

When p is specified, the second argument must be a pattern, not a length. (See "Pattern" below).

### Patterns:

The pattern defines the layout of the resulting password. Each character in the pattern dictates a character
class that will be substituted at that position in the pattern. Characters that do not represent a given character
class will be substituted as-is.

For example:

`uull-dddd` will result in:

* Two upper case characters for the first two characters of the pattern, followed by:
* Two lower case characters for the next two characters, followed by:
* "-" followed by:
* Four digits

Use the following place holders to define your pattern:

*Base class place holders:*
```
u  Upper case characters: A-Z 
l  Lower case characters: a-z
s  Symbols: !@#$%^&*
d  Digits: 0-9
b  Bracket characters: {}[]()<>
m  The minus character: -
n  The underscore character: _
p  Punctuation: ,.;:
```

*Combination and sub-class place holders:*

```
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
```

*Special placeholders*
```
\    Escapes the proceeding character, and tells the generator to print it "as-is".
{n}  Print the previous character n times.
```

## EXAMPLES

### Random password for a website, and show the timing

```
./prppg.py slut 16
```

### Random MAC address:
```
./prpg.py p 'h{2}:h{2}:h{2}:h{2}:h{2}:h{2}' 
```

### Random three word pass phrase:
```
./prpg.py w 3
```

### Escape the h so it starts with h

```
./prpg.py p '\hu{12}' 
```

# Support and Issues

For support, problems, and issues, file an issue on github:
  https://github.com/mjmunger/pyrpg 

## References
* [Python secrets](https://docs.python.org/3/library/secrets.html#random-numbers)

## Sources and contributions
* Pattern functions based on [Keepass password generator](https://keepass.info/help/base/pwgenerator.html)
* mmap usage for words.txt based on [Python fastest way to process large file](https://stackoverflow.com/questions/30294146/python-fastest-way-to-process-large-file)
* English words list provided by [dwyl/englishwords](https://github.com/dwyl/english-words)
