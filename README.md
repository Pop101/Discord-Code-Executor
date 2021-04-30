# CodeExecutor
 Execute code automatically in Discord

## Table of contents
* [Technologies](#technologies)
* [General info](#general-info)
* [Setup](#setup)
* [Usage](#usage)

## Technologies
This project is created with:
* [Piston API](https://github.com/engineer-man/piston#): v2
* [DiscordPy](https://pypi.org/project/discord.py/): 1.6.0
* [Python-Levenshtein](https://pypi.org/project/python-Levenshtein/): 0.12.0
* [whats-that-code](https://github.com/matthewdeanmartin/whats_that_code): 0.1.11
* [PyYAML](https://pyyaml.org/) 5.3.1

## General info
This discord bot simply attempt to execute every code block it can see securely using [Piston API](https://github.com/engineer-man/piston#). It works best when the message author specifies a language. If they do not, the bot attempts to recognize it using [whats-that-code](https://github.com/matthewdeanmartin/whats_that_code), but may fail. If no runnable code is detected or the execution of the code results in an error, the bot will remain silent. Otherwise, the code's output is printed to a message
	
## Setup
To run this project, first download it and install the requirements with `pip3 install -r requirements.txt`. \
Then, generate and paste your discord bot token in `./config.yml` You can generate one at the [Discord Developer Portal](https://discord.com/developers/applications)

## Usage
Simply starting the program with python3: `python3 bot.py` will automatically start the bot, provided the token is correct

### Configuration
```yaml
Token: <TOKEN>
```