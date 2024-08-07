# CyberShield

An app that prevents scams with integrated WireGuard to prevent MITM attacks and automated OSINT to stop spearphishing.

## Architecture

Android and Windows GUI in Kotlin/Tkinter

## Installation/Setup

Requires Python installed on any OS.

Creating virtual environment in Linux:

```
python3 -m venv venv
source venv/bin/activate
```
Creating environment in replit:

1. Select python as main language
2. Open the shell interpreter and follow the below instructions

In root terminal or otherwise:

```
git clone https://github.com/AnonymousRendezvous/CyberShield
cd CyberShield
pip install -Ur requirements.txt
```

You also need to install tkinter for your respective OS if not previously installed.
(mostly linux and windows based distributions)

## Usage

```
python osint.py
```
(Currently only the OSINT feature is working)

Input any person's full name under "Query:" (Please input the person's full name for better results)

Input a known keyword associated with the person under "Any other information: ". If nothing, simply leave it blank.

For "Any other information: ", type in complete sentences and don't use acronyms,
do also remember to spell out full nouns and watch your intensifiers. 
Leave this option blank if you have no additional information.

Type either y/n in the "Do you want to trawl for images?" parameter. (Beta testing)

Enter your email under "Email: " parameter. (Don't worry, your email will not be stored)

Enter your instagram username under the "Input your instagram username: " parameter. (Beta testing, to use the API, uncomment the line of code in main.)

## Additional Information

*Removed Instagram username search as still under beta testing and too volatile. (For now)
Another known issue is that the compilation rate is a little slow (2-3 minutes) 
so do bear with our program should it take a long time to load.
