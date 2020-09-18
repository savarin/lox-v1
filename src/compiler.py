from typing import Any, TYPE_CHECKING

import scanner

if TYPE_CHECKING:
    import chunk


class Parser():
    def __init__(self, reader):
        #
        """
        """
        self.reader = reader
        self.current = None
        self.previous = None
        self.had_error = False
        self.panic_mode = False

    def advance(self):
        # type: () -> None
        """
        """
        self.previous = self.current

        while True:
            self.current = self.reader.scan_token()

            if self.current.type != scanner.TokenType.TOKEN_ERROR:
                break

            error_at_current(self.current.start)

    def consume(self, token_type, message):
        # type: (scanner.TokenType, str) -> None
        """
        """
        if self.current.token_type == token_type:
            self.advance()
            return None

        self.error_at_current(message)

    def error_at_current(self, message):
        #
        """
        """
        error_at(self.current, message)

    def error(message):
        #
        """
        """
        error_at(self.previous, message)

    def error_at(token, message):
        #
        """
        """
        if self.panic_mode:
            return None

        self.panic_mode = True

        print("[line {}] Error".format(token.line), end=" ")

        if token.token_type == scanner.TokenType.TOKEN_EOF:
            print(" at end", end=" ")
        elif token.type == scanner.TokenType.TOKEN_ERROR:
            pass
        else:
            current_token = self.reader.source[token.start:(token.start +
                                                            token.length)]
            print(" at {}".format(current_token), end=" ")

        print(": {}".format(message))
        self.had_error = True


def compile(source, bytecode):
    # type: (str, chunk.Chunk) -> None
    """
    """
    reader = scanner.Scanner(source)
    viewer = Parser(reader)

    viewer.advance()
    expression()
    consume(scanner.TokenType.TOKEN_EOF, "Expect end of expression.")

    return not viewer.had_error
