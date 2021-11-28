# Current version of TKPass.
VERSION_TKP = "1.1"

# Lowercase alphabet.
ALPHA_MIN = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l",
             "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
# Capital alphabet.
ALPHA_MAJ = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L",
             "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
# Numbers.
NUMBERS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
# Special characters.
CARACTS_SPE = ["&", "~", '"', "#", "'", "{", "(", "[", "-", "|", "`", "_", "^",
               "@", ")", "]", "°", "+", "=", "}", "¨", "£", "$", "¤", "%", "µ",
               "*", "!", "§", ":", ";", ".", ",", "?"]

# Comment on the password score.
SCORE_TO_WORD = {
    0: "Very weak",
    1: "Very weak",
    2: "Weak",
    3: "Medium",
    4: "Strong",
}

# Password security tips.
PASSWORD_DOCUMENTATION = (
    "\n  What are the main risks?"
    "\n\n    The websites and applications you use are under attack every day."
    " Security breaches occur and your passwords are stolen."
    "\n    When you reuse the same passwords, you only need to break one"
    " or use a stolen database to gain access to all your accounts."
    "\n    Use two-factor authentication (2FA) to significantly increase your security "
    "and avoid the SMS authentication code."
    "\n    Only you are the master of your actions: don't trust anyone, "
    "don't open unknown links and don't install anything that is not secure."
    "\n\n\n  Safety recommendations:"
    "\n\n    - Create a unique password for each account so you don't compromise them all at once."
    "\n    - Choose a password that is not related to you and does not contain addresses, names, dates, etc."
    "\n    - Make sure your passwords contain at least 14 characters "
    "with scattered numbers and special characters."
    "\n    - Don't share them with anyone. No one."
    "\n    - Do not write down your passwords and do not save them on your devices."
    "\n    - Log out after logging in on a non-personal computer."
    "\n    - Do not send sensitive information by SMS, email or using an unsecured protocol (http, ftp)."
    "\n    - Use multiple email addresses."
    "\n\n  Recommended password manager (free):        bitwarden.com"
    "\n  Check if you are concerned by a data leak:  haveibeenpwned.com"
    "\n\n\n  Sources:"
    "\n\n    dropbox.tech/security/zxcvbn-realistic-password-strength-estimation"
    "\n    github.com/howsecureismypassword"
    "\n    blog.mozilla.org/firefox/en/stay-in-good-health-online-but-not-quite"
    "\n    ssi.gouv.fr/guide/password"
    "\n    bitwarden.com/blog"
    "\n    en.wikipedia.org/wiki/Password_strength\n")
