#! /usr/bin/python3
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
import os
import pyperclip
import shelve
import sys

logging.basicConfig(level=logging.DEBUG,
        format='[%(levelname)s] %(filename)s:%(lineno)d\n%(message)s')

def initialize_shelf(filename: str) -> int:
    """
    Create a shelf file.

    Create an empty shelf with the specified filename.

    Parameters:
        filename: the string to use as the shelf's name

    Return:
        0 -- shelf created successfully
        1 -- shelf with name 'filename' already exists
        2 -- other -- see stack trace
    """
    rc: int = 0

    try:
        if (not os.path.exists(filename)):
            shelf = shelve.open(filename)
            shelf.close()
        elif (os.path.exists(filename)):
            logging.error("Shelf '%s' already exists.", filename)
            rc = 1
    except:
        logging.error("Unkown error. Stacktrace: %s", sys.exc_info())
        rc = 2
    finally:
        return rc


def add(filename: "shelf", content: str, key: str) -> bool:
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

    if (key in filename.keys()):
        print(f"Key {key} already exists.")
        print(f"It contains: {filename[key]}")
        print("If you want to overwrite the contents, press ENTER.")
        print("Otherwise, press CTRL-C to abort.")
    try:
        input()
        filename[key] = content
        rc = True
    except KeyboardInterrupt:
        print("\nAborted.")
    except:
        logging.error("%s", sys.exc_info())
        rc = False
    finally:
        return rc


def copy(filename: "shelf", key: str) -> int:
    """
    Copy the contents of the specified key.

    Parameters:
        filename: the filename of the shelf to retrieve fromt
        key: The key to retrieve and copy from

    Return:
        0 -- key found, contents copied successfully
        1 -- key not found
        2 -- Operation aborted with CTRL-C
    """

    rc: int = 0

    print(f"Key {key} contains the following:")
    print(f"{filename[key]}\n")
    print("Is this what you want?")
    print("Press Enter to proceed.")
    try:
        input("Otherwise, press CTRL-C to abort.\n")
        pyperclip.copy(filename[key])
    except KeyboardInterrupt:
        print("\nAborted.")
        rc = 2
    except KeyError:
        logging.error("'%s' not found in %s. :( Did you mean another key?", key, filename)
        rc = 1
    finally:
        return rc


def confirm_delete(filename: "shelf", key: str) -> bool:
    """
    Display message to confirm key deletion.

    Parameters:
        filename: the shelf where the key exists
        key: the key pending deletion

    Return:
        True if the key is to be deleted, False otherwise
    """
    rc: bool = False
    confirm: str = input(f"Delete {key} from shelf? (y/n) ")

    if (confirm[0].lower() == 'y'):
        rc = True

    return rc


def delete_key(filename: "shelf", key: str) -> int:
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


def get_interactive(filename: "shelf") -> None:
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
        print(f"'{key}' already exists in the shelf")
        print(f"content: '{filename[key]}'")
        overwrite = input("Overwrite its contents? (y/n) ")
        if (overwrite[0].lower() == 'n'):
            print("Exiting...")
            return
        else:
            filename[key] = content
    else:
        print()
        print(f"Your key is {key} .")
        print(f"Your content is {content} .")
        print()
        try:
            print("If this is wrong, press CTRL-C to abort.")
            input("Else, press ENTER\n")
            filename[key] = content
        except KeyboardInterrupt:
            print("\nAborting...")
            return


def list_keys(filename: "shelf") -> None:
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


def purge(filename: "shelf") -> int:
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

    if (confirm[0].lower() == "y"):
        for key in filename.keys():
            filename.pop(key)
            rc += 1
    else:
        print("Purging aborted.")

    return rc


def setup_parser() -> "ArgumentParser":
    """
    Set up the option parser.

    Return:
        A reference to the created parser
    """

    parser = argparse.ArgumentParser(usage="python3 %(prog)s [options]",
            description="""Clipboard persistence -- save/load text from/to
            the clipboard"""
    )

    parser.add_argument("-a", "--add", nargs=2,
            metavar=('<content>', '<key>'),
            help="Store <content> as <key>"
    )

    parser.add_argument("-c", "--copy", metavar='<key>',
            help="Copy <key>'s contents to clipboard"
    )

    parser.add_argument("-d", "--delete", nargs="*", metavar="<keys>",
            help="Delete selected keys"
    )

    parser.add_argument("-i", "--interactive",
            action="store_true",
            help="Interactively enter a key and content"
    )

    parser.add_argument("-l", "--list", action="store_true",
            help="List all keys and content")

    parser.add_argument("-p", "--purge", action="store_true",
            help="Delete *ALL* keys and contents"
    )

    return parser


def main():
    filename: str = "mcb"

    if (not os.path.exists(filename)):
        initialize_shelf(filename)

    parser = setup_parser()
    args = parser.parse_args()

    if (len(sys.argv) == 1):
        parser.parse_args(['-h'])

    with shelve.open(filename) as shelf:

        if (args.add):
            content: str = args.add[0]
            key: str = args.add[1]

            rc: bool = add(shelf, content, key)

        elif (args.copy):
            key: str = args.copy
            rc: int = copy(shelf, key)

            if (rc == 1 or rc == 2):
                list_keys(shelf)

        elif (args.delete):
            for key in args.delete:
                go_ahead: bool = confirm_delete(shelf, key)
                if (go_ahead):
                    rc: int = delete_key(shelf, key)
                    if (rc == 1):
                        list_keys(shelf)

        elif (args.interactive):
            get_interactive(shelf)

        elif (args.list):
            list_keys(shelf)

        elif (args.purge):
            rc: int = purge(shelf)
            if (rc == 0):
                print("It looks like you didn't need to do that...")
                print("The shelf was already empty...")
            else:
                print("Purging successful.")
                print(f"Deleted {rc} keys.")


if __name__ == "__main__":
    main()
