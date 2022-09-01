# -*- coding: utf-8 -*-
'''Unreal bootstrapper

Currently only really supporting Windows, because of non-generic paths

Usage: Place file in either 
    <Unreal project folder>/Content/Python or 
    <User documents folder>/UnrealEngine/Python

File in the latter location will take precedence, allowing developers to bootstrap
a different repository than end-users.

If you want to auto-populate various UI elements with a default project
see the `os.environ` calls below.
'''

import os
import sys
import traceback

# Developer vs. production paths
DEVELOPERPATHS = [r'C:\GIT\ue5-error-example\python', r'D:\GIT\ue5-error-example\python']
LIB_STUB = 'lib'

# Don't touch this
BOOTLOCATION_MYDOCS = r'{}\Documents\UnrealEngine\Python'.format(os.getenv('USERPROFILE'))
CURRENT_SCRIPT_LOCATION = os.path.realpath(__file__)


def addPaths(modPath):
    '''Adds paths to sys.path if required'''

    libPath = r'{}\{}'.format(modPath, LIB_STUB)
    for path in [modPath, libPath]:
        if not path in sys.path:
            print('Adding path {} to sys.path'.format(path))
            sys.path.insert(0, path)
        else:
            print('Path {} is already in sys.path, taking no action'.format(path))


def execute():
    '''Main entry point'''

    print('Unreal bootstrapper is loading from {}'.format(CURRENT_SCRIPT_LOCATION))
    targetPaths = []

    if 'PROXI_UNREAL_HASLOADED' in os.environ:
        print('Bootstrapper has already been executed. Aborting.')
        return

    if BOOTLOCATION_MYDOCS.lower() in CURRENT_SCRIPT_LOCATION.lower():
        print('Using developer paths')
        targetPaths = DEVELOPERPATHS

    target = None
    for path in targetPaths:
        print('Testing {}...'.format(path))
        if os.path.exists(path):
            print('Found!')
            target = path
            break

        print('Not found')

    if not target:
        print('None of the desired paths were found -- this will not go well. Adding the first one nonetheless')
        target = targetPaths[0]

    addPaths(target)
    
    print('Executing startup script')
    try:
        import proxi.startup
        os.environ['PROXI_UNREAL_HASLOADED'] = 'True'
    except Exception as e:
        import unreal
        unreal.log_error('Error initializing PROXi Python module: {}'.format(e))
        stack = traceback.format_exc()
        unreal.log_error('## Stacktrace ##\n{}'.format(stack))
        unreal.EditorDialog.show_message(
            title='PROXi Pipeline Error',
            message='Unable to initialize PROXi Pipeline integration.\n\nInstall path(s) not found:\n{}\n\nUnreal says:\n{}'.format('\n'.join(targetPaths), e),
            message_type=unreal.AppMsgType.OK,
            default_value=unreal.AppReturnType.NO
        )

    print('Unreal bootstrapper has finished')


# Simply call the `execute` entry point.
# TODO: context verification?
execute()