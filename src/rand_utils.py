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


import math as _math
import os as _os
import hashlib as _hashlib
import lzma as _lzma
import json as _json
import time as _time

parent_dir = _os.path.dirname(_os.path.dirname(_os.path.realpath(__file__)))

if not _os.path.isdir(parent_dir + '\\crash-logs'):
    _os.makedirs(parent_dir + '\\crash-logs')
if not _os.path.isdir(parent_dir + '\\logs'):
    _os.makedirs(parent_dir + '\\logs')


def clear():
    _os.system('cls')
def average(l):
    return sum(l) / len(l)
def meter(num, denom, size=50, wrapper=int):
    t = int(num / denom * size)
    return '| ' + ('#' * t) + (' ' * (size-t)) + ' | ' + (str(wrapper(num / denom * 100)) + '%').rjust(4, ' ') + ' | ' + str(num).rjust(len(str(denom)), ' ') + ' / ' + str(denom)

def timestamp(ff=True):
    if ff:
        return _time.strftime('%y-%m-%d %H.%M.%S')
    else:
        return _time.strftime('%y/%m/%d %H:%M:%S')

def dump_lzma(data, ts=None):
    ts = ts or timestamp()
    fn = parent_dir + '\\logs\\' + ts + '-dump.json.lzma'
    f = open(fn, 'wb')
    f.write(_lzma.compress(_json.dumps(data, indent=4).encode()))
    f.close()
    return fn

def dump_txt(data, ts=None):
    ts = ts or timestamp()
    fn = parent_dir + '\\logs\\' + ts + '-report.txt'
    f = open(fn, 'w')
    f.write(data)
    f.close()
    return fn

def dump_csv(data, ts=None):
    ts = ts or timestamp()
    fn = parent_dir + '\\logs\\' + ts + '-scan.csv'
    f = open(fn, 'w')
    f.write(data)
    f.close()
    return fn

##############################################################################################################################


def algorithm_default(seed):
    modifiers = list(str(int(seed))) 
    OLD = seed
    if seed == 0:
        seed = 1
    if seed - _math.floor(seed) != 0:
        seed = int(seed * _math.pow(10, len(str(seed - _math.floor(seed)))))
    seed = seed + (_math.pi * seed)
    noise = abs(((_math.sin(seed) * 5024 / (seed / 103) + seed/7001074777777)))
    noise2 = abs(seed * 2 - _math.cos(seed) * 607 + seed)
    if noise < noise2:
        n2a = noise2; n1a = noise; noise = n2a; noise2 = n1a
    if seed > 100000000000000:
        seed = seed / ((noise - noise2) / 35)
    else:
        seed = seed * noise2 * noise       
    seed = int(seed-noise2) / _math.sqrt(int(seed+noise2))
    for x in range(0, len(str(int(seed)))):
        seed = seed / (1.31 * (len(str(int(seed)))))
    for x in modifiers:
        if x == '0':
            continue
        seed = seed + (1 / int(x))
    return _math.fmod(abs(_math.fmod(seed * 417.7, 5) / 4.9), 1)

def algorithm_md5(seed):
    h = _hashlib.md5(str(seed).encode())
    h.update(''.join(['acegikmoqz'[int(x)] for x in str(seed) if x in '0123456789']).encode())
    return _math.fmod(int(h.hexdigest(), 16) / 340282366920938463463374607431768211455, 1)

def algorithm_sha256(seed):
    h = _hashlib.sha256(str(seed).encode())
    h.update(''.join(['acegikmoqz'[int(x)] for x in str(seed) if x in '0123456789']).encode())
    return _math.fmod(int(h.hexdigest(), 16) / 115792089237316195423570985008687907853269984665640564039457584007913129639935, 1)

