import sys
import importlib
import os
import textwrap


def get_help_string(action_name):
    termwidth = os.get_terminal_size().columns

    if action_name == None:
        help_string_base = 'Usage: python3 %s %s [options]\n' % (sys.argv[0], '[action]')
    else:
        help_string_base = 'Usage: python3 %s %s [options]\n' % (sys.argv[0], action_name)

    # Get action description
    if action_name == None:
        # No action specified, show help for all actions
        actions = ['setup', 'report']
        actions_width = len(max(actions, key=len))  # Get longest action name in list

        help_string_base += 'Actions:\n'
        for action in actions:
            action_module = importlib.import_module('initializer.' + action)
            
            help_string_base += '    %s %s\n' % (action.ljust(actions_width, ' '), action_module.action_description)

        help_string_base += 'Options:\n'
        help_string_base += '    Global:\n'
        help_string_base += '        -h, --help      Show this help message and exit\n'
        help_string_base += '        -V, --version   Show program\'s version number and exit\n'

        for action in actions:
            action_module = importlib.import_module('initializer.' + action)

            help_string_base += '    %s:\n' % action
            if len(action_module.action_params) == 0:
                help_string_base += '        No options available\n'
                continue
            else:
                params_width = len(max([', '.join(param['params']) for param in action_module.action_params], key=len))  # Get longest param name in list

                for param in action_module.action_params:
                    help_string_base += '        %s ' % (', '.join(param['params']).ljust(params_width, ' '))
                    help_string_base += textwrap.fill(param['help'], termwidth - params_width - 8, initial_indent='', subsequent_indent=' ' * (params_width + 9)) + '\n'
        
        return help_string_base

    

