# TKPass main configuration file

import os

### [GLOBAL]

# The path of /TKPass:
TKPATH = os.path.realpath(__file__)[:-10]

# Systematically copy the generated result?
# True = copies the generated data to the clipboard automatically.
# False = disabled.
AUTO_COPY_GENERATED = True

# Folder of word lists to load.
# Each file in this folder will be loaded as a dictionary during password verification.
# This is also the default folder for searching word lists for passphrase generation.
DICTIONNARY_DIRECTORY = TKPATH + "/dictionaries/"

# Default destination for the -o argument.
# Used without specifying a destination with the -o argument.
# By specifying only a file, it will be written to the location of the user.
DEFAULT_OUTFILE = "outfile_tkp.txt"

# Number of default generation.
# Value applied in the absence of the -n option.
DEFAULT_NB_GENERATION = 1

### [PASSWORD]

# Default password generation configuration. Used if not specified otherwise in the command arguments.
# If the value is empty (""), it means that the value is random within the limit of the number of characters.
DEFAULT_PASSWORD_LENGTH = 16            # Number of characters. Can't be empty.
DEFAULT_PASSWORD_LOWER_LETTERS = ""     # Number of lower case letters.
DEFAULT_PASSWORD_UPPER_LETTERS = ""     # Number of upper case letters.
DEFAULT_PASSWORD_DIGITS = ""            # Number of digits.
DEFAULT_PASSWORD_SPECIALS_SYMBOLS = ""  # Number of special characters.

# Characters banned from password generation.
# These characters will not appear in a generated password.
# Example: ["t", "5", "#"]
BANNED_CHARACTERS_PASSWORD = []

# Default file for the word list used to generate the phrase when generating a password.
# This value is used if the -p option is used but no file is specified.
DEFAULT_WORDLIST_FILE_SENTENCE_PASSWORD = DICTIONNARY_DIRECTORY + "English_wordlist_(370099).txt"

### [PASSPHRASE]

# Word list file to use by default for passphrase generation.
# Used if the -e argument is not specified.
DEFAULT_WORDLIST_FILE_PASSPHRASE = DICTIONNARY_DIRECTORY + "English_wordlist_(370099).txt"

# Default separator between the words of the passphrase.
# Used if the -s option is not specified.
DEFAUT_SEPARATOR_PASSPHRASE = "-"

# Default number of words to be included in the passphrase.
# Used if the -l option is not specified.
DEFAULT_NB_WORDS_PASSPHRASE = 6
