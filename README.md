# Dropbox Notifier 🐍 + 📄

Get notified when a file or folder is modified in your [Dropbox](https://www.dropbox.com) account.

The development of this project was sponsored by [Hive Solutions](http://www.hive.pt).

## Features

* Uses Python 3.6+ with type hinting
* Uses [Appier](https://github.com/hivesolutions/appier) and [Appier Extras](https://github.com/hivesolutions/appier-extras)
* Runs on top of [ASGI](https://asgi.readthedocs.io/en/latest/)
* Sends e-mail based notifications
* Makes use of Black for validation

### Configuration

| Name                   | Type   | Default | Description                                                                                      |
| ---------------------- | ------ | ------- | ------------------------------------------------------------------------------------------------ |
| **SCHEDULER**          | `bool` | `True`  | If the scheduler for modification tracking is active.                                            |
| **SCHEDULER_TIMEOUT**  | `int`  | `30`    | The number of seconds between tick scheduler tick operations.                                    |
| **NOTIFIER_EMAIL**     | `str`  | `None`  | The email address to where the modification notifications are going to be sent.                  |
| **NOTIFIER_RECEIVERS** | `list` | `[]`    | Alternative to `NOTIFIER_EMAIL` to specify multiple receivers.                                   |
| **NOTIFIER_CC**        | `list` | `[]`    | Sames as `NOTIFIER_RECEIVERS` but for the CC field.                                              |
| **NOTIFIER_BCC**       | `list` | `[]`    | Sames as `NOTIFIER_RECEIVERS` but for the BCC field.                                             |
| **NOTIFIER_FOLDER**    | `str`  | `None`  | The Dropbox path or ID of the folder to be scanned for changes (eg: `"id:CtYjakofsdAAAAAPyEg"`). |

## License

Dropbox Notifier is currently licensed under the [Apache License, Version 2.0](http://www.apache.org/licenses/).

## Build Automation

[![PyPi Status](https://img.shields.io/pypi/v/dropbox-notifier.svg)](https://pypi.python.org/pypi/dropbox-notifier)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://www.apache.org/licenses/)
