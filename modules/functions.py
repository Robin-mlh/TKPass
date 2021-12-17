from secrets import choice, randbelow
import configparser
import os

from zxcvbn import zxcvbn
from zxcvbn.matching import add_frequency_lists

from modules.data import *

# User configuration file.
config = configparser.ConfigParser()
config.read(os.path.realpath(__file__)[:-21] + os.sep + 'tkp.conf')
replace_path = config["GLOBAL"]["DICTIONNARY_DIRECTORY"].replace("PROG_PATH",
                                                                 os.path.realpath(__file__)[:-21])
config["GLOBAL"]["DICTIONNARY_DIRECTORY"] = replace_path


def export_file(content, path):
    """ Export the content to a file. """

    if os.path.exists(path):
        if input(f"\n{path} already exists. Do you want to overwrite it? (N/y)\n") != "y":
            return False
    try:
        with open(path, "w") as f:
            f.write(content)
        print("File successfully written.")
    except Exception as e:
        raise SystemExit(f"Unable to write the file: {e}")


def check_password(password, infos_sup=None, files_wordlists=[]):
    """ Evaluates the strength of the password according to several criteria. Powered by zxcvbn. """

    # --- Load the dictionaries and add them to zxcvbn.
    dict_wordlists = {}
    # Default location dictionaries (defined in the config file).
    for file_name in os.listdir(config["GLOBAL"]["DICTIONNARY_DIRECTORY"]):
        with open(config["GLOBAL"]["DICTIONNARY_DIRECTORY"] + os.sep + file_name, "r") as f:
            list_actual_dict = f.read().split("\n")[:-1]
        dict_wordlists[os.path.splitext(file_name)[0]] = list_actual_dict
        add_frequency_lists(dict_wordlists)
    # Additional dictionaries added as arguments.
    for file in files_wordlists:
        with file as f:
            list_actual_dict = f.read().split("\n")[:-1]
        file_name = str(file).replace("<_io.TextIOWrapper name='",
                                      "").replace("' mode='r' encoding='UTF-8'>", "")
        dict_wordlists[os.path.splitext(os.path.split(file_name)[1])[0]] = list_actual_dict
        add_frequency_lists(dict_wordlists)

    # --- Gets the password results with zxcvbn and displays the score.
    if not password:
        raise SystemExit("ValueError: The password is empty.")
    result = zxcvbn(password, infos_sup)
    print("    " + SCORE_TO_WORD[result["score"]] + " (" + str(result["score"]) + "/4)")

    # --- Shows the estimated time.
    print("\nEstimated time needed to guess the password: ")
    print("    Fast hashing with many processors (1e10/s) : ",
          result["crack_times_display"]["offline_fast_hashing_1e10_per_second"])
    print("    Slow hashing with many processors (1e4/s) :  ",
          result["crack_times_display"]["offline_slow_hashing_1e4_per_second"])
    print("    Online attack without throttling (10/s) :    ",
          result["crack_times_display"]["online_no_throttling_10_per_second"])
    print("    Online attack with throttling (100/h) :      ",
          result["crack_times_display"]["online_throttling_100_per_hour"])

    # --- Feedback
    no_feedback = True
    print("\nComments and recommendations: ")
    if result["feedback"]["warning"] != "":
        no_feedback = False
        print("    " + result["feedback"]["warning"])
    for x in result["feedback"]["suggestions"]:
        no_feedback = False
        print("    " + x)
    if len(password) <= 6:
        no_feedback = False
        print("    Your password is much too short."
              " A minimum length of 14 characters is recommended.")
    elif len(password) < 14:
        no_feedback = False
        print("    A minimum length of 14 characters is recommended.")
    # Dispersion of numbers and special characters
    nb_nums = 0
    nb_cs = 0
    for x in password:
        if x in NUMBERS:
            nb_nums += 1
        elif x in CARACTS_SPE:
            nb_cs += 1
    nb_nums_start_end = 0
    nb_cs_start_end = 0
    for x in password:
        if x in NUMBERS:
            nb_nums_start_end += 1
        elif x in CARACTS_SPE:
            nb_cs_start_end += 1
        else:
            break
    for x in reversed(password):
        if x in NUMBERS:
            nb_nums_start_end += 1
        elif x in CARACTS_SPE:
            nb_cs_start_end += 1
        else:
            break
    if nb_nums_start_end == nb_nums and nb_nums != 0:
        no_feedback = False
        if nb_cs_start_end == nb_cs and nb_cs != 0:
            print("    Numbers and special characters are not scattered correctly.")
        else:
            print("    The numbers are not dispersed properly.")
    elif nb_cs_start_end == nb_cs and nb_cs != 0:
        no_feedback = False
        print("    Special characters are not scattered correctly.")
    if no_feedback:
        print("    No comments available.")

    # --- Exposure in dictionaries.
    print("\nExposure report:")
    no_matches_found = True
    for exposed in result["sequence"]:
        try:
            print("    '" + exposed["matched_word"] + "' found in " + exposed["dictionary_name"])
            no_matches_found = False
        except KeyError:
            pass  # No matche found
    if no_matches_found:
        print("    No matches found.")


def password_from_sentence(sentence):
    """ Create a phrase-based password.

    Remember the sentence to remember the password.
    The first letters of each word are added to the password,
    numbers and special characters are kept as is.

    Arguments:
       sentence -- The sentence for create the passord (str).

    Return:
       password(s) (str)
    """

    if not sentence:
        raise SystemExit("ValueError: The sentence is empty.")
    password = ""
    if sentence[0] in ALPHA_MAJ or sentence[0] in ALPHA_MIN:
        password += sentence[0]
    for x1 in range(len(sentence)):
        if sentence[x1] in NUMBERS or sentence[x1] in CARACTS_SPE:
            password += sentence[x1]
        elif x1 != len(sentence)-1 and sentence[x1] == " ":
            if sentence[x1+1] in ALPHA_MIN or sentence[x1+1] in ALPHA_MAJ:
                password += sentence[x1+1]

    return password


