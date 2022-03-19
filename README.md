# [Xenoponics Logo](https://gitlab.51aliens.space/uploads/-/system/project/avatar/2/xenoponics.png)Xenoponics
A repository for scripts and other tools to run hydroponics systems in a smarter way.

## Configured Scripts

### `control.py`

### Summary

The management script for our current Raspberry Pi setup.
Uses [Typer](https://typer.tiangolo.com), [python-requests](https://docs.python-requests.org/en/latest/), and Python stdlib to perform POST requests to [XenoAPI](https://gitlab.51aliens.space/default/xenoapi), which is a GraphQL API that handles database interactions.

### Requirements

- Python 3.8+

### Setup

1. Make a virtualenv

```shell
python3 -m venv .xenovenv
```

2. Activate the virtualenv

```shell
source ./xenovenv/bin/activate
```

3. Install pip dependencies

```shell
pip3 install -r requirements.txt
```

### Usage

See `./control.py --help` for usage information.

---

"I've been a plant lady since birth." - [McCDouble21](https://www.youtube.com/watch?v=dQw4w9WgXcQ)

