#!python3

"""
Copyright (c) 2016 Dylan Beswick
The MIT License (MIT)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files
(the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge,
publish, distribute, sublicense, and/or sell  copies of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""


import traceback as _traceback
import os as _os
import sys as _sys
import time as _time
import platform as _platform
import math as _math


def basic_error_report(err):
    fn = _time.strftime('error-%y-%m-%d %H.%M.%S.txt')
    x = open(fn, 'w')
    x.write(err)
    x.close()
    if __name__ == "__main__":
        _os.startfile(fn)
    _sys.exit()   



try:
    import importlib.util
except:
    basic_error_report('Failed to import importlib.util, probably because python version is not 3.5')

try:
    path = _os.path.dirname(_os.path.realpath(__file__))
except:
    basic_error_report('Could not locate self')

def import_path(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    globals()[name] = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(globals()[name])
    return globals()[name]


global G_SETTINGS
G_SETTINGS = {'logging.dump_lzma':'false'}

args = _sys.argv[1:]

try:
    assert int(len(args) % 2) == 0
except:
    basic_error_report('Invalid Settings args input')

try:
    for x in range(0, len(args)):
        if int(x % 2) == 0:
            G_SETTINGS[args[x]] = args[x+1]
except:
    basic_error_report('Error parsing args\n\n' + _traceback.format_exc())

try:
    import_path('rand_sources', path + '\\rand_sources.py')
    import_path('rand_utils', path + '\\rand_utils.py')
except:
    basic_error_report('A Dependency failed. Please download the entire zip file and do not move any files, as this can cause this error message.\n\n' + _traceback.format_exc())

def test(tests, alogrithm, tries, src, gui=False):
    t = []
    lu = _time.time()
    for x in range(0, tests):
        occ = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        tx = []
        for y in range(0, tries):
            num = alogrithm(src.get())
            tx.append(num)
            occ[int(num * 10)] += 1
            tm = rand_utils.meter((x * tries) + y + 1, tests * tries)
            if gui:
                if lu + 0.05 < _time.time():
                    print('\r' + tm, end='')
                    lu = _time.time()
        t.append((rand_utils.average(tx), abs(0.5 - rand_utils.average(tx)), occ[:10], tx))
    print('\r' + rand_utils.meter(tests * tries - 1, tests * tries), end='')
    return t

def experiment(source, algorithm, tests, tries, gui=False):
    source.init()
    res = test(tests, algorithm, tries, source, gui)
    source.dels()
    cp = ''
    obj = {'source':source.name, 'algorithm':algorithm.__name__, 'tests':tests * tries, 'divisions':tests, 'division_tries':tries, 'global_greatest_outcome_difference':rand_utils.average([((((max(res[x][2]) / (tries)) - (min(res[x][2]) / (tries))) * 100)) for x in range(0, tests)]), 'global_average':rand_utils.average([res[x][0] for x in range(0, tests)]), 'global_dist_offset':rand_utils.average([res[x][1] for x in range(0, tests)]), 'sets':[]}
    cp = cp + "RandomPy Experiment Log\n"
    cp = cp + "RandomPy is Copyright (c) Dylan Beswick 2016. You may (re)distribute this log (or parts of it) noncommercially as long as this notice is kept in all copies of this log.\n"
    cp = cp + "-" * 80 + '\n'
    cp = cp + "Source: " + source.name + '\n'
    cp = cp + "Algorithm: " + algorithm.__name__ + '\n'
    cp = cp + "Tests: " + str(tests * tries) + '\n'
    cp = cp + "Divisions: " + str(tests) + '\n'
    cp = cp + "Tries per Division: " + str(tries) + '\n'
    cp = cp + "Overall Distribution Offset: " + str(rand_utils.average([res[x][1] for x in range(0, tests)])) + '\n'
    cp = cp + 'Overall Greatest Outcome Difference: ' + str(rand_utils.average([((((max(res[x][2]) / (tries)) - (min(res[x][2]) / (tries))) * 100)) for x in range(0, tests)])) + '%\n'
    cp = cp + 'Average: ' + str(rand_utils.average([res[x][0] for x in range(0, tests)])) + '\n'
    for x in range(0, tests):
        obj['sets'].append({'avg': res[x][0], 'dist_offset':res[x][1], 'occurances':[x for x in res[x][2]], 'occ_dump':res[x][3], 'greatest_outcome_difference':(((max(res[x][2]) / (tries)) - (min(res[x][2]) / (tries))) * 100)})
        cp = cp + ('#' * 40) + (' Test %s: ' % (x + 1)) + ('#' * 40) + '\n'
        cp = cp + 'Average: ' + str(res[x][0]) + '\n'
        cp = cp + 'Average Distribution Offset: ' + str(res[x][1]) + '\n'
        cp = cp + 'Greatest Outcome Difference: ' + str((((max(res[x][2]) / (tries)) - (min(res[x][2]) / (tries))) * 100)) + '%\n'
        cp = cp + 'Outcomes:' + '\n'
        for y in range(0, 10):
            cp = cp + str(y).rjust(2, '0') + ' ' + rand_utils.meter(res[x][2][y], tries, 50, round) + '\n'
        cp = cp + '\n\n'
    ts = rand_utils.timestamp()
    if G_SETTINGS['logging.dump_lzma'].lower() == 'true':
        rand_utils.dump_lzma(obj, ts)
    fn = rand_utils.dump_txt(cp, ts)
    if gui:
        print('\r' + rand_utils.meter(tests * tries, tests * tries))
    return (cp, fn)

def ui_main():
    print('RandomPy\nCopyright (c) Dylan Beswick 2016')
    dev = False
    settings = {'tests':10, 'tries':100000, 'func':rand_sources.random_py, 'algorithm':rand_utils.algorithm_default}
    while True:
        lss = input('Please enter a source class:\n')
        if lss == 'custom':
            dev = True
            break
        try:
            settings['func'] = getattr(rand_sources, lss)
            if (type(settings['func']) == rand_sources.Source) or (type(settings['func']) == rand_sources.InitializingSource):
                break
        except:
            print('Error: the class is invalid does not exist.')
    while True:
        lss = input('Please enter an algorithm function name (blank for default):\n')
        if lss == 'custom':
            dev = True
            break
        if lss.strip() == '':
            break
        try:
            settings['algorithm'] = getattr(rand_utils, lss)
            assert type(settings['algorithm'](42)) == float
            break
        except:
            print('Error: the function is invalid does not exist.')
    if dev:
        while True:
            q = input('RandPy> ')
            if q.lower() == 'quit':
                break
            try:
                settings[q.split()[0]] = ' '.join(q.split()[1:])
            except:
                _traceback.print_exc()
    if type(settings['func']) == str:
        settings['func'] = getattr(rand_sources, settings['func'])
    if type(settings['algorithm']) == str:
        settings['algorithm'] = getattr(rand_utils, settings['algorithm'])
    print('Running tests...')
    _time.sleep(2)
    txt, fn = experiment(settings['func'], settings['algorithm'], int(settings['tests']), int(settings['tries']), gui=True)
    while True:
        f = input('Print results? [Y/N]: ').lower()[0]
        if f == 'y':
            pr = True
            break
        elif f == 'n':
            pr = False
            break
    if pr:
        for x in txt.split('\n'):
            print(x)
    input('\n\n## Press Return ##\n')
    _os.startfile(fn)


def user_interface():
    try:
        ui_main()
    except KeyboardInterrupt:
        pass
    except BaseException as e:
        tm = _time.localtime()
        error_text = "RandomPy Crash Report\n"
        error_text += ['Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun'][tm.tm_wday] + ' '
        error_text += ['January', 'Febuary', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'][tm.tm_mon - 1] + ' '
        error_text += str(tm.tm_mday) + ', '
        error_text += _time.strftime('%T\n')
        error_text += "Report bugs at https://github.com/Dylan5797/RandomPy/issues\n"
        error_text += "-" * 60 + "\n" * 2
        error_text += e.__class__.__name__ + ": " + str(e) + '\n\n\n'
        error_text += ''.join(_traceback.format_exception(type(e), e, e.__traceback__))
        fn = _os.path.dirname(_os.path.dirname(_os.path.realpath(__file__))) + '\\crash-logs\\' + _time.strftime('crash-%y-%m-%d %H.%M.%S.txt')
        fl = open(fn, 'w')
        fl.write(error_text)
        fl.close()
        _os.startfile(fn)

        
if __name__ == "__main__":
    user_interface()
