import sys

import chunk
import debug
import vm


def repl(emulator):
    #
    """
    """
    while True:
        line = input("> ")

        if not line:
            print("")
            break

        emulator.interpret(line)


def run_file(path, debug_level=0):
    #
    """
    """
    with open(path, "r") as f:
        source = f.read()

    result = emulator.interpret(source, int(debug_level), True)

    if result == vm.InterpretResult.INTERPRET_COMPILE_ERROR:
        exit_with_code(65)

    elif result == vm.InterpretResult.INTERPRET_RUNTIME_ERROR:
        exit_with_code(70)


def run_custom():
    #
    """
    """
    source = [
        """\
let breakfast = "beignets";
let beverage = "cafe au lait";
breakfast = "beignets with " + beverage;

print breakfast;""",
    ]

    result = emulator.interpret(source[0], 0, False)
    assert "".join(
        emulator.result.value_as.chars)[:-1] == "beignets with cafe au lait"


def exit_with_code(error_code):
    #
    """
    """
    print("Exit: {}".format(error_code))
    sys.exit()


if __name__ == "__main__":
    emulator = vm.VM()
    size = len(sys.argv)

    if size == 1:
        # Run custom test instead of repl
        run_custom()
    elif size == 2:
        run_file(sys.argv[1])
    elif size == 3:
        run_file(sys.argv[1], sys.argv[2])
    else:
        print("Usage: clox [path]")
        exit_with_code(64)

    emulator.free_vm()
