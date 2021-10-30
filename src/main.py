#!/usr/bin/env python

"""Nicely displays information in a table."""

import json
import logging
import os
import random
import sys
from textwrap import wrap

import coloredlogs
from tabulate import tabulate

FORMAT = "%(asctime)-15s - [%(levelname)s] - %(message)s  (%(filename)s:%(lineno)s)"

logging.basicConfig(format=FORMAT, stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)

# Final logger setup
coloredlogs.install(level="INFO", fmt=FORMAT, logger=logger, isatty=True)


class GithubAction:
    """GithubAction helper to parse variables from GitHub Action builds."""

    def __init__(self):
        """Create a GithubAction."""
        self._buildargs = os.environ

    def get(self, key, default=None):
        """Helper to retrieve GitHub action build vars safely."""
        if default is None:
            try:
                return self._buildargs[f"INPUT_{key}"]
            except KeyError as error:
                logger.error("The variable %s is mandatory but undefined", error)
                sys.exit(1)
        else:
            return self._buildargs.get(f"INPUT_{key}", default)


class Pallete:

    ansi_reset = "\u001b[0m"  # Reset
    ansi_bold = "\u001b[1m"

    ansi_foreground_prefix = "\u001b[38;5;"
    ansi_background_prefix = "\u001b[48;5;"

    ansi_foreground = {
        "black": f"{ansi_foreground_prefix}0m",
        "red": f"{ansi_foreground_prefix}1m",
        "green": f"{ansi_foreground_prefix}2m",
        "yellow": f"{ansi_foreground_prefix}3m",
        "blue": f"{ansi_foreground_prefix}4m",
        "magenta": f"{ansi_foreground_prefix}5m",
        "cyan": f"{ansi_foreground_prefix}6m",
        "white": f"{ansi_foreground_prefix}7m",
    }

    ansi_background = {
        "black": f"{ansi_background_prefix}0m",
        "red": f"{ansi_background_prefix}9m",
        "green": f"{ansi_background_prefix}10m",
        "yellow": f"{ansi_background_prefix}11m",
        "blue": f"{ansi_background_prefix}12m",
        "magenta": f"{ansi_background_prefix}13m",
        "cyan": f"{ansi_background_prefix}14m",
        "white": f"{ansi_background_prefix}15m",
    }

    default = [
        (ansi_background["black"], ansi_foreground["red"], ansi_bold),
        (ansi_background["black"], ansi_foreground["green"], ansi_bold),
        (ansi_background["black"], ansi_foreground["yellow"], ansi_bold),
        (ansi_background["black"], ansi_foreground["blue"], ansi_bold),
        (ansi_background["black"], ansi_foreground["magenta"], ansi_bold),
        (ansi_background["black"], ansi_foreground["cyan"], ansi_bold),
        (ansi_background["black"], ansi_foreground["white"], ansi_bold),
    ]

    pastel = [
        (ansi_background["red"], ansi_foreground["yellow"], ansi_bold),
        (ansi_background["cyan"], ansi_foreground["black"], ansi_bold),
        (ansi_background["green"], ansi_foreground["black"], ansi_bold),
        (ansi_background["yellow"], ansi_foreground["magenta"], ansi_bold),
        (ansi_background["magenta"], ansi_foreground["white"], ansi_bold),
    ]

    @classmethod
    def colorizer(cls, theme=None, method=None):
        """Python generator which yields colors according to the theme and provided method."""
        idx = 0
        while True:
            if method == "random":
                bg_color = "".join(random.choice(getattr(cls, theme)))
                yield bg_color
            else:
                yield "".join(getattr(cls, theme)[idx % len(getattr(cls, theme))])
                idx += 1

    @classmethod
    def colorify(cls, txt, color):
        bg_reset = cls.ansi_reset
        bg_color = color

        colorified = None
        if isinstance(txt, list):
            colorified = []

            for t in txt:
                wrapped = f"{bg_reset}\n{bg_color}".join(wrap(t))
                colorified.append(f"{bg_color}{wrapped}{bg_reset}")
        else:
            wrapped = f"{bg_reset}\n{bg_color}".join(wrap(txt))
            colorified = f"{bg_color}{wrapped}{bg_reset}"

        return colorified


class Tabulate:
    """Tabulate object."""

    def __init__(
        self, headers=[], rows=[], tablefmt="simple", theme="default", method="default"
    ):
        """Create an ECSAutoscaler."""
        self._headers = headers
        self._rows = rows
        self._format = tablefmt
        self._theme = theme
        self._method = method

    def __repr__(self):
        """Representation of the Table object."""
        return f"<{self.__class__} 'foo': {self._headers} {self._rows}>"

    def setup(self):
        """Main action logic."""
        table = []

        colors = Pallete.colorizer(theme=self._theme, method=self._method)

        for row in self._rows:
            colored_row = Pallete.colorify(row, color=next(colors))
            table.append(colored_row)

        print(tabulate(table, headers=self._headers, tablefmt=self._format))


def main():
    """The main entrypoint for the action."""

    github = GithubAction()

    try:
        headers = github.get("HEADERS", "").split(",")
        rows = json.loads(github.get("ROWS", "{}"))
        tablefmt = github.get("FORMAT", "simple")
        theme = github.get("THEME", "default")
        method = github.get("METHOD", "default")

        action = Tabulate(
            headers=headers, rows=rows, tablefmt=tablefmt, theme=theme, method=method
        )

        logger.debug("The action has been initialized with: %s", action)
        action.setup()

    except Exception as error:
        logger.exception("Error while executing the action: %s", error)
        sys.exit(1)


if __name__ == "__main__":
    main()
