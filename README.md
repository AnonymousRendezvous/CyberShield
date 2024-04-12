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

Input any person's name under "Query:"

Input any additional information about the person under "Any other information: "

For "Any other information: ", type in complete sentences and don't use acronyms, do also remember to spell out full nouns and watch your intensifiers.

If no other information, simply press enter.

Type either y/n in the "Do you want to trawl for images?" parameter.
