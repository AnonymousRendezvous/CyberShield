# CyberShield Backend

![Python 3.9](https://img.shields.io/badge/python-3.9-blue)

An app that prevents scams.

## Features

- OSINT, to find exposed personal information on the Internet
- Website checker, to see if a website is suspicious

The Python backend for both features is located here.

## Installation/Setup

Requires Python 3.9 installed on any OS. Consider using [pyenv](https://github.com/pyenv/pyenv).

Set up the development environment in Linux:

```
python3 -m venv venv
source venv/bin/activate
pip install -Ur requirements.txt
```

## Running

Either run the frontend locally (see instructions in [cybershield-ui](https://github.com/frosetrain/cybershield-ui)), or use our hosted instance at https://cybershield.pages.dev

## OSINT

Input your full name[^1] under "Your name" (The full name is needed for good results)

Input more context about you under "Additional information about you", like your educational or work experience. This helps the AI to know which person you are.

Optionally, you can enter your email to check whether it was found in any data breaches.

Optionally, you can enter your Instgram username to see what publicly available information can be found in your profile.

## Webcheck

We used Label Sleuth to create a classification model to determine whether a website is suspicious or not. The training data is the URL combined with the first 10,000 characters in the website's HTML.

### Dataset

Bad websites: https://github.com/StevenBlack/hosts (Unified hosts + fakenews)

Good websites: https://gist.github.com/bejaneps/ba8d8eed85b0c289a05c750b3d825f61

You can see the CSV files containing our training data in the `training-data` folder.

## Disclaimers

(TODO) Write a whole legal disclaimer about the OSINT tool

The webchecker is not completely reliable, so exercise your own judgement when browsing the web. If a website seems suspicious, don't click on the link.

[^1]: Please use your own name. We are not responsible for any cases of this tool being used for stalking.
