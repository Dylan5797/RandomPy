#!python3
import platform
import sys
import traceback
import os
import lzma
import json
import subprocess

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

srcs = ['rand_random', 'rand_utils', 'rand_sources', 'ini']

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

srcs = []
print('Loading...', end='')

for x in sorted(os.listdir(path + '\\logs')):
    print('\rLoading... Discovered ' + str(len(srcs)) + ' datasets...', end='')
    if os.path.splitext(x)[1] == '.lzma':
        ff = open(path + '\\logs\\' + x, 'rb')
        srcs.append(json.loads(lzma.decompress(ff.read()).decode()))
        ff.close()

print('\rLoading... Discovered ' + str(len(srcs)) + ' datasets... Done')

if len(srcs) == 0:
    print('Error: No datasets to extract. Make sure LZMA dumping is enabled.')
    input()
    sys.exit()

print('Generating table...')
count = 0

table = [[]]
most = 0
most_sets = 0
for x in srcs:
    if len(x['sets']) > most_sets:
        most_sets = len(x['sets'])

while True:
    try:
        amt = int(input('%s sets found. Enter amount to be included: ' % str(most_sets)))
        assert amt > 0
        break
    except:
        print('Invalid number.')

for x in srcs:
    if len(x['sets'][0]['occ_dump']) * len(x['sets'][:amt]) > most:
        most = len(x['sets'][0]['occ_dump']) * len(x['sets'][:amt])

for x in range(0, most):
    table.append([])
    
for x in srcs:
    print('\rExtracting %s of %s...' % (str(count), str(len(srcs))), end='')
    table[0].append(x['source'].lower() + '.' + x['algorithm'].lower())
    include = []
    for y in x['sets'][:amt]:
        include.extend(y['occ_dump'])
    for y in range(0, len(include)):
        table[y + 1].append(include[y])
    count += 1
print('\rExtracting %s of %s...' % (str(count), str(len(srcs))))
print('Compiling...')
rand_utils.dump_csv('\n'.join([','.join([str(z) for z in y]) for y in table]))
