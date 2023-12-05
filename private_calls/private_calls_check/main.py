import argparse
import importlib
import inspect
import os
from ast import parse
from contextlib import suppress

from find_call import FindCall
from find_function_def import FindFunctionDef


def private_calls_check(folders: list[str]):
    errors = []
    for folder in folders:
        for dirpath, _, filenames in os.walk(folder):
            filenames_py = (
                filename for filename in filenames if filename.endswith(".py")
            )
            for filename in filenames_py:
                filename_no_ext = filename.split(".")[0]
                dirpath_with_dot = dirpath.replace("/", ".")

                modname = f"{dirpath_with_dot}.{filename_no_ext}"
                with suppress(OSError):  # in case module is empty.
                    mod = importlib.import_module(modname)
                    mod_src_code = parse(inspect.getsource(mod))

                    function_definitions = FindFunctionDef()
                    function_calls = FindCall()
                    function_definitions.visit(mod_src_code)
                    function_calls.visit(mod_src_code)

                    functions_calls_n_defs = (
                        function_calls.result + function_definitions.result
                    )
                    function_definitions_set = set(function_definitions.result)
                    functions_calls_n_defs_set = set(functions_calls_n_defs)
                    calls_not_in_module = (
                        functions_calls_n_defs_set - function_definitions_set
                    )
                    if len(calls_not_in_module) > 0:
                        for i, call in enumerate(calls_not_in_module):
                            if call.startswith("_"):
                                errors.append(
                                    (modname, call, function_calls.linenos[i])
                                )
    if len(errors) > 0:
        err_msg = []
        for i, modname, function_call, lineno in enumerate(errors):
            err_msg.append(
                f"{i}. {modname} is calling {function_call} at line {lineno}, a private function that doesn't belong to it."
            )

        raise Exception("\n".join(err_msg))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("folders", nargs="*")
    args = parser.parse_args()

    private_calls_check(args.folders)


if __name__ == "__main__":
    main()
