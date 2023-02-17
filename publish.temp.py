import time
import subprocess
import os
import argparse
import io
import selectors
import shutil

from yaspin import yaspin

scripts = [
    ("frontend_lint", "frontend/scripts/lint.sh"),
    ("frontend_build", "frontend/scripts/build.sh"),

    ("backend_lint", "backend/scripts/lint.sh"),
    ("backend_test", "backend/scripts/test.sh"),

    ("publish", "scripts/publish.sh"),
]

def run_shell_script(script, write_func, options):
    """
    script: shell script path
    write_func: function to write output
    options: verbose[True, False]
    """
    process = subprocess.Popen(script, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    buf = io.StringIO()

    def handle_output(stream, _mask):
        line = stream.readline()
        buf.write(line.decode("utf-8"))
        if options['verbose']:
            write_func(line.decode("utf-8").rstrip())

    selector = selectors.DefaultSelector()
    selector.register(process.stdout, selectors.EVENT_READ, handle_output)

    while process.poll() is None:
        events = selector.select()
        for key, mask in events:
            callback = key.data
            callback(key.fileobj, mask)

    returncode = process.wait()
    selector.close()

    return returncode, buf.getvalue()


def run_shell_scripts(script_nm, script, verbose):
    with yaspin(text="Running shell script " + script, color="cyan", timer=True) as spin:
        returncode, output = run_shell_script(script, spin.write, {"verbose": verbose})

        if returncode != 0:
            spin.fail("✘")
            print(output)
        else:
            spin.ok("✔")

        with open("reports/template/publish-report/data/" + script_nm + ".txt", "w", encoding="utf8") as f:
            f.write(output)

        return returncode


def main(args):
    if os.path.exists("reports/template/publish-report/data"):
        shutil.rmtree("reports/template/publish-report/data")

    os.mkdir("reports/template/publish-report/data")

    for script in scripts:
        if len(args.scripts) > 0 and script[0] not in args.scripts:
            continue

        return_code = run_shell_scripts(script[0], script[1], args.verbose)
        if return_code != 0:
            print("Error running script " + script[0] + ". Exited with status code " + str(return_code) + ".")
            exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument("scripts", nargs="*", help="list of shell scripts to run", default=[])
    args = parser.parse_args()

    main(args)
