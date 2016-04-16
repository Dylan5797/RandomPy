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

if _platform.system() != 'Windows':
    print('Invalid platform. Must be Windows.')
    input()
    _sys.exit()

try:
    import rand_sources
    import rand_utils
except:
    fn = _time.strftime('error-%y-%m-%d %H.%M.%S.txt')
    x = open(fn, 'w')
    x.write('Dependency failed. Please download the entire zip file and do not move any files, as this can cause this error message.\n')
    x.close()
    _os.startfile(fn)



def test(tests, tries, src, gui=False):
    t = []
    lu = _time.time()
    for x in range(0, tests):
        occ = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        tx = []
        for y in range(0, tries):
            num = rand_utils.proc_seed(src.get())
            tx.append(num)
            occ[int(num * 10.5)] += 1
            tm = rand_utils.meter((x * tries) + y + 1, tests * tries)
            if gui:
                if lu + 0.05 < _time.time():
                    print('\r' + tm, end='')
                    lu = _time.time()
        t.append((rand_utils.average(tx), abs(0.5 - rand_utils.average(tx)), occ, tx))
    print('\r' + rand_utils.meter(tests * tries - 1, tests * tries), end='')
    return t

def experiment(source, tests, tries, gui=False):
    res = test(tests, tries, source, gui)
    cp = ''
    obj = []
    cp = cp + "RandomPy Experiment Log\n"
    cp = cp + "RandomPy is Copyright (c) Dylan Beswick 2016. You may (re)distribute this log (or parts of it) noncommercially as long as this notice is kept in all copies of this log.\n"
    cp = cp + "-" * 80 + '\n'
    for x in range(0, tests):
        obj.append({'avg': res[x][0], 'dist_offset':res[x][1], 'occurances':','.join([str(x) for x in res[x][2]]), 'occ_dump':','.join([str(x) for x in res[x][3]])})
        cp = cp + ('#' * 40) + (' Test %s:' % (x + 1)) + ('#' * 40) + '\n'
        cp = cp + 'Average: ' + str(res[x][0]) + '\n'
        cp = cp + 'Average Distribution Offset: ' + str(res[x][1]) + '\n'
        cp = cp + 'Rounded Outcomes:' + '\n'
        for y in range(0, 11):
            cp = cp + str(y) + rand_utils.meter(res[x][2][y], tries, 100) + '\n'
        cp = cp + '\n\n'
    ts = rand_utils.timestamp()
    rand_utils.dump_lzma(obj, ts)
    rand_utils.dump_txt(cp, ts)
    if gui:
        print('\r' + rand_utils.meter(tests * tries, tests * tries))

def ui_main():
    print('RandomPy\nCopyright (c) Dylan Beswick 2016')
    dev = False
    local_tests = 10
    local_tries = 100000
    local_func = rand_sources.random_py
    while True:
        lss = input('Please enter a source class:\n')
        if lss == 'devMode':
            dev = True
            break
        try:
            local_func = getattr(rand_sources, lss)
            a = local_func.get()
        except:
            _trackback.print_exc()
            print('Error: the class is invalid does not exist.')
        else:
            break
    if dev:
        while True:
            q = input('RandPy> ')
            if q.lower() == 'quit':
                break
            try:
                exec(q)
            except:
                _traceback.print_exc()
    if type(local_func) == str:
        local_func = getattr(rand_sources, lss)
    print('Running tests...')
    _time.sleep(2)
    try:
        experiment(local_func, local_tests, local_tries, gui=True)
    except:
        _traceback.print_exc()
    input('\n\n## Tests Done. Press Return ##')


def user_interface():
    try:
        ui_main()
    except:
        error_text = """
"""

if __name__ == "__main__":
    user_interface()
