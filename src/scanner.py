from enum import Enum


class TokenType(Enum):
    # Single-character tokens
    TOKEN_LEFT_PAREN = "TOKEN_LEFT_PAREN"
    TOKEN_RIGHT_PAREN = "TOKEN_RIGHT_PAREN"
    TOKEN_LEFT_BRACE = "TOKEN_LEFT_BRACE"
    TOKEN_RIGHT_BRACE = "TOKEN_RIGHT_BRACE"
    TOKEN_COMMA = "TOKEN_COMMA"
    TOKEN_DOT = "TOKEN_DOT"
    TOKEN_MINUS = "TOKEN_MINUS"
    TOKEN_PLUS = "TOKEN_PLUS"
    TOKEN_SEMICOLON = "TOKEN_SEMICOLON"
    TOKEN_SLASH = "TOKEN_SLASH"
    TOKEN_STAR = "TOKEN_STAR"

    # One or two character tokens
    TOKEN_BANG = "TOKEN_BANG"
    TOKEN_BANG_EQUAL = "TOKEN_BANG_EQUAL"
    TOKEN_EQUAL = "TOKEN_EQUAL"
    TOKEN_EQUAL_EQUAL = "TOKEN_EQUAL_EQUAL"
    TOKEN_GREATER = "TOKEN_GREATER"
    TOKEN_GREATER_EQUAL = "TOKEN_GREATER_EQUAL"
    TOKEN_LESS = "TOKEN_LESS"
    TOKEN_LESS_EQUAL = "TOKEN_LESS_EQUAL"

    # Literals
    TOKEN_IDENTIFIER = "TOKEN_IDENTIFIER"
    TOKEN_STRING = "TOKEN_STRING"
    TOKEN_NUMBER = "TOKEN_NUMBER"

    # Keywords
    TOKEN_AND = "TOKEN_AND"
    TOKEN_CLASS = "TOKEN_CLASS"
    TOKEN_ELSE = "TOKEN_ELSE"
    TOKEN_FALSE = "TOKEN_FALSE"
    TOKEN_FOR = "TOKEN_FOR"
    TOKEN_FUN = "TOKEN_FUN"
    TOKEN_IF = "TOKEN_IF"
    TOKEN_NIL = "TOKEN_NIL"
    TOKEN_OR = "TOKEN_OR"
    TOKEN_PRINT = "TOKEN_PRINT"
    TOKEN_RETURN = "TOKEN_RETURN"
    TOKEN_SUPER = "TOKEN_SUPER"
    TOKEN_THIS = "TOKEN_THIS"
    TOKEN_TRUE = "TOKEN_TRUE"
    TOKEN_VAR = "TOKEN_VAR"
    TOKEN_WHILE = "TOKEN_WHILE"
    TOKEN_ERROR = "TOKEN_ERROR"
    TOKEN_EOF = "TOKEN_EOF"


class Token():
    def __init__(self, token_type, start, length, source, line):
        # type: (TokenType, int, int, int) -> None
        """
        """
        self.token_type = token_type
        self.start = start
        self.length = length
        self.source = source
        self.line = line


single_token_map = {
    "(": TokenType.TOKEN_LEFT_PAREN,
    ")": TokenType.TOKEN_RIGHT_PAREN,
    "{": TokenType.TOKEN_LEFT_BRACE,
    "}": TokenType.TOKEN_RIGHT_BRACE,
    ";": TokenType.TOKEN_SEMICOLON,
    ",": TokenType.TOKEN_COMMA,
    ".": TokenType.TOKEN_DOT,
    "-": TokenType.TOKEN_MINUS,
    "+": TokenType.TOKEN_PLUS,
    "/": TokenType.TOKEN_SLASH,
    "*": TokenType.TOKEN_STAR,
}

double_token_map = {
    "!": (TokenType.TOKEN_BANG_EQUAL, TokenType.TOKEN_BANG),
    "=": (TokenType.TOKEN_EQUAL_EQUAL, TokenType.TOKEN_EQUAL),
    "<": (TokenType.TOKEN_LESS_EQUAL, TokenType.TOKEN_LESS),
    ">": (TokenType.TOKEN_GREATER_EQUAL, TokenType.TOKEN_GREATER),
}


