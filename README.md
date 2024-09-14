# CyberShield

![Python 3.9](https://img.shields.io/badge/python-3.9-blue)

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

Input any person's full name under "Query:" (Please input the person's full name for better results)

Input a known keyword associated with the person under "Any other information: ". If nothing, simply leave it blank.

For "Any other information: ", type in complete sentences and don't use acronyms,
do also remember to spell out full nouns and watch your intensifiers.
Leave this option blank if you have no additional information.

Type either y/n in the "Do you want to trawl for images?" parameter. (Beta testing)

Enter your email under "Email: " parameter. (Don't worry, your email will not be stored)

Enter your instagram username under the "Input your instagram username: " parameter. (Beta testing, to use the API, uncomment the line of code in main.)

```
python webcheck.py
```

Input the website you would like to check in the query box.

```
replosint.py
```

For those who wish to use a web interface (replit) to run code due to convenience. Please use the above code and follow the instructions from osint.py.

Do note that this is ONLY compatible with Replit and was made specifically to address issues in replit.

## Additional Information
Average report generation time is around 5 minutes for 12 results.

To access our web app, do head to https://github.com/frosetrain/cybershield-ui 

## Webchecker

### Dataset

Bad websites: https://github.com/StevenBlack/hosts (Unified hosts + fakenews)
Good websites: https://gist.github.com/bejaneps/ba8d8eed85b0c289a05c750b3d825f61
