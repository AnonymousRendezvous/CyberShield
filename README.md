# CyberShield

An app that protects that has integrated WireGuard and automated OSINT to stop spearphishing.

## Architecture

Android and Windows GUI in Kotlin

## Installation/Setup

Currently only available in terminal. 

Requires Python installed on any OS.

Creating virtual environment in Linux:

```
python3 -m venv venv
source venv/bin/activate
```
In root terminal or otherwise:

```
git clone https://github.com/AnonymousRendezvous/CyberShield
cd CyberShield
pip install -Ur requirements.txt
```
Alternative setup:

Create new python file and type in the above commands in shell/terminal.

(Replit highly encouraged for online compilation)


## Usage

```
python main.py
```

Input any person's name under "Query:" (Please input the person's full name for better results)

Input any additional information about the person under "Any other information: "

For "Any other information: ", type in complete sentences and don't use acronyms, do also remember to spell out full nouns and watch your intensifiers. If no other information, simply press enter.

Type either y/n in the "Do you want to trawl for images?" parameter.

Specify details and accuracy from 1-10. Do note that the higher the number, the slower the program but the higher the accuracy.

A known issue is rate limit error. In this instance, refrain from inputting higher accuracy numbers and wait for a longer time (around 5 - 10 minutes) before submitting your query again.
