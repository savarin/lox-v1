from enum import Enum
from typing import Any

import chunk
import debug
import scanner
import value

DEBUG_PRINT_CODE = True

UINT8_MAX = 256


# yapf: disable
class Precedence(Enum):
    PREC_NONE = 1
    PREC_ASSIGNMENT = 2  # =
    PREC_OR = 3          # or
    PREC_AND = 4         # and
    PREC_EQUALITY = 5    # == !=
    PREC_COMPARISON = 6  # < > <= >=
    PREC_TERM = 7        # + -
    PREC_FACTOR = 8      # * /
    PREC_UNARY = 9       # ! -
    PREC_CALL = 10       # . ()
    PREC_PRIMARY = 11
# yapf: enable


class ParseRule():
    def __init__(self, prefix, infix, precedence):
        #
        """
        """
        self.prefix = prefix
        self.infix = infix
        self.precedence = precedence


# yapf: disable
rule_map = {
    "TOKEN_LEFT_PAREN":    ["grouping", None,     "PREC_NONE"],
    "TOKEN_RIGHT_PAREN":   [None,       None,     "PREC_NONE"],
    "TOKEN_LEFT_BRACE":    [None,       None,     "PREC_NONE"],
    "TOKEN_RIGHT_BRACE":   [None,       None,     "PREC_NONE"],
    "TOKEN_COMMA":         [None,       None,     "PREC_NONE"],
    "TOKEN_DOT":           [None,       None,     "PREC_NONE"],
    "TOKEN_MINUS":         ["unary",    "binary", "PREC_TERM"],
    "TOKEN_PLUS":          [None,       "binary", "PREC_TERM"],
    "TOKEN_SEMICOLON":     [None,       None,     "PREC_NONE"],
    "TOKEN_SLASH":         [None,       "binary", "PREC_FACTOR"],
    "TOKEN_STAR":          [None,       "binary", "PREC_FACTOR"],
    "TOKEN_BANG":          ["unary",    None,     "PREC_NONE"],
    "TOKEN_BANG_EQUAL":    [None,       "binary", "PREC_EQUALITY"],
    "TOKEN_EQUAL":         [None,       None,     "PREC_NONE"],
    "TOKEN_EQUAL_EQUAL":   [None,       "binary", "PREC_EQUALITY"],
    "TOKEN_GREATER":       [None,       "binary", "PREC_COMPARISON"],
    "TOKEN_GREATER_EQUAL": [None,       "binary", "PREC_COMPARISON"],
    "TOKEN_LESS":          [None,       "binary", "PREC_COMPARISON"],
    "TOKEN_LESS_EQUAL":    [None,       "binary", "PREC_COMPARISON"],
    "TOKEN_IDENTIFIER":    ["variable", None,     "PREC_NONE"],
    "TOKEN_STRING":        ["string",   None,     "PREC_NONE"],
    "TOKEN_NUMBER":        ["number",   None,     "PREC_NONE"],
    "TOKEN_AND":           [None,       None,     "PREC_NONE"],
    "TOKEN_CLASS":         [None,       None,     "PREC_NONE"],
    "TOKEN_ELSE":          [None,       None,     "PREC_NONE"],
    "TOKEN_FALSE":         ["literal",  None,     "PREC_NONE"],
    "TOKEN_FOR":           [None,       None,     "PREC_NONE"],
    "TOKEN_FUN":           [None,       None,     "PREC_NONE"],
    "TOKEN_IF":            [None,       None,     "PREC_NONE"],
    "TOKEN_NIL":           ["literal",  None,     "PREC_NONE"],
    "TOKEN_OR":            [None,       None,     "PREC_NONE"],
    "TOKEN_PRINT":         [None,       None,     "PREC_NONE"],
    "TOKEN_RETURN":        [None,       None,     "PREC_NONE"],
    "TOKEN_SUPER":         [None,       None,     "PREC_NONE"],
    "TOKEN_THIS":          [None,       None,     "PREC_NONE"],
    "TOKEN_TRUE":          ["literal",  None,     "PREC_NONE"],
    "TOKEN_VAR":           [None,       None,     "PREC_NONE"],
    "TOKEN_WHILE":         [None,       None,     "PREC_NONE"],
    "TOKEN_ERROR":         [None,       None,     "PREC_NONE"],
    "TOKEN_EOF":           [None,       None,     "PREC_NONE"],
}
# yapf: enable