def password_generation(lowercase_letters=None, upper_case_letters=None, digits=None,
                        special_symbols=None, nb_characters=None,
                        generation_number=1, banned_characters=[]):
    """ Generates password(s)

    Arguments:
       lowercase_letters  -- Number of lowercase letters (int or '' to select the value randomly).
       upper_case_letters -- Number of of capital letters (int or '' to select the value randomly).
       digits             -- Number of figures (int or '' to select the value randomly).
       special_symbols    -- Number of special symbols (int or '' to select the value randomly).
       nb_characters      -- Total number of characters for each password (int).
       generation_number  -- Number of password to generate (int).
       banned_characters  -- List of banned characters (list).

    Return:
       password(s) (str)

    """

    # Create lists of characters of each type without banned characters.
    alpha_min = [caract_min for caract_min in ALPHA_MIN if caract_min not in banned_characters]
    alpha_maj = [caract_maj for caract_maj in ALPHA_MAJ if caract_maj not in banned_characters]
    chiffres = [chiffre for chiffre in NUMBERS if chiffre not in banned_characters]
    caracts_speciaux = [caract_spe for caract_spe in CARACTS_SPE if caract_spe not in banned_characters]

    total_passwords = []
    for x in range(generation_number):
        list_loto = []
        password = []
        if lowercase_letters is not None:
            if lowercase_letters == "":
                list_loto = [*list_loto, *alpha_min]
            else:
                for nb_lower_letters in range(int(lowercase_letters)):
                    password.append(choice(alpha_min))
        if upper_case_letters is not None:
            if upper_case_letters == "":
                list_loto = [*list_loto, *alpha_maj]
            else:
                for nb_upper_letters in range(int(upper_case_letters)):
                    password.append(choice(alpha_maj))
        if digits is not None:
            if digits == "":
                list_loto = [*list_loto, *chiffres]
            else:
                for nb_digits in range(int(digits)):
                    password.append(choice(chiffres))
        if special_symbols is not None:
            if special_symbols == "":
                list_loto = [*list_loto, *caracts_speciaux]
            else:
                for nb_symbols in range(int(special_symbols)):
                    password.append(choice(caracts_speciaux))
        if nb_characters is not None and len(list_loto) > 0:
            for remaining_length in range(int(nb_characters) - len(password)):
                password.append(choice(list_loto))

        # Shuffle the password (list) securely.
        for i in reversed(range(1, len(password))):
            j = randbelow(i + 1)
            password[i], password[j] = password[j], password[i]
        if x is not generation_number-1:
            password.append("\n")
        total_passwords.append("".join(password))

    return "".join(total_passwords)


def password_generation_sentence(password, wordlist):
    """ Generates sentence from the password.

    Remember the sentence to remember the password.
    Inverse operation of the 'password_from_sentence' function.

    Arguments:
       password -- Obviously the password (str).
       wordlist -- The list of words to use to create the sentence (list)
                   The default value is defined in the configuration file.

    Return:
       Sentence(s) (str)

    """

    total_sentence = []
    sentence = ""
    for password in password.split("\n"):
        for l in password:
            if l in CARACTS_SPE or l in NUMBERS:
                sentence += l + " "
            elif l in ALPHA_MIN or l in ALPHA_MAJ:
                try:
                    word_choice = choice([x for x in wordlist if x[0] == l.lower()])
                    if l in ALPHA_MAJ:
                        sentence += word_choice[0].upper() + word_choice[1:] + " "
                    else:
                        sentence += word_choice + " "
                except IndexError:
                    sentence += l + " "
        total_sentence.append(sentence)
        sentence = "\n"

    return "".join(total_sentence)


def passphrase_generation(wordlist, nb_words, sep, generation_number,
                          symbols, digits, capitalization):
    """ Generates a passphrase.

    A password made of words. Useful to remember.

    Arguments:
       wordlist -- The list of words to use (list).
                   The default value is defined in the configuration file.
       nb_words -- The number of words in each passphrase (int).
       sep      -- Separator between words (str).
       generation_number -- Number of passphrases to generate.
       symbols  -- Number of symbols to append (int).
       digits   -- Number of digits to append (int).
       capitalization  -- Capitalize the first letter of each word? (True or False)

    Return:
       Passphrase(s) (str)

    """

    total_passphrases = []
    for npp in range(generation_number):
        passphrase = []
        for nwords in range(nb_words):
            word = choice(wordlist) + sep
            if capitalization:
                word = word[0].upper()
            passphrase.append(word)
        for nb_digits in range(digits):
            passphrase.append(choice(NUMBERS))
        for nb_symbols in range(symbols):
            passphrase.append(choice(CARACTS_SPE))
        # Shuffle the passphrase (list) securely.
        for i in reversed(range(1, len(passphrase))):
            j = randbelow(i + 1)
            passphrase[i], passphrase[j] = passphrase[j], passphrase[i]
        # Delete last separator
        for x in range(len(passphrase)-1, -1, -1):
            if passphrase[x].endswith(sep):
                passphrase[x] = passphrase[x][:-len(sep)]
                break
        passphrase = "".join(passphrase)
        total_passphrases.append(passphrase)
        if npp is not generation_number-1:
            total_passphrases.append("\n")

    return "".join(total_passphrases)
