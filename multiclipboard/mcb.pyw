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

def add(filename: str, key: str, content: str) -> bool:
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


def copy(filename: str, key: str) -> int:
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


def confirm_delete(filename: str, key: str) -> bool:
    """
    Display message to confirm key deletion.

    Parameters:
        filename: the shelf where the key exists
        key: the key pending deletion

    Return:
        True if the key is to be deleted, False otherwise
    """
    rc: bool = False
    confirm: str = input(f"Delete {key} from {filename}? (y/n) ")

    if (confirm[0].lower() == 'y'):
        rc = True

    return rc


def delete_key(filename: str, key: str) -> int:
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


def get_interactive(filename: str) -> None:
    """
    Interactively prompt user for a key and content.

    Use stdin to interactively get a key and content from the user. If the user
    specifies a key that already exists, will ask for confirmation before
    overwriting the old contents.

    Parameters:
        filename: the shelf to check in, and save to

    Return:
        None. Because the all information is coming from stdin, copying is not
        involved. Additionally, the user is prompted if the key they want
        already exists -- they overwrite at their own discretion.
    """

    content: str = input("Enter the text you want to save: ")
    key: str = input("Enter the key you want to save it as: ")

    overwrite: str = "y"

    if (key in filename.keys()):
        print(f"'{key}' already exists in {filename}")
        print(f"content: '{content}'")
        overwrite = input("Overwrite its contents? (y/n) ")
        if (overwrite[0].lower() == 'n'):
            print("Exiting...")
            return
        else:
            pass
    else:
        filename[key] = content


def list_keys(filename: str) -> None:
    """
    List all keys in the specified file

    Parameters:
        filename: the shelf to search and list

    Return:
        None
    """

    for key in filename.keys():
        print(f"Key: {key}")
        print(f"Contents: {filename[key]}")
        print()


def purge(filename: str) -> int:
    """
    Delete all keys in the shelf.

    Delete all keys in shelf specified by filename. Only prompts for
    confirmation before the first delete operation.

    Parameters:
        filename: the shelf to purge

    Return:
        The number of keys deleted
    """

    rc: int = 0
    confirm: str = "n"

    print("This will delete *ALL* keys and content from the shelf.")
    confirm = input("Are you sure you want to do this? (y/n) ")

    if (confirm[0],lower() == "y"):
        for key in filename.keys():
            filename.pop(key)
            rc += 1
    else:
        print("Purging aborted.")

    return rc
