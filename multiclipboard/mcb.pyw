#! python3
# mcb.pyw - Saves and loads pieces of text to the clipboard
#
# Usage:    python3 mcb.pyw [options]
#
# Options:
#           -a, --add <content> <key> - Store <content> as <key>
#           -c, --copy <key>          - Copy <key>'s contents to clipboard for
#                                       usage
#           -d, --delete [<keys>]     - Delete <keys> and associated content
#           -i, --interactive         - Use stdin to interactively add a key
#                                       and content
#           -l, --list                - List all keys and their contents
#           -p, --purge               - Delete *ALL* keys and contents

import argparse
import logging
import pyperclip
import shelve
import sys

logging.basicConfig(level=logging.DEBUG,
        format='[%(levelname)s] %(filename)s:%(lineno)d %(message)s')

def add(filename: str, key: str, content: str):
    """
    Add the specified contents to the shelf.

    Add the content to the specified shelf, saved as the specified key.

    Parameters:
        filename: The filename of the shelf to save to
        key: The string to use as the key
        content: The actual content to save

    Return:
        True if successful, False otherwise
    """
    rc: bool = False
    try:
        filename[key] = content
        rc = True
    except:
        logging.error("%s", sys.exc_info())
        rc = False
    finally:
        return rc


def copy(filename: str, key: str):
    """
    Copy the contents of the specified key.

    Parameters:
        filename: the filename of the shelf to retrieve fromt
        key: The key to retrieve and copy from

    Return:
        0 -- key found, contents copied successfully
        1 -- key not found
    """

    rc: int = 0

    try:
        pyperclip.copy(filename[key])
    except KeyError:
        logging.error("'%s' not found in %s. :( Did you mean another key?", key, filename)
        rc = 1
    finally:
        return rc


def delete_key(filename: str, key: str):
    """
    Delete a key from the shelf.

    Delete the specified key from the shelf.

    Parameters:
        filename: the filename of the shelf where the key exists
        key: the key to delete

    Return:
        0 -- Key found and successfully deleted
        1 -- Key not found
    """

    rc: int = 0
    try:
        filename.pop(key)
    except KeyError:
        logging.error("'%s' not found in '%s' :(. Did you mean a different key?",
                key, filename)
        rc = 1
    finally:
        return rc