class Parser():
    def __init__(self, reader, bytecode, debug):
        # type: (scanner.Scanner, chunk.Chunk, bool) -> None
        """
        """
        self.reader = reader
        self.bytecode = bytecode  # referred to in text as compiling_chunk
        self.current = None
        self.previous = None
        self.had_error = False
        self.panic_mode = False
        self.debug = debug

    def current_chunk(self):
        #
        """
        """
        return self.bytecode

    def error_at(self, token, message):
        #
        """
        """
        if self.panic_mode:
            return None

        self.panic_mode = True

        print("[line {}] Error".format(token.line), end=" ")

        if token.token_type == scanner.TokenType.TOKEN_EOF:
            print(" at end", end=" ")
        elif token.token_type == scanner.TokenType.TOKEN_ERROR:
            pass
        else:
            current_token = self.reader.source[token.start:(token.start +
                                                            token.length)]
            print("at {}".format(current_token), end="")

        print(": {}".format(message))
        self.had_error = True

    def error(self, message):
        #
        """
        """
        self.error_at(self.previous, message)

    def error_at_current(self, message):
        #
        """
        """
        self.error_at(self.current, message)

    def advance(self):
        # type: () -> None
        """
        """
        self.previous = self.current

        while True:
            self.current = self.reader.scan_token()

            if self.current.token_type != scanner.TokenType.TOKEN_ERROR:
                break

            self.error_at_current(self.current.start)

    def consume(self, token_type, message):
        # type: (scanner.TokenType, str) -> None
        """
        """
        if self.current.token_type == token_type:
            self.advance()
            return None

        self.error_at_current(message)

    def match(self, token_type):
        #
        """
        """
        if not self.check(token_type):
            return False

        self.advance()
        return True

    def check(self, token_type):
        #
        """
        """
        return self.current.token_type == token_type

    def emit_byte(self, byte):
        #
        """
        """
        self.current_chunk().write_chunk(byte, self.previous.line)

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

    def make_constant(self, val):
        #
        """
        """
        constant = self.current_chunk().add_constant(val)

        if constant > UINT8_MAX:
            self.error("Too many constants in one chunk.")
            return None

        return constant

    def emit_constant(self, val):
        #
        """
        """
        self.emit_bytes(chunk.OpCode.OP_CONSTANT, self.make_constant(val))

    def end_compiler(self):
        #
        """
        """
        self.emit_return()

        if self.debug and not self.had_error:
            debug.disassemble_chunk(self.current_chunk(), "code")

    def binary(self, can_assign):
        #
        """
        """
        # Remember the operator
        operator_type = self.previous.token_type

        # Compile the right operand.
        rule = self.get_rule(operator_type)

        # Get precedence which has 1 priority level above precedence of current rule
        precedence = Precedence(rule.precedence.value + 1)
        self.parse_precedence(precedence)

        if operator_type == scanner.TokenType.TOKEN_BANG_EQUAL:
            self.emit_bytes(chunk.OpCode.OP_EQUAL, chunk.OpCode.OP_NOT)
        elif operator_type == scanner.TokenType.TOKEN_EQUAL_EQUAL:
            self.emit_byte(chunk.OpCode.OP_EQUAL)
        elif operator_type == scanner.TokenType.TOKEN_GREATER:
            self.emit_byte(chunk.OpCode.OP_GREATER)
        elif operator_type == scanner.TokenType.TOKEN_GREATER_EQUAL:
            self.emit_bytes(chunk.OpCode.OP_LESS, chunk.OpCode.OP_NOT)
        elif operator_type == scanner.TokenType.TOKEN_LESS:
            self.emit_byte(chunk.OpCode.OP_LESS)
        elif operator_type == scanner.TokenType.TOKEN_LESS_EQUAL:
            self.emit_bytes(chunk.OpCode.OP_GREATER, chunk.OpCode.OP_NOT)
        elif operator_type == scanner.TokenType.TOKEN_PLUS:
            self.emit_byte(chunk.OpCode.OP_ADD)
        elif operator_type == scanner.TokenType.TOKEN_MINUS:
            self.emit_byte(chunk.OpCode.OP_SUBTRACT)
        elif operator_type == scanner.TokenType.TOKEN_STAR:
            self.emit_byte(chunk.OpCode.OP_MULTIPLY)
        elif operator_type == scanner.TokenType.TOKEN_SLASH:
            self.emit_byte(chunk.OpCode.OP_DIVIDE)

    def literal(self, can_assign):
        #
        """
        """
        if self.previous.token_type == scanner.TokenType.TOKEN_FALSE:
            self.emit_byte(chunk.OpCode.OP_FALSE)
        elif self.previous.token_type == scanner.TokenType.TOKEN_NIL:
            self.emit_byte(chunk.OpCode.OP_NIL)
        elif self.previous.token_type == scanner.TokenType.TOKEN_TRUE:
            self.emit_byte(chunk.OpCode.OP_TRUE)

    def grouping(self, can_assign):
        #
        """
        """
        self.expression()
        self.consume(
            scanner.TokenType.TOKEN_RIGHT_PAREN,
            "Expect ')' after expression.",
        )

    def number(self, can_assign):
        #
        """
        """
        val = float(self.previous.source)
        self.emit_constant(value.number_val(val))

    def string(self, can_assign):
        # type: () -> None
        """Extracts relevant section from string, wraps in a ObjectString, wraps
        in a Value and append to the stack."""
        # Start from position after quote
        chars = self.previous.source[1:self.previous.length - 1]

        # End from position before quote and end of string token
        val = value.copy_string(chars, self.previous.length - 2)

        self.emit_constant(value.obj_val(val))

    def named_variable(self, name, can_assign):
        #
        """
        """
        arg = self.identifier_constant(name)

        if can_assign and self.match(scanner.TokenType.TOKEN_EQUAL):
            self.expression()
            self.emit_bytes(chunk.OpCode.OP_SET_GLOBAL, arg)
        else:
            self.emit_bytes(chunk.OpCode.OP_GET_GLOBAL, arg)

    def variable(self, can_assign):
        # type: (bool) -> None
        """
        """
        self.named_variable(self.previous, can_assign)

    def unary(self, can_assign):
        #
        """
        """
        operator_type = self.previous.token_type

        # Compile the operand
        self.parse_precedence(Precedence.PREC_UNARY)

        # Emit the operator instruction
        if operator_type == scanner.TokenType.TOKEN_BANG:
            self.emit_byte(chunk.OpCode.OP_NOT)
        elif operator_type == scanner.TokenType.TOKEN_MINUS:
            self.emit_byte(chunk.OpCode.OP_NEGATE)

    def parse_precedence(self, precedence):
        #
        """
        """
        self.advance()
        prefix_rule = self.get_rule(self.previous.token_type).prefix

        if prefix_rule is None:
            self.error("Expect expression")
            return None

        can_assign = precedence.value <= Precedence.PREC_ASSIGNMENT.value
        prefix_rule(can_assign)

        while precedence.value <= self.get_rule(
                self.current.token_type).precedence.value:
            self.advance()

            infix_rule = self.get_rule(self.previous.token_type).infix
            infix_rule(can_assign)

        # Error if '=' not consumed as part of expression
        if can_assign and self.match(scanner.TokenType.TOKEN_EQUAL):
            self.error("Invalid assignment target.")

    def identifier_constant(self, name):
        #
        """
        """
        chars = name.source[:name.length]
        obj_val = value.obj_val(value.copy_string(chars, name.length))
        return self.make_constant(obj_val)

    def parse_variable(self, error_message):
        #
        """
        """
        self.consume(scanner.TokenType.TOKEN_IDENTIFIER, error_message)
        return self.identifier_constant(self.previous)

    def define_variable(self, global_var):
        #
        """
        """
        self.emit_bytes(chunk.OpCode.OP_DEFINE_GLOBAL, global_var)

    def get_rule(self, token_type):
        # type: (TokenType) -> ParseRule
        """Custom function to convert TokenType to ParseRule. This allows the
        rule_map to consist of strings, which are then replaced by respective
        classes in the conversion process.
        """
        type_map = {
            "binary": self.binary,
            "grouping": self.grouping,
            "literal": self.literal,
            "number": self.number,
            "string": self.string,
            "unary": self.unary,
            "variable": self.variable,
        }

        rule = rule_map[token_type.name]

        return ParseRule(
            prefix=type_map.get(rule[0], None),
            infix=type_map.get(rule[1], None),
            precedence=Precedence[rule[2]],
        )

    def expression(self):
        #
        """
        """
        self.parse_precedence(Precedence.PREC_ASSIGNMENT)

    def var_declaration(self):
        #
        """
        """
        global_var = self.parse_variable("Expect variable name.")

        if self.match(scanner.TokenType.TOKEN_EQUAL):
            self.expression()
        else:
            self.emit_byte(chunk.OpCode.OP_NIL)

        self.consume(scanner.TokenType.TOKEN_SEMICOLON,
                     "Expect ';' after variable declaration")

        self.define_variable(global_var)

    def expression_statement(self):
        #
        """
        """
        self.expression()
        self.consume(scanner.TokenType.TOKEN_SEMICOLON,
                     "Expect ';' after expression.")
        self.emit_byte(chunk.OpCode.OP_POP)

    def print_statement(self):
        #
        """
        """
        self.expression()
        self.consume(scanner.TokenType.TOKEN_SEMICOLON,
                     "Expect ';' after value.")
        self.emit_byte(chunk.OpCode.OP_PRINT)

    def synchronize(self):
        #
        """
        """
        self.panic_mode = False

        while self.current.token_type != scanner.TokenType.TOKEN_EOF:
            if self.previous.token_type == scanner.TokenType.TOKEN_SEMICOLON:
                return None

            if self.current.token_type == scanner.TokenType.TOKEN_RETURN:
                return None

            self.advance()

    def declaration(self):
        #
        """
        """
        if self.match(scanner.TokenType.TOKEN_VAR):
            self.var_declaration()
        else:
            self.statement()

        if self.panic_mode:
            self.synchronize()

    def statement(self):
        #
        """
        """
        if self.match(scanner.TokenType.TOKEN_PRINT):
            self.print_statement()
        else:
            self.expression_statement()


def compile(source, bytecode, debug):
    # type: (str, chunk.Chunk, bool) -> None
    """KIV change this to Compiler class with method compile."""
    reader = scanner.Scanner(source)
    parser = Parser(reader=reader, bytecode=bytecode, debug=debug)

    parser.advance()

    while not parser.match(scanner.TokenType.TOKEN_EOF):
        parser.declaration()

    parser.end_compiler()

    return not parser.had_error
