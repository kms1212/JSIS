from colorama import init, Fore, Back, Style
import tqdm
import os
import sys
import argparse
from pyfiglet import Figlet

action_description = ""
action_params = [
    { 'params': ['--interactive'],           'action': 'store_true', 'help': 'Run in interactive mode. (default=true)', 'default': True },

    { 'params': ['--server-domain'],         'action': 'store',      'help': 'Server domain name.' },
    { 'params': ['--django-secret-key'],     'action': 'store',      'help': 'Django secret key. If not specified, a random key will be generated. Generate key from https://djecrety.ir/ and paste it here.', 'default': None },
    { 'params': ['--remote-available'],      'action': 'store',      'help': 'Is remote host reachable with SSH connection? (default=true)', 'default': True },
    { 'params': ['--remote-host'],           'action': 'store',      'help': 'Remote host name or IP address.' },
    { 'params': ['--remote-user'],           'action': 'store',      'help': 'Remote user name.' },
    { 'params': ['--remote-port'],           'action': 'store',      'help': 'Remote port number.' },
    { 'params': ['--migration-path-host'],   'action': 'store',      'help': 'Path to the directory where migration files will be stored on the host.' },
    { 'params': ['--migration-mount-point'], 'action': 'store',      'help': 'Path to the directory where migration files will be mounted on the container.' },
    { 'params': ['--static-path-host'],      'action': 'store',      'help': 'Path to the directory where static files will be stored on the host.' },
    { 'params': ['--static-mount-point'],    'action': 'store',      'help': 'Path to the directory where static files will be mounted on the container.' },
    { 'params': ['--media-path-host'],       'action': 'store',      'help': 'Path to the directory where media files will be stored on the host.' },
    { 'params': ['--media-mount-point'],     'action': 'store',      'help': 'Path to the directory where media files will be mounted on the container.' },
    { 'params': ['--database-name'],         'action': 'store',      'help': 'Database name. (default=jsis)', 'default': 'jsis' },
    { 'params': ['--database-user'],         'action': 'store',      'help': 'Database user name. (default=jsisuser)', 'default': 'jsisuser' },
    { 'params': ['--database-password'],     'action': 'store',      'help': 'Database user password.' },
    { 'params': ['--email-host'],            'action': 'store',      'help': 'Email host name or IP address.' },
    { 'params': ['--email-port'],            'action': 'store',      'help': 'Email port number.' },
    { 'params': ['--email-user'],            'action': 'store',      'help': 'Email user name.' },
    { 'params': ['--email-password'],        'action': 'store',      'help': 'Email user password.' },
    { 'params': ['--sentry-dsn'],            'action': 'store',      'help': 'Sentry DSN.' },

    { 'params': ['--dry-run'],               'action': 'store_true', 'help': 'Run a simulation of the script.' },
]

class Worker():
    
    def set_init_options(args):
        if not args.simple:
            init(autoreset=True)
            f = Figlet(font='univers')
            print(Fore.GREEN + f.renderText('JSIS') + Fore.RESET)

        if args.interactive:
            print('Server domain name')
            print('(e.g. https://jsis.example.com)')
            args.server_domain = input(': ')

            print('Django secret key')
            print('(If not specified, a random key will be generated.')
            print(' Generate key from https://djecrety.ir/ and paste it here.)')
            args.django_secret_key = input(': ')

            print('Is remote host reachable with SSH connection? [true]')
            args.remote_available = input(': ')

            print('Remote host name or IP address')
            args.remote_host = input(': ')

            print('Remote user name')
            args.remote_user = input(': ')

            print('Remote port number')
            args.remote_port = input(': ')

            print('Path to the directory where migration files will be stored on the host')
            args.migration_path_host = input(': ')

            print('Path to the directory where migration files will be mounted on the container')
            args.migration_mount_point = input(': ')

            print('Path to the directory where static files will be stored on the host')
            args.static_path_host = input(': ')

            print('Path to the directory where static files will be mounted on the container')
            args.static_mount_point = input(': ')

            print('Path to the directory where media files will be stored on the host')
            args.media_path_host = input(': ')

            print('Path to the directory where media files will be mounted on the container')
            args.media_mount_point = input(': ')

            print('Database name [jsis]')
            args.database_name = input(': ')

            print('Database user name [jsisuser]')
            args.database_user = input(': ')

            print('Database user password')
            args.database_password = input(': ')

            print('Email host name or IP address')
            args.email_host = input(': ')

            print('Email port number')
            args.email_port = input(': ')

            print('Email user name')
            args.email_user = input(': ')

            print('Email user password')
            args.email_password = input(': ')

            print('Sentry DSN')
            args.sentry_dsn = input(': ')

            print('Summary')
            print('======================================')
            print('Server domain name: ' + args.server_domain)
            print('Django secret key: ' + args.django_secret_key)
            print('Is remote host reachable with SSH connection? ' + args.remote_available)
            print('Remote host name or IP address: ' + args.remote_host)
            print('Remote user name: ' + args.remote_user)
            print('Remote port number: ' + args.remote_port)
            print('Migration directory path: ' + args.migration_path_host)
            print('Docker Container migration directory mount point: ' + args.migration_mount_point)
            print('Static files directory path: ' + args.static_path_host)
            print('Docker Container static files directory mount point: ' + args.static_mount_point)
            print('Media files directory path: ' + args.media_path_host)
            print('Docker Container media files directory mount point: ' + args.media_mount_point)
            print('Database name: ' + args.database_name)
            print('Database user name: ' + args.database_user)
            print('Database user password: ' + args.database_password)
            print('Email host name or IP address: ' + args.email_host)
            print('Email port number: ' + args.email_port)
            print('Email user name: ' + args.email_user)
            print('Email user password: ' + args.email_password)
            print('Sentry DSN: ' + args.sentry_dsn)
            print('======================================')

            while True:
                print('Menu: [1] Run setup, [2] Generate Report, [3] Exit')
                menu = input(': ')
                if menu == '1':
                    break
                elif menu == '2':
                    break
                elif menu == '3':
                    sys.exit()
                else:
                    print('Invalid input')
