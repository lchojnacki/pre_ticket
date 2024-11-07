import io
import re

import six

from .commands import call_command


def get_current_branch():
    return call_command(["git", "rev-parse", "--abbrev-ref", "HEAD"])


def retrieve_ticket(branch, regex):
    matches = re.match(regex, branch)
    if matches:
        ticket_number = matches.group("ticket")
        return ticket_number


def is_ticket_in_message(contents, ticket):
    """
    Checks if a specified ticket is present in the given message contents.

    This function scans through each line of the provided message contents,
    ignoring empty lines and comments (except for the first line), to determine
    if the specified ticket is mentioned. It performs a case-insensitive search
    for the ticket within the non-empty, non-comment lines.

    The first line is an exception because some conventions assume that the task
    number preceded by a hashtag will appear at the beginning of the commit
    message: "#123 Commit Message".

    Examples:
    >>> is_ticket_in_message("This is a message with ticket #123", "#123")
    True
    >>> is_ticket_in_message("This is a message without a ticket", "#123")
    False
    >>> is_ticket_in_message("#123 This is a message with a ticket", "#123")
    True
    """
    for i, line in enumerate(contents.splitlines()):
        stripped = line.strip().lower()

        if stripped == "" or (stripped.startswith("#") and i != 0):
            continue

        if ticket.lower() in stripped:
            return True

    return False

def add_ticket_number(filename, regex, format_template):
    branch = get_current_branch()
    ticket_number = retrieve_ticket(branch, regex)

    if ticket_number:
        with io.open(filename, "r+") as fd:
            contents = fd.read()

            if (
                is_ticket_in_message(contents, ticket_number)
                or not contents[:contents.find("\n")]
            ):
                return

            ticket_msg = format_template.format(message=contents, ticket=ticket_number)
            fd.seek(0)
            fd.write(six.text_type(ticket_msg))
            fd.truncate()
