import time
import subprocess
import os
import argparse

from yaspin import yaspin

scripts = [
    ("frontend_lint", "frontend/scripts/lint.sh"),
    ("frontend_build", "frontend/scripts/build.sh"),

    ("backend_lint", "backend/scripts/lint.sh"),
    ("backend_test", "backend/scripts/test.sh"),

    ("publish", "scripts/publish.sh"),
]

def run_shell_scripts(script, verbose):
    with yaspin(text="Running shell script " + script, color="cyan", timer=True) as spin:
        process = subprocess.Popen([script], shell=True, stdout=subprocess.PIPE)

        if verbose:
            with process.stdout:
                for line in iter(process.stdout.readline, b''):
                    spin.write(line.decode("utf-8").strip())

        process.wait()

        if process.returncode != 0:
            spin.fail("✘")
        else:
            spin.ok("✔")
        return process.returncode


def run(args):
    for script in scripts:
        if len(args.scripts) > 0 and script[0] not in args.scripts:
            continue

        return_code = run_shell_scripts(script[1], args.verbose)
        if return_code != 0:
            print("Error running script " + script[0] + ". Exited with status code " + str(return_code) + ".")
            exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument("scripts", nargs="*", help="list of shell scripts to run", default=[])
    args = parser.parse_args()

    run(args)
