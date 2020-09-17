from typing import Any

import scanner


def compile(source):
    # type: (str) -> None
    """
    """
    reader = scanner.Scanner(source)
    line = -1

    while True:
        token = reader.scan_token()

        if token.line != line:
            print("{:04d}".format(token.line), end=" ")
            line = token.line
        else:
            print("   |", end=" ")

        current_token = reader.source[token.start:(token.start + token.length)]
        print("{} '{}'".format(token.token_type, current_token))

        if token.token_type == scanner.TokenType.TOKEN_EOF:
            break
