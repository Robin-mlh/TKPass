## TKPass

> **A Password ToolKit**

### Evaluate, generate, and much more.

## Features

 - __Test the strength of a password.__ Estimate the time to break it, give customized advice and check the exposition in word lists.
 - __Generate one or more passwords.__ Advanced customization of characteristics.
 - __Generate one or more passphrases.__ Longer and easier to remember passwords. Advanced customization of characteristics.
 - __Generate a password from a phrase.__ Remember the sentence to remember the password.
 - __Show password security recommendations__ and sources used.

The results can be copied or exported to a file.

## Installation

TKPass has been tested on Ubuntu and Windows.

Python 3 is required.

In the same directory as tkp, use the following command to install the dependencies:

    python3 -m pip install -r requirements.txt

***On Windows, replace `python3` by `py`.***

## Usage

To use TKPass:

    python3 tkp.py

For example, to generate a password:

    python3 tkp.py password

Or to check the strength of the password "qwER43@!":

    python3 tkp.py check -p qwER43@!

Open the config.py file as a text file to change important settings used by TKPass.
For example the default password generation settings, the files used, the automatic copy and many other things.

## FAQ

#### What is the Exposure report section in the password check ?

The exposure report shows the correspondences between the terms of the loaded dictionaries and the password.
All files in /dictionnaries/* are taken into account as word or password dictionaries exposed.
This directory can be changed in the configuration file.
You can also specify different files with the option --wordlist FILE [FILE ...]
These files must contain one element (word, password) per line.

#### Why is there a 'more data (unused)' folder ?

The 'more data (unused)' folder contains dictionary files available for use.
By default it is not used by TKPass.
Download only the files you use because they are quite heavy.

#### How does the password review work ?

The zxcvbn module is used because it offers a realistic and advanced estimation of the security of a password.

#### I don't trust you. tkp will share my password.

 If you don't want to use your real password in TKPass, replace the one with characters of the same type.

#### How to edit the password generation configuration used by default ?

The default password settings used is editable in the configuration file.

#### Is the random source for password generation secure ?

The python secret module is used to take advantage of the best random available on the operating system.

#### How to define the word lists used for passphrase generation ?

The --wordlist FILE option defines a specific file for the word source.
The default file used (without the --wordlist option) is defined in the configuration file.

## Contact, contributions and more

***Help and feedback are welcome.*** Feel free to contribute on GitHub!

Mail: dev_contactmail@protonmail.com