class Scanner():
    def __init__(self, source):
        # type: (str) -> None
        """
        """
        self.start = 0  # pointer changed to int
        self.current = 0
        self.source = source
        self.line = 1

    def is_alpha(self, char):
        #
        """
        """
        return ((char >= "a" and char <= "z") or (char >= "A" and char <= "Z")
                or char == "_")

    def is_digit(self, char):
        #
        """
        """
        return char >= "0" and char <= "9"

    def is_at_end(self):
        #
        """
        """
        return self.current == len(self.source)

    def advance(self):
        #
        """
        """
        self.current += 1
        return self.source[self.current - 1]

    def peek(self):
        #
        """
        """
        return self.source[self.current]

    def peek_next(self):
        #
        """
        """
        return self.source[self.current + 1]

    def match(self, expected):
        #
        """
        """
        if self.is_at_end():
            return False

        elif self.source[self.current] != expected:
            return False

        self.current += 1
        return True

    def make_token(self, token_type):
        #
        """
        """
        return Token(
            token_type=token_type,
            start=self.start,
            length=self.current - self.start,
            source=self.source[self.start:self.current],
            line=self.line,
        )

    def error_token(self, message):
        #
        """
        """
        print("Error: {}".format(message))
        return self.make_token(TokenType.TOKEN_ERROR)

    def skip_whitespace(self):
        #
        """
        """
        while True:
            # Check since not using EOF marker
            if self.is_at_end():
                return None

            char = self.peek()

            if char in [" ", "\r", "\t"]:
                self.advance()
                continue

            elif char == "\n":
                self.line += 1
                self.advance()
                continue

            elif char == "/":
                if self.peek_next() == "/":
                    while self.peek() != "\n" and not self.is_at_end():
                        self.advance()
                    continue
                else:
                    return None

            return None

    def check_keyword(self, start, length, rest, token_type):
        #
        """
        """
        index = self.start + start

        if (self.current - self.start == start +
                length) and (self.source[index:index + length] == rest):
            return token_type

    def identifier_type(self):
        #
        """
        """
        char = self.source[self.start]

        if char == "a":
            return self.check_keyword(1, 2, "nd", TokenType.TOKEN_AND)
        elif char == "c":
            return self.check_keyword(1, 4, "lass", TokenType.TOKEN_CLASS)
        elif char == "e":
            return self.check_keyword(1, 3, "lse", TokenType.TOKEN_ELSE)
        elif char == "i":
            return self.check_keyword(1, 1, "f", TokenType.TOKEN_IF)
        elif char == "l":
            return self.check_keyword(1, 2, "et", TokenType.TOKEN_VAR)
        elif char == "n":
            return self.check_keyword(1, 2, "il", TokenType.TOKEN_NIL)
        elif char == "o":
            return self.check_keyword(1, 1, "r", TokenType.TOKEN_OR)
        elif char == "p":
            return self.check_keyword(1, 4, "rint", TokenType.TOKEN_PRINT)
        elif char == "r":
            return self.check_keyword(1, 5, "eturn", TokenType.TOKEN_RETURN)
        elif char == "s":
            return self.check_keyword(1, 4, "uper", TokenType.TOKEN_SUPER)
        elif char == "w":
            return self.check_keyword(1, 4, "hile", TokenType.TOKEN_WHILE)

        elif char == "f":
            if self.current - self.start > 1:
                next_char = self.source[self.start + 1]
                if next_char == "a":
                    return self.check_keyword(2, 3, "lse", TOKEN_FALSE)
                if next_char == "o":
                    return self.check_keyword(2, 1, "r", TOKEN_FOR)
                if next_char == "u":
                    return self.check_keyword(2, 1, "n", TOKEN_FUN)

        elif char == "t":
            if self.current - self.start > 1:
                next_char = self.source[self.start + 1]
                if next_char == "h":
                    return self.check_keyword(2, 2, "is", TOKEN_THIS)
                if next_char == "r":
                    return self.check_keyword(2, 2, "ue", TOKEN_TRUE)

        return TokenType.TOKEN_IDENTIFIER

    def identifier(self):
        #
        """
        """
        while self.is_alpha(self.peek()) or self.is_digit(self.peek()):
            self.advance()

        return self.make_token(self.identifier_type())

    def number(self):
        #
        """
        """
        while self.is_digit(self.peek()):
            self.advance()

        # Look for a fractional part
        if self.peek() == "." and self.is_digit(self.peek_next()):
            # Consume the period
            self.advance()

            while self.is_digit(self.peek()):
                self.advance()

        return self.make_token(TokenType.TOKEN_NUMBER)

    def string(self):
        #
        """
        """
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == "\n":
                self.line += 1
            self.advance()

        if self.is_at_end():
            return error_token("Unterminated string.")

        # The closing quote
        self.advance()
        return self.make_token(TokenType.TOKEN_STRING)

    def scan_token(self):
        # type: () -> Token
        """
        """
        self.skip_whitespace()
        self.start = self.current

        if self.is_at_end():
            return self.make_token(TokenType.TOKEN_EOF)

        char = self.advance()

        if self.is_alpha(char):
            return self.identifier()

        elif self.is_digit(char):
            return self.number()

        elif char in single_token_map:
            return self.make_token(single_token_map[char])

        elif char in double_token_map:
            if self.match("="):
                return self.make_token(double_token_map[char][0])
            else:
                return self.make_token(double_token_map[char][1])

        if char == '"':
            return self.string()

        return self.error_token("Unexpected character.")
