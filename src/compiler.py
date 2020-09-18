from typing import Any, TYPE_CHECKING

import scanner

if TYPE_CHECKING:
    import chunk


class Parser():
    def __init__(self, reader, bytecode):
        #
        """
        """
        self.reader = reader
        self.bytecode = bytecode
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

    def emit_byte(self, byte):
        #
        """
        """
        self.bytecode.write_chunk(byte, self.previous.line)

    def emit_bytes(self, byte1, byte2):
        #
        """
        """
        self.emit_byte(byte1)
        self.emit_byte(byte2)

    def emit_return(self):
        #
        """
        """
        self.emit_byte(chunk.OpCode.OP_RETURN)

    def end_compiler(self):
        #
        """
        """
        self.emit_return()

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
    # compiling_chunk = bytecode
    viewer = Parser(reader, bytecode)

    viewer.advance()
    expression()
    consume(scanner.TokenType.TOKEN_EOF, "Expect end of expression.")
    end_compiler()

    return not viewer.had_error
