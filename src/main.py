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


def interpret(emulator, source, target):
    #
    """
    """
    emulator.free_vm()
    result = emulator.interpret(source, 0, False)

    return result, "".join(emulator.result.value_as.chars)[:-1] == target


def run_custom(emulator):
    #
    """
    """
    source = """\
let breakfast = "beignets";
let beverage = "cafe au lait";
breakfast = "beignets with " + beverage;

print breakfast;"""

    assert interpret(emulator, source, "beignets with cafe au lait")[1]

    source = """\
{
    let breakfast = "beignets";

    {
        let beverage = "cafe au lait";
        breakfast = "beignets with " + beverage;

        print breakfast;
    }
}"""

    assert interpret(emulator, source, "beignets with cafe au lait")[1]

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

    result, assertion = interpret(emulator, source, "beignets with cafe au lait")
    assert assertion
    assert result == vm.InterpretResult.INTERPRET_RUNTIME_ERROR

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

    result, assertion = interpret(emulator, source, "beignets with cafe au lait")
    assert assertion
    assert result == vm.InterpretResult.INTERPRET_RUNTIME_ERROR

    source = """\
let breakfast = "beignets";
let beverage = "cafe au lait";

if (false or true) {
    print breakfast;
} else {
    print beverage;
}"""

    assert interpret(emulator, source, "beignets")[1]

    source = """\
let breakfast = "beignets";
let beverage = "cafe au lait";

if (false and true) {
    print breakfast;
} else {
    print beverage;
}"""

    assert interpret(emulator, source, "cafe au lait")[1]

    source = """\
let breakfast = "beignets";
let counter = 0;

while (counter < 2) {
    breakfast = breakfast + " and beignets";
    counter = counter + 1;
}

print breakfast;"""

    assert interpret(emulator, source, "beignets and beignets and beignets")[1]

    source = """\
let breakfast = "beignets";

for (let counter = 0; counter < 2; counter = counter + 1) {
    breakfast = breakfast + " and beignets";
}

print breakfast;"""

    assert interpret(emulator, source, "beignets and beignets and beignets")[1]


if __name__ == "__main__":
    main()
