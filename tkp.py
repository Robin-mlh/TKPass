#!/usr/bin/python3

""" Password toolkit. """

import sys
import os
import getpass
import configparser
from secrets import randbelow  # To use random cryptography.
import argparse  # Module for the command line system.

import pyperclip  # To copy and get the clipboard.

from modules import functions  # Functions.
from modules.functions import config  # Configuration file.
from modules.data import *  # Data and text file.


def required_length(nmin, nmax):
    """ Action that returns an error
    if the number of arguments (nargs) is out of range. """

    class RequiredLength(argparse.Action):
        def __call__(self, parser, args, values, option_string=None):
            if not nmin <= len(values) <= nmax:
                raise argparse.ArgumentTypeError(
                      f"argument {self.dest} requires between {nmin} and {nmax} arguments")
            setattr(args, self.dest, values)
    return RequiredLength


def definition_parent_parser():
    """ Set the parent parser.
    A shortcut to assign the same arguments to several parsers."""

    global parent_parser_generation
    parent_parser_generation = argparse.ArgumentParser(add_help=False)
    parent_parser_generation.add_argument("--copy", "-c", action="store_true",
                                          help="Copiy the result to the clipboard")
    parent_parser_generation.add_argument("--hide", "-H", action="store_true",
                                          help="Does not display the result")
    parent_parser_generation.add_argument("--output", "-o", type=str, metavar="FILE",
                                          default=False, nargs="?", help="Export result to a file")


# Modification of argparse.ArgumentParser to customize the global help message.
class ArgumentParserCustomGlobal(argparse.ArgumentParser):

     def format_help(self):
         return """Usage: tkp.py [COMMAND] [OPTION]...

A password toolkit.

Commands:
   check, c       Test the strength of a password
   password, w    Generate a password
   passphrase, p  Generate a passphrase
   sentence, s    Generate a sentence-based password
   doc            Shows safety recommendations and tkp sources

Options:
   -h, --help     Show this help message and exit
   -v, --version  Show program's version number and exit
   
Use "tkp.py [COMMAND] --help" for more information about a command.
"""


