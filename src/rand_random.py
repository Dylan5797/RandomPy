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


try:
    import_path('rand_sources', path + '\\rand_sources.py')
    import_path('rand_utils', path + '\\rand_utils.py')
except:
    basic_error_report('A Dependency failed. Please download the entire zip file and do not move any files, as this can cause this error message.\n\n' + _traceback.format_exc())

def test(tests, tries, src, gui=False):
    t = []
    lu = _time.time()
    for x in range(0, tests):
        occ = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        tx = []
        for y in range(0, tries):
            num = rand_utils.proc_seed_md5(src.get())
            tx.append(num)
            occ[int(num * 10.49999999999999999)] += 1
            tm = rand_utils.meter((x * tries) + y + 1, tests * tries)
            if gui:
                if lu + 0.05 < _time.time():
                    print('\r' + tm, end='')
                    lu = _time.time()
        t.append((rand_utils.average(tx), abs(0.5 - rand_utils.average(tx)), occ, tx))
    print('\r' + rand_utils.meter(tests * tries - 1, tests * tries), end='')
    return t

def experiment(source, tests, tries, gui=False):
    source.init()
    res = test(tests, tries, source, gui)
    source.dels()
    cp = ''
    obj = []
    cp = cp + "RandomPy Experiment Log\n"
    cp = cp + "RandomPy is Copyright (c) Dylan Beswick 2016. You may (re)distribute this log (or parts of it) noncommercially as long as this notice is kept in all copies of this log.\n"
    cp = cp + "-" * 80 + '\n'
    cp = cp + "Source: " + source.name + '\n'
    cp = cp + "Overall Distribution Offset: " + str(rand_utils.average([res[x][1] for x in range(0, tests)])) + '\n'
    for x in range(0, tests):
        obj.append({'avg': res[x][0], 'dist_offset':res[x][1], 'occurances':','.join([str(x) for x in res[x][2]]), 'occ_dump':','.join([str(x) for x in res[x][3]])})
        cp = cp + ('#' * 40) + (' Test %s: ' % (x + 1)) + ('#' * 40) + '\n'
        cp = cp + 'Average: ' + str(res[x][0]) + '\n'
        cp = cp + 'Average Distribution Offset: ' + str(res[x][1]) + '\n'
        cp = cp + 'Rounded Outcomes:' + '\n'
        for y in range(0, 11):
            cp = cp + str(y).rjust(2, '0') + ' ' + rand_utils.meter(res[x][2][y], tries, 100) + '\n'
        cp = cp + '\n\n'
    ts = rand_utils.timestamp()
    rand_utils.dump_lzma(obj, ts)
    rand_utils.dump_txt(cp, ts)
    if gui:
        print('\r' + rand_utils.meter(tests * tries, tests * tries))

def ui_main():
    print('RandomPy\nCopyright (c) Dylan Beswick 2016')
    dev = False
    settings = {'local_tests':10, 'local_tries':100000, 'local_func':rand_sources.random_py}
    while True:
        lss = input('Please enter a source class:\n')
        if lss == 'devMode':
            dev = True
            break
        try:
            settings['local_func'] = getattr(rand_sources, lss)
            if (type(settings['local_func']) == rand_sources.Source) or (type(settings['local_func']) == rand_sources.InitializingSource):
                break
        except:
            print('Error: the class is invalid does not exist.')
    if dev:
        while True:
            q = input('RandPy> ')
            if q.lower() == 'quit':
                break
            try:
                settings['local_' + q.split()[0]] = ' '.join(q.split()[1:])
            except:
                _traceback.print_exc()
    if type(settings['local_func']) == str:
        settings['local_func'] = getattr(rand_sources, settings['local_func'])
    print('Running tests...')
    _time.sleep(2)
    experiment(settings['local_func'], int(settings['local_tests']), int(settings['local_tries']), gui=True)
    input('\n\n## Tests Done. Press Return ##')


def user_interface():
    try:
        ui_main()
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
