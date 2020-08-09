#!/usr/bin/env python

# Copyright: Zoltan Puskas <sinustrom.info>, 2020
# License: GPLv3
#
# This tool will read an address book from abook and create a procmailrc rule
# that can be included for mail processing. Currently it produces an allowlist.

import click
import configparser
import logging
import sys
from pathlib import Path

VERSION = "0.3.1"
LICENSE = "GPLv3"
HOME = Path.home()


logging.basicConfig(format='%(message)s', level=logging.WARNING)
log = logging.getLogger("abook2procmailrc")


def get_email_from_abook(abook_path):
    email_addresses = []

    abook_path_resolved = Path(abook_path).expanduser()
    if not abook_path_resolved.is_file():
        log.error(f"{abook_path_resolved} does not exist or not a file!")
        sys.exit(1)

    try:
        open(abook_path_resolved)
    except PermissionError:
        log.error(
            f"Not enough permissions: {abook_path_resolved} is not readable."
        )
        sys.exit(1)

    parser = configparser.ConfigParser()
    parser.read(abook_path_resolved)
    for section in parser.sections():
        if "email" in parser[section]:
            email_addresses.extend(parser[section]["email"].split(','))

    return email_addresses


def write_procmail_rc(rc_path, email_list, action):
    rc_content = []

    # Add rule filters
    for email in email_list:
        email = email.replace(".", "\\.")
        rc_content.append(f"*$ $A2P_SUPREME^0 ^From.*<?{email}>?$")

    # Sorting the list only helps readability, procmail will keep processing
    # rules till a match is found
    rc_content.sort()

    # Add supreme scoring to the OR condition so we stop processing when
    # email address matches. See:
    # http://pm-doc.sourceforge.net/doc/#oring_and_score_recipe
    rc_content.insert(0, "A2P_SUPREME=9876543210")
    rc_content.insert(1, "")

    # Add rule starter line
    rc_content.insert(2, ":0")
    # Add rule action
    rc_content.append(action)

    if rc_path:
        rc_path_resolved = Path(rc_path).expanduser()
        try:
            with open(rc_path_resolved, 'w') as f:
                f.write('\n'.join(rc_content))
        except PermissionError:
            log.error(
                f"Not enough permissions: {rc_path_resolved} is not writeable."
            )
            sys.exit(1)
        except Exception as e:
            log.error(f"Writing rule file failed with error: {e}")
            sys.exit(1)

    else:
        print('\n'.join(rc_content))


@click.command(help="Turn abook address book into a procmail filter rule")
@click.version_option(version=VERSION,
                      message=f'%(prog)s v%(version)s, License: {LICENSE}')
@click.option("--action", "-t",
              default="$MAILDIR",
              show_default=True,
              help="Procmail action line override to store e-mail somewhere "
                   "else than the default INBOX. Use /dev/null to discard "
                   "messages, e.g. for spam filtering.")
@click.option("--address-book", "-a",
              default=f"{HOME}/.abook/addressbook",
              show_default=True,
              help="Path to the address book file")
@click.option("--procmailrc", "-p",
              default=None,
              help="Path to generated procmailrc include file (overwritten). "
              " [default: stdout]")
def cli(procmailrc, address_book, action):
    """
    CLI entry point. We read user options here and call the right functions
    """
    email_addresses = get_email_from_abook(address_book)
    write_procmail_rc(procmailrc, email_addresses, action)


if __name__ == "__main__":
    cli()
