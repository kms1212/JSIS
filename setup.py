from colorama import init, Fore, Back, Style
import tqdm
import os
import sys
import argparse
from pyfiglet import Figlet

import initializer

version = 'JSIS Server Initializer v0.0.1'


if __name__ == '__main__':
    print(initializer.get_help_string(None))

    # Parse command line options




    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument('-V', '--version',         action='version',    version=version)

    parser.add_argument('setup',                   action='store_true', help='Run setup.')
    parser.add_argument('report',                  action='store_true', help='Generate report.')
    parser.add_argument('remote-setup',            action='store_true', help='Run remote setup.')
    parser.add_argument('remote-clean',            action='store_true', help='Run remote clean.')
    parser.add_argument('remote-restart',          action='store_true', help='Run remote restart.')

    parser.add_argument('-v', '--verbose',         action='store_true', help='Run in verbose mode.')
    parser.add_argument('--simple',                action='store',      help='Run without fancy output.', default=False)
    parser.add_argument('-q', '--quiet',           action='store_true', help='Do not print anything.')

    parser.add_argument('--interactive',           action='store_true', help='Run in interactive mode. (default=true)', default=True)

    parser.add_argument('--server-domain',         action='store',      help='Server domain name.')
    parser.add_argument('--django-secret-key',     action='store',      help='Django secret key. If not specified, a random key will be generated. Generate key from https://djecrety.ir/ and paste it here.', default=None)
    parser.add_argument('--remote-available',      action='store',      help='Is remote host reachable with SSH connection? (default=true)', default=True)
    parser.add_argument('--remote-host',           action='store',      help='Remote host name or IP address.')
    parser.add_argument('--remote-user',           action='store',      help='Remote user name.')
    parser.add_argument('--remote-port',           action='store',      help='Remote port number.')
    parser.add_argument('--migration-path-host',   action='store',      help='Path to the directory where migration files will be stored on the host.')
    parser.add_argument('--migration-mount-point', action='store',      help='Path to the directory where migration files will be mounted on the container.')
    parser.add_argument('--static-path-host',      action='store',      help='Path to the directory where static files will be stored on the host.')
    parser.add_argument('--static-mount-point',    action='store',      help='Path to the directory where static files will be mounted on the container.')
    parser.add_argument('--media-path-host',       action='store',      help='Path to the directory where media files will be stored on the host.')
    parser.add_argument('--media-mount-point',     action='store',      help='Path to the directory where media files will be mounted on the container.')
    parser.add_argument('--database-name',         action='store',      help='Database name. (default=jsis)', default='jsis')
    parser.add_argument('--database-user',         action='store',      help='Database user name. (default=jsisuser)', default='jsisuser')
    parser.add_argument('--database-password',     action='store',      help='Database user password.')
    parser.add_argument('--email-host',            action='store',      help='Email host name or IP address.')
    parser.add_argument('--email-port',            action='store',      help='Email port number.')
    parser.add_argument('--email-user',            action='store',      help='Email user name.')
    parser.add_argument('--email-password',        action='store',      help='Email user password.')
    parser.add_argument('--sentry-dsn',            action='store',      help='Sentry DSN.')

    parser.add_argument('--dry-run',               action='store_true', help='Run a simulation of the script.')
    args = parser.parse_args()

