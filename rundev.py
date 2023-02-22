import subprocess
import io
import threading
import queue
from colorama import Fore, init
import signal


class ProgramRunner:
    def __init__(self, name, command, color=Fore.WHITE):
        self.name = name
        self.command = command
        self.buffer = io.StringIO()
        self.logqueue = queue.Queue()
        self.color = color

        self.process = None
        self.thread = None
        self.exitcode = None

    def run(self):
        self.thread = threading.Thread(target=self.runner)
        self.thread.start()
        print(self.color + self.name + ': ' + 'Process started' + Fore.RESET)

    def stop(self):
        if self.process:
            self.process.terminate()
            self.process.wait(1000)
            self.process.kill()
            self.exitcode = self.process.returncode

            if self.thread:
                self.thread.join(1000)

            print(self.color + self.name + ': ' + 'Process terminated with exit code ' + str(self.exitcode) + Fore.RESET)

    def runner(self):
        self.process = subprocess.Popen(self.command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        with self.process.stdout:
            for line in iter(self.process.stdout.readline, b''):
                print(self.color + self.name + ': ' + line.decode("utf-8") + Fore.RESET, end='')

    def isrunning(self):
        return self.process and self.process.poll() is None

def signal_handler(_sig, _frame):
    for runner in runners:
        runner.stop()

runners = [
    ProgramRunner('django_server', './backend/devscripts/rundevserver.sh', Fore.GREEN),
    ProgramRunner('tailwindcss', 'cd frontend/src && npm run css', Fore.CYAN),
    ProgramRunner('vite', 'cd frontend/src && npm run dev', Fore.MAGENTA),
]

if __name__ == '__main__':
    init()
    for runner in runners:
        runner.run()

    signal.signal(signal.SIGINT, signal_handler)
