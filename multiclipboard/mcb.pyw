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
