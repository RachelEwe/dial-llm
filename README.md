# dial-llm

A proof of concept to generate dialogs between Pygmalion chatbots.

Can also be used interactively to chat with one bot in command line.

Can be used with [back-llm](https://github.com/RachelEwe/back-llm) backend.

Can support AES with a preshared key (export PSK in .env) so you can use crypted api without using a certificate.

Can also be used with oobabooga or other compatible backend (but without encryption).

```
usage: dial.py [-h] [-c CHARA [CHARA ...]] [-d] [-i] [-o OUTPUT] [-s]

optional arguments:
  -h, --help            show this help message and exit
  -c CHARA [CHARA ...], --chara CHARA [CHARA ...]
                        1 or 2 characters (png card of json file)
  -d, --dialog          Automatic dialogue beetween 2 characters
  -i, --interactive     Chat interactively with one character
  -o OUTPUT, --output OUTPUT
                        Save the output to a file
```
