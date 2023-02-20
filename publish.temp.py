import subprocess
import os
import argparse
import shutil
import io

from yaspin import yaspin

scripts = [  # pylint: disable=invalid-name
    ("frontend_lint", "frontend/scripts/lint.sh"),
    ("frontend_build", "frontend/scripts/build.sh"),

    ("backend_lint", "backend/scripts/lint.sh"),
    ("backend_test", "backend/scripts/test.sh"),

    ("publish", "scripts/publish.sh"),
    ("create_report", "reports/template/scripts/latex-publish-report.sh")
]

def run_shell_script(script, write_func, options):
    """
    script: shell script path
    write_func: function to write output
    options: verbose[True, False]
    """
    process = subprocess.Popen(script, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    strbuf = io.StringIO()

    with process.stdout:
        for line in iter(process.stdout.readline, b''):
            if options['verbose']:
                write_func(line.decode("utf-8"))
            strbuf.write(line.decode("utf-8"))

    returncode = process.wait()

    return returncode, strbuf.getvalue()


def run_shell_scripts(script_nm, script, verbose):
    with yaspin(text="Running shell script " + script, color="cyan", timer=True) as spin:
        returncode, output = run_shell_script(script, spin.write, {"verbose": verbose})

        if returncode != 0:
            spin.fail("✘")
            print(output)
        else:
            spin.ok("✔")

        if script_nm != "create_report":
            with open("reports/template/publish-report/data/" + script_nm + ".txt",
                      "w",
                      encoding="utf8") as file:
                file.write(output)

        return returncode


def main(args):
    if os.path.exists("reports/template/publish-report/data"):
        shutil.rmtree("reports/template/publish-report/data")

    os.mkdir("reports/template/publish-report/data")

    for script in scripts:
        if args.scripts and script[0] not in args.scripts:
            continue

        return_code = run_shell_scripts(script[0], script[1], args.verbose)
        if return_code != 0:
            print("Error running script %s. Exited with status code %d." % (script[0], return_code))
            exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=True)  # pylint: disable=invalid-name
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument("scripts", nargs="*", help="list of shell scripts to run", default=[])
    args = parser.parse_args()  # pylint: disable=invalid-name

    main(args)
