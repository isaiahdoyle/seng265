#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 01 08:35:33 2022
@author: rivera

This is a text processor that allows to translate XML-based events to YAML-based events.
CAREFUL: You ARE NOT allowed using (i.e., import) modules/libraries/packages to parse XML or YAML
(e.g., yaml or xml modules). You will need to rely on Python collections to achieve the reading of XML files and the
generation of YAML files.
"""
import sys


def print_hello_message(message):
    """Prints a welcome message.

    Parameters
    ----------
    message : str, required
        The file path of the file to read.

    Returns
    -------
    void
        This function is not expected to return anything
    """
    print(message)


def main():
    """The main entry point for the program.
    """
    # Calling a dummy function to illustrate the process in Python
    print('Hi! from:', sys.argv[0])


if __name__ == '__main__':
    main()
