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


class MissingDependency(BaseException):
    def __init__(self, package, *args, **kwargs):
        self.package = package
        BaseException.__init__(self, *args, **kwargs)

class Source:
    def __init__(self, packages_required, function):
        self.packages = packages_required
        self.random = function
    def get(self):
        for x in self.packages:
            try:
                globals()[x] = __import__(x)
            except ImportError:
                raise MissingDependency(x, 'missing package "' + x + '"')
        return self.random()



def src_random_mic():
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, output=True, frames_per_buffer=8)
    sd = sum(array.array('h', stream.read(16)).tolist())
    stream.close()
    return abs(sd)

def src_random_py():
    return random.uniform(1, 100)

def src_random_time():
    return int(time.time())

def src_random_urandom():
    return sum([x for x in os.urandom(15)])




random_mic = Source(['pyaudio', 'array'], src_random_mic)
random_py = Source(['random'], src_random_py)
random_time = Source(['time'], src_random_time)
random_urandom = Source(['os'], src_random_urandom)
