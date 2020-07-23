#!/usr/bin/env python

# Copyright: Zoltan Puskas <sinustrom.info>, 2020
# License: GPLv3
#
# This tool will read an address book from abook and create a procmailrc rule
# that can be included for mail processing. Currently it produces an allowlist.

import click
import configparser
import logging
import os
import sys

VERSION = "0.1.0"
LICENSE = "GPLv3"
HOME = os.getenv("HOME")


log = logging.getLogger("abook2procmailrc")
log.setLevel(logging.WARNING)


def get_email_from_abook(abook_path):
    email_addresses = []

    try:
        open(abook_path)
    except PermissionError:
        log.error(
            f"Insufficient permissions: {abook_path} is not readable."
        )
        sys.exit(1)

    parser = configparser.ConfigParser()
    parser.read(abook_path)
    for section in parser.sections():
        if "email" in parser[section]:
            email_addresses.extend(parser[section]["email"].split(','))

    return email_addresses


def write_procmail_rc(path, email_list):
    rc_content = []

    # Add rule filters
    for email in email_list:
        email = email.replace(".", "\\.")
        rc_content.append(f"*$ $SUPREME^0 ^From.*<?{email}>?$")

    # Sorting the list only helps readability, procmail will keep processing
    # rules till a match is found
    rc_content.sort()

    # Add rule starter line
    rc_content.insert(0, ":0")
    # Add rule action
    rc_content.append("$MAILDIR")

    if path:
        try:
            with open(path, 'w') as f:
                f.write('\n'.join(rc_content))
        except PermissionError:
            log.error(
                f"Insufficient permissions: {path} is not writeable."
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
@click.option("--address-book", "-a",
              default=f"{HOME}/.abook/addressbook",
              help="Path to the address book file")
@click.option("--procmailrc", "-p",
              default=None,
              help="Path to generated procmailrc include file (overwritten)")
def cli(procmailrc, address_book):
    """
    CLI entry point. We read user options here and call the right functions
    """
    email_addresses = get_email_from_abook(address_book)
    write_procmail_rc(procmailrc, email_addresses)


if __name__ == "__main__":
    cli()
