import argparse
import importlib
import inspect
from ast import parse
from contextlib import suppress
from pathlib import Path

from private_calls.private_calls_check.find_call import FindCall
from private_calls.private_calls_check.find_function_def import FindFunctionDef


def _create_violations_msg(mod_name: str, violations: list[str]) -> list[str]:
    violations_msg = []
    for function_call in violations:
        violations_msg.append(
            f"Violation found @ {mod_name}: {function_call} is being called even though it's a private function not defined inside the module."
        )
    return violations_msg


def private_calls_check(file: Path):
    file_path_no_name = ".".join(file.parts[:-1])
    file_stem = file.stem
    mod_name = ".".join(
        filter(lambda part: len(part) > 0, [file_path_no_name, file_stem])
    )

    with suppress(OSError):  # in case module is empty.
        mod = importlib.import_module(mod_name)
        mod_src_code = parse(inspect.getsource(mod))

        function_definitions = FindFunctionDef()
        function_calls = FindCall()
        function_definitions.visit(mod_src_code)
        function_calls.visit(mod_src_code)

        functions_calls_n_defs = [
            fn_call for fn_call in function_calls.result if fn_call.startswith("_")
        ] + function_definitions.result

        function_definitions_set = set(function_definitions.result)
        functions_calls_n_defs_set = set(functions_calls_n_defs)

        calls_not_in_module = functions_calls_n_defs_set - function_definitions_set

        return calls_not_in_module


def main(*filenames):
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*")
    args = parser.parse_args(filenames)

    total_violations = []
    for filename in args.filenames:
        file = Path(filename)
        file_violations = private_calls_check(file)
        if len(file_violations) > 0:
            file_violations_msgs = _create_violations_msg(
                mod_name=str(file), violations=file_violations
            )
            total_violations += file_violations_msgs

    print(f"{len(total_violations)} violation(s) found.")
    if len(total_violations) > 0:
        raise Exception("\n".join(total_violations))


if __name__ == "__main__":
    main()
