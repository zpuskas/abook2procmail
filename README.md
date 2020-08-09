# abook2procmail

A simple script to generate [procmail](http://www.procmail.org/) rules from
[abook](http://abook.sourceforge.net/) based address books.

## Usage

Generate an address book rule by running:

```
$ abook2procmail --procmailrc ~/.procmail/abook.rc
```

Then in the `~/.procmailrc`, close to the top of the file,  add the following
line:

```
INCLUDERC=$HOME/.procmail/abook.rc
```

and enjoy e-mail from the address book landing in the INBOX.

If there are multiple address books, one can use the `--address-book` option to
override the source and the `--action` option to override what to do with the
messages. If multiple rc files are generated, multiple includes will have to be
added.

To ensure that the filtering rules are up to date one can set up a periodic
cron job (e.g. once a day) to regenerate the rc file.

## Dependencies

- Python 3.8 or later
- [click](https://click.palletsprojects.com/en/7.x/) 7.x or later

## License

Copyright (C) 2020 Zoltan Puskas  
Licensed under GPLv3