class TkpCli(object):
    """ Command line system.  """

    def __init__(self):
        parser = ArgumentParserCustomGlobal(description="A password toolkit.",
                                            usage="""tkp.py [COMMAND] [OPTION]...""")
        parser.add_argument("-v", "--version", action='version', version='TKPass '+VERSION_TKP)
        parser.add_argument('command', metavar="COMMAND", help='command')
        if len(sys.argv) == 1:
            # Displays the help when the program is started without arguments.
            parser.print_help(sys.stderr)
            sys.exit(1)
        args = parser.parse_args(sys.argv[1:2])
        # A method = A command.
        if not hasattr(self, args.command):
            # If no method matches the command entered by the user.
            parser.error(message="Unrecognized command."
                                 "\nUse the -h option to see the available commands.")
        definition_parent_parser()  # Set the parent parser.
        # Executes the corresponding method to a command.
        getattr(self, args.command)()


    def check(self):
        parser = argparse.ArgumentParser(description="Test the strength of a password.",
                                         usage="tkp.py {check|c} [-h] [-p PASSWORD | --getpass | --clipboard]"
                                               "\n       [-i INFO [INFO ...]] [--wordlist FILE [FILE ...]]")
        group_check_password = parser.add_mutually_exclusive_group(required=False)
        group_check_password.add_argument("--password", "-p", metavar="PASSWORD", type=str,
                                          help="The password to check")
        group_check_password.add_argument("--getpass", "-g", action="store_true",
                                          help="Use the getpass function to securely ask for the password"
                                                "\nDefault method used to get the password.")
        group_check_password.add_argument("--clipboard", "-c", action="store_true",
                                          help="Use the clipboard as password")
        parser.add_argument("--info", "-i", type=str, nargs="+",
                            help="Additional information. For example, a name or a date of birth")
        parser.add_argument("--wordlist", "-w", type=argparse.FileType('r'),
                            nargs="+", metavar="FILE", default=[],
                            help="Additional word list files to load")
        args = parser.parse_args(sys.argv[2:])

        if args.password not in [False, None]:
            password = args.password
        elif args.clipboard not in [False, None]:
            try:
                password = pyperclip.paste()
            except pyperclip.PyperclipException as e:
                raise SystemExit(f"An error has occurred: the clipboard does not exist or cannot be reached. {e}")
        else:
            password = getpass.getpass()
            print()
        functions.check_password(password, infos_sup=args.info, files_wordlists=args.wordlist)


    def password(self):
        parser = argparse.ArgumentParser(parents=[parent_parser_generation],
                                         formatter_class=argparse.RawTextHelpFormatter,
                                         usage="""tkp.py {password|w} [-cfh] [-o [OUTFILE]] [-l {LENGTH | MIN_LENGTH MAX_LENGTH}]
       [-a NUM_LOWERCASE_LETTERS] [-u NUM_UPPER_CASE_LETTERS] [-d NUM_DIGITS] [-s NUM_SPECIAL_SYMBOLS]
       [-n GENERATION_NUMBER] [-b BANNED_CHARACTERS [BANNED_CHARACTERS ...]] [--passphrase [WORDLIST_FILE]]""",
                                              description="Generates a cryptographically random password."
                                                          "\nUse the command without argument to use the default configuration.",
                                              epilog="""Example:
   tkp w -n 7 -l 20 -a 10 -u 0
   Generates 7 passwords of 20 characters composed of no capital letters,
   10 lowercase letters, numbers and special characters.""")
        parser.add_argument("-l", type=int, nargs="+", action=required_length(1, 2), metavar="LENGTH",
                            help="Number of characters in each password. With two numbers,\n"
                                 "the length will be random between the first and the second")
        parser.add_argument("-a", metavar="NUM_LOWERCASE_LETTERS",
                            default=config["PASSWORD"]["DEFAULT_PASSWORD_LOWER_LETTERS"],
                            help="Number of lowercase letters in each password")
        parser.add_argument("-u", metavar="NUM_UPPER_CASE_LETTERS",
                            default=config["PASSWORD"]["DEFAULT_PASSWORD_UPPER_LETTERS"],
                            help="Number of capital letters in each password")
        parser.add_argument("-d", metavar="NUM_DIGITS",
                            default=config["PASSWORD"]["DEFAULT_PASSWORD_DIGITS"],
                            help="Number of digits in each password")
        parser.add_argument("-s", metavar="NUM_SPECIAL_SYMBOLS",
                            default=config["PASSWORD"]["DEFAULT_PASSWORD_SPECIALS_SYMBOLS"],
                            help="Number of special symbols in each password")
        parser.add_argument("-n", type=int, default=config["GLOBAL"]["DEFAULT_NB_GENERATION"],
                            metavar="GENERATION_NUMBER", help="Number of password to generate")
        parser.add_argument("-b", nargs="+", default=config["PASSWORD"]["BANNED_CHARACTERS_PASSWORD"],
                            metavar="BANNED_CHARACTER",
                            help="Characters that cannot be included in the password")
        parser.add_argument("--passphrase", "-p", type=str, metavar="WORDLIST_FILE", nargs="?", default=None,
                            const=config["PASSWORD"]["DEFAULT_WORDLIST_FILE_SENTENCE_PASSWORD"].replace("DICTIONNARY_DIRECTORY",
                                                                                                config["GLOBAL"]["DICTIONNARY_DIRECTORY"]),
                            help="Generate a phrase based on the password to remember it")
        args = parser.parse_args(sys.argv[2:])

        if args.l is None:
            if not isinstance((config.getint("PASSWORD", "DEFAULT_PASSWORD_LENGTH")), int):
                raise SystemExit("ValueError: The password length value to be generated is invalid.\n"
                                 "Check the value of DEFAULT_PASSWORD_LENGTH in the configuration file.")
            else:
                nb_characters = config.getint("PASSWORD", "DEFAULT_PASSWORD_LENGTH")
        elif len(args.l) == 1:
            nb_characters = args.l[0]
        elif len(args.l) == 2:
            nb_characters = randbelow(args.l[1])
            while nb_characters < args.l[0]:
                nb_characters = randbelow(args.l[1])
        # Generation of the password(s).
        result = functions.password_generation(args.a, args.u, args.d, args.s,
                                               nb_characters, args.n, args.b)
        # Initialization of the arguments used after the generation of the result.
        if not args.hide:
            print(result)
            if args.passphrase is not None:
                with open(args.passphrase, "r") as f:
                    wordlist = list(f.read().split("\n"))
                sentence_password = functions.password_generation_sentence(result, wordlist)
                print("\n" + sentence_password)
        if args.copy or config.getboolean('GLOBAL', 'AUTO_COPY_GENERATED'):
            try:
                pyperclip.copy(result)
            except pyperclip.PyperclipException as e:
                raise SystemExit(f"An error has occurred: the clipboard does not exist or cannot be reached. {e}")
        if args.output is None:
            functions.export_file(result, path=config["GLOBAL"]["DEFAULT_OUTFILE"])
        elif args.output is not False:
            functions.export_file(result, path=args.output)


    def passphrase(self):
        parser = argparse.ArgumentParser(usage="tkp.py {passphrase|p} [-cdfhuw]"
                                               " [-l {WORDS_NUMBER | MIN_NUM_WORDS MAX_NUM_WORDS}]"
                                               "\n       [-i WORDLIST_FILE] [-s SEPARATOR] [-n GENERATION_NUMBER] [-o [OUTFILE]]",
                                         parents=[parent_parser_generation],
                                         formatter_class=argparse.RawTextHelpFormatter,
                                         description="Generats a cryptographically random passphrase.",
                                         epilog="""Example:
   tkp p -n 2 -l 6 -s '-' -o 'passphrase.txt'
   Generate and export to a file 2 passphrases of 6 words separated by a dash.""")
        parser.add_argument("--separator", "-s", type=str, default=config["PASSPHRASE"]["DEFAUT_SEPARATOR_PASSPHRASE"],
                            help="Character between words")
        parser.add_argument("--generation-number", "-n", type=int, default=config["GLOBAL"]["DEFAULT_NB_GENERATION"],
                            help="Number of passphrase to generate")
        parser.add_argument("--words-number", "-l", type=int, nargs="+", action=required_length(1, 2),
                            help="Number of words in each passphrase")
        parser.add_argument("-u", action="store_true", help="Capitalize the first letter of each word")
        parser.add_argument("-w", type=int, default=0, help="Number of symbols (default: 0)", metavar="NUM_SYMBOLS")
        parser.add_argument("-d", type=int, default=0, help="Number of digits (default: 0)", metavar="NUM_DIGITS")
        parser.add_argument("--wordlist", "-i", type=str, metavar="FILE",
                            default=config["PASSPHRASE"]["DEFAULT_WORDLIST_FILE_PASSPHRASE"].replace("DICTIONNARY_DIRECTORY",
                                                                                                     config["GLOBAL"]["DICTIONNARY_DIRECTORY"]),
                            help="List of words to be used for the generation of the passphrase")
        args = parser.parse_args(sys.argv[2:])

        with open(args.wordlist, "r") as f:
            wordlist = list(f.read().split("\n"))
        # Definition of the number of words
        # to put in the passphrase according to the user's arguments.
        if args.words_number is None:
            nb_words = config.getint("PASSPHRASE", "DEFAULT_NB_WORDS_PASSPHRASE")
        elif len(args.words_number) == 1:
            nb_words = args.words_number[0]
        elif len(args.words_number) == 2:
            nb_words = randbelow(args.words_number[1])
            while nb_words < args.words_number[0]:
                nb_words = randbelow(args.words_number[1])
        # Generation of the passphrase(s).
        result = functions.passphrase_generation(wordlist, nb_words,
                                                 args.separator, args.generation_number,
                                                 args.w, args.d, args.u)
        # Initialization of the arguments used after the generation of the result.
        if not args.hide:
            print(result)
        if args.copy or config.getboolean('GLOBAL', 'AUTO_COPY_GENERATED'):
            try:
                pyperclip.copy(result)
            except pyperclip.PyperclipException as e:
                raise SystemExit(f"An error has occurred: the clipboard does not exist or cannot be reached. {e}")
        if args.output is None:
            functions.export_file(result, path=config["GLOBAL"]["DEFAULT_OUTFILE"])
        elif args.output is not False:
            functions.export_file(result, path=args.output)


    def sentence(self):
        parser = argparse.ArgumentParser(usage="""tkp.py {sentence|s} [-cfh] [--output [FILE]] SENTENCE""",
                                         description="Generate a phrase-based password."
                                                     "\nRemember the sentence to remember the password.",
                                         parents=[parent_parser_generation],
                                         formatter_class=argparse.RawTextHelpFormatter,
                                         epilog="""Exemple:
   tkp s 'Lorem ipsum dolor 66 sit amet!' -c
   Generate and copy the password created using the sentence given as an argument.""")
        parser.add_argument("sentence", metavar="SENTENCE", type=str,
                            help="Sentence")
        args = parser.parse_args(sys.argv[2:])

        result = functions.password_from_sentence(args.sentence)
        if not args.hide:
            print(result)
        if args.copy or config.getboolean('GLOBAL', 'AUTO_COPY_GENERATED'):
            try:
                pyperclip.copy(result)
            except pyperclip.PyperclipException as e:
                raise SystemExit(f"An error has occurred: the clipboard does not exist or cannot be reached. {e}")
        if args.output is None:
            functions.export_file(result, path=config["GLOBAL"]["DEFAULT_OUTFILE"])
        elif args.output is not False:
            functions.export_file(result, path=args.output)


    def doc(self):
        parser = argparse.ArgumentParser(usage="tkp.py doc [-h]",
                                         description="Show safety recommandations and TKPass sources.")
        args = parser.parse_args(sys.argv[2:])

        print(PASSWORD_DOCUMENTATION)

    # Aliases
    def c(self):
        TkpCli.check(self)

    def w(self):
        TkpCli.password(self)

    def p(self):
        TkpCli.passphrase(self)

    def s(self):
        TkpCli.sentence(self)


if __name__ == '__main__':
    TkpCli()
