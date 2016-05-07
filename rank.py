#!python3
import platform
import sys
import traceback
import os
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


def find_best_source(exclusions=[]):
    avg_dist = []
    avg_diff = []

    for x in sorted(os.listdir(path + '\\logs')):
        if os.path.splitext(x)[1] == '.txt':
            ff = open(path + '\\logs\\' + x)
            cnt = ff.readlines()
            ff.close()
            dist_ds = True
            diff_ds = True
            for y in cnt:
                if ('overall absolute deviation' in y.lower()) and dist_ds and (not (x in exclusions)):
                    avg_dist.append([x, str(float(y[28:-1]) * 100)])
                    dist_ds = False
                if ('overall frequency distribution range' in y.lower()) and diff_ds and (not (x in exclusions)):
                    avg_diff.append([x, y[38:-2]])
                    diff_ds = False

    best_dist = [avg_dist[0][0], float(avg_dist[0][1])]
    best_diff = [avg_dist[0][0], float(avg_diff[0][1])]

    for x in avg_dist:
        if float(x[1]) < best_dist[1]:
            best_dist = [x[0], float(x[1])]

    for x in avg_diff:
        if float(x[1]) < best_diff[1]:
            best_diff = [x[0], float(x[1])]

    best_source = None

    if best_diff[0] == best_dist[0]:
        best_source = best_diff[0]
    else:
        for x in avg_diff:
            if best_dist[0] == x[0]:
                dist_ad = [best_dist[0], best_dist[1] + float(x[1])]
        for x in avg_dist:
            if best_diff[0] == x[0]:
                diff_ad = [best_diff[0], best_diff[1] + float(x[1])]
        if diff_ad[1] > dist_ad[1]:
            best_source = dist_ad[0]
        else:
            best_source = diff_ad[0]
    return best_source


def rank_sources():
    def recurse(num, exc=[]):
        s = find_best_source(exc)
        i = open(path + '\\logs\\' + s)
        li = i.readlines()
        i.close()
        if 'rank' in li[0].lower():
            li[0] = 'Rank: ' + str(num) + '\n'
        else:
            li.insert(0, 'Rank: ' + str(num) + '\n')
        i = open(path + '\\logs\\' + s, 'w')
        i.write(''.join(li))
        i.close()
        if s.startswith('['):
            nn = s
            for x in range(0, len(nn)):
                if nn[x] == ']':
                    nn = '[' + str(num) + nn[x:]
                    break
        else:
            nn = '[' + str(num) + '] ' + s
        os.rename(path + '\\logs\\' + s, path + '\\logs\\' + nn)
        if num != len([x for x in os.listdir(path + '\\logs') if os.path.splitext(x)[1] == '.txt']):
            recurse(num + 1, exc + [nn])
    recurse(1)


if __name__ == "__main__":
    print('Ranking logs...', end='')
    try:
        rank_sources()
    except:
        traceback.print_exc()
        print('\n\nError: please make sure logs are not corrupt.')
    else:
        print('Done')
    input()
