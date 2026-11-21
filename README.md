# Discord Code Executor

A Discord bot experiment that recognizes fenced code blocks and sends supported snippets to an external runner. When no language is specified, it guesses; that guess can be wrong.

> **Maintenance boundary:** A Discord message is untrusted input. Do not use the automatic execution design in a live server without an explicit review of consent, isolation, rate limits, and data sent to the runner.

## Table of Contents

- [What’s here](#whats-here)
- [Technologies](#technologies)

## What’s here

The repository contains the Python bot, language boilerplates, and configuration. The historical implementation posts successful output back to Discord. The use of an external runner is not, by itself, a guarantee of safety or confidentiality.

## Technologies

- [Python](https://www.python.org/) and [discord.py](https://discordpy.readthedocs.io/) for the bot.
- [Piston](https://github.com/engineer-man/piston) for external execution.
- [whats-that-code](https://github.com/matthewdeanmartin/whats_that_code) for language guesses.
- [PyYAML](https://pyyaml.org/) for configuration.
