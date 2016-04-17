#!python3
import platform
import sys
import traceback
import os

errors = []
warns = []


print('RandomPy')
print('Copyright (c) Dylan Beswick 2016')
print('')

if int(''.join(platform.python_version_tuple()[0:2])) < 35:
    errors.append('Outdated python version. Expected at least 3.5')

if platform.system() != "Windows":
    errors.append('Unsupported operating system. Must be a windows environment')

if len(errors) > 0:
    [print('FATAL: ' + x) for x in errors]
    input()
    sys.exit()

path = os.path.dirname(os.path.realpath(__file__))

import importlib.util

def import_path(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    globals()[name] = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(globals()[name])
    return globals()[name]

srcs = ['rand_random', 'rand_utils', 'rand_sources']

for x in srcs:
    try:
        globals()[x] = import_path(x, path + '\\src\\' + x + '.py')
    except:
        errors.append('Failed to load "' + x + '"')




if 'rand_sources' in globals():
    for x in rand_sources.RAND_SOURCES:
        for y in x.packages:
            try:
                __import__(y)
            except:
                warns.append('Package "' + y + '" missing for source "' + x.name + '". Using this source may cause errors')


if not (platform.release() in ["7", "8", "8.1", "10"]):
    warns.append('Windows version is outdated. The program may be unstable')


if len(warns) > 0:
    [print('WARNING: ' + x) for x in warns]

if len(errors) > 0:
    [print('FATAL: ' + x) for x in errors]
    input()
    sys.exit()

input('\n\nPress return to begin\n')
os.startfile(path + '\\src\\rand_random.py')
