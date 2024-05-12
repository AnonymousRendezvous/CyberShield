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

## Usage

```
python osint.py
```
(Currently only the OSINT feature is working)

Input any person's name under "Query:" (Please input the person's full name for better results)

Input any additional information about the person under "Any other information: "

For "Any other information: ", type in complete sentences and don't use acronyms, do also remember to spell out full nouns and watch your intensifiers. Leave this option blank if you have no additional information.

Type either y/n in the "Do you want to trawl for images?" parameter. (Beta testing)

Enter your email under "Email: " parameter. (Don't worry, your email will not be stored)

A known issue is rate limit error. In this instance, refrain from inputting higher accuracy numbers and wait for a longer time (around 5 - 10 minutes) before submitting your query again.
