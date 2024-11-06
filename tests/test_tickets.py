from pre_ticket.tickets import is_ticket_in_message
import pytest


with_ticket_1 = """#1234 Updated some code

# Please enter the commit message for your changes. Lines starting
# with '#' will be ignored.
"""

with_ticket_2 = """Updated some code

Ref: #1234

# Please enter the commit message for your changes. Lines starting
# with '#' will be ignored.
"""

without_ticket_1 = ""

without_ticket_2 = """Updated some code

# 1234
# Please enter the commit message for your changes. Lines starting
# with '#' will be ignored.
"""

@pytest.mark.parametrize(
    ("content", "expected_result"),
    [
        (without_ticket_1, False),
        (without_ticket_2, False),
        (with_ticket_1, True),
        (with_ticket_2, True),
    ]
)
def test_is_ticket_in_message(content, expected_result):
    assert is_ticket_in_message(content, "1234") is expected_result
