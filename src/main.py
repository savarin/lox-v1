import sys

import chunk
import debug
import vm


def main():
    emulator = vm.VM()
    size = len(sys.argv)

    if size == 1:
        # Run custom test instead of repl
        run_custom(emulator)
    elif size == 2:
        run_file(emulator, sys.argv[1])
    elif size == 3:
        run_file(emulator, sys.argv[1], sys.argv[2])
    else:
        print("Usage: clox [path]")
        exit_with_code(64)

    emulator.free_vm()


def exit_with_code(error_code):
    #
    """
    """
    print("Exit: {}".format(error_code))
    sys.exit()


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


def run_file(emulator, path, debug_level=0):
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


def run_custom(emulator):
    #
    """
    """
    source = """\
let breakfast = "beignets";
let beverage = "cafe au lait";
breakfast = "beignets with " + beverage;

print breakfast;"""

    emulator.free_vm()
    result = emulator.interpret(source, 0, False)
    assert "".join(
        emulator.result.value_as.chars)[:-1] == "beignets with cafe au lait"

    emulator.free_vm()

    source = """\
{
    let breakfast = "beignets";
    {
        let beverage = "cafe au lait";
        breakfast = "beignets with " + beverage;

        print breakfast;
    }
}"""

    emulator.free_vm()
    result = emulator.interpret(source, 0, False)
    assert "".join(
        emulator.result.value_as.chars)[:-1] == "beignets with cafe au lait"

    source = """\
{
    let breakfast = "beignets";
    {
        let beverage = "cafe au lait";
        breakfast = "beignets with " + beverage;

        print breakfast;
    }

    print beverage;
}"""

    emulator.free_vm()
    result = emulator.interpret(source, 0, False)
    assert "".join(
        emulator.result.value_as.chars)[:-1] == "beignets with cafe au lait"
    assert result == vm.InterpretResult.INTERPRET_RUNTIME_ERROR


if __name__ == "__main__":
    main()
