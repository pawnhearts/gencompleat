import os, re, builtins
from operator import attrgetter, itemgetter
from pprint import pprint
import fire
from functools import partial


def run(cmd):
    return os.popen(cmd).read().splitlines()

def runt(cmd):
    return os.popen(cmd).read()

def rpartial(func, *fargs):
    def wrapper(*args, **kwargs):
        return func(*args, *fargs, **kwargs)

    return wrapper

def map(func, lst):
    return list(builtins.map(func, lst))

def filter(func, lst):
    return list(builtins.filter(func, lst))

def startswith(lst, *sl):
    return [l for l in lst if any(l.startswith(s) for s in sl)]

def notstartswith(lst, *sl):
    return [l for l in lst if not any(l.startswith(s) for s in sl)]

def contains(lst, s):
    return filter(rpartial(str.__contains__, s), lst)

def split(lst, by=None, index=None):
    lst = map(rpartial(str.split, by), lst)
    if index is not None:
        lst = map(itemgetter(index), lst)
    return lst

def sub(lst, pattern, repl):
    return map(lambda s: re.sub(pattern, repl, s), lst)

def strip(lst):
    return map(str.strip, lst)


def main(cmd, help="-h", indent='  '):
    cmdhelp = run(f"{cmd} {help}")
    commands = notstartswith(split(startswith(cmdhelp, indent), index=0), '<', '-', cmd)
    commands = {c: sub(sub(map(itemgetter(0),  re.findall(r'(\-+\w+(\s<[\w\.]+>)?)', runt(f'{cmd} {help} {c}'))), r'\s([A-Z]+)\b', r' <\1>'), r'<\.\.\.>', '<ARG>') for c in commands}
    commands = {c: [max(argvals, key=len) for argvals in {a.split()[0]: startswith(args, f'{a.split()[0]}') for a in args}.values()] for c, args in commands.items()}

    # commands = {c: startswith(sub(sub(strip(run(f'{cmd} {help} {c} 2>/dev/null')), r'\s([A-Z]+)\b', r' <\1>'), r'(\s+\w.*)', r''), '-', '[-') for c in commands}
    ctext = '\n  |  '.join('%s (%s)' % (c, (' | '.join(args))) for c, args in commands.items())
    print(f'{cmd} (\n{  ctext}\b)')




if __name__ == "__main__":
    fire.Fire(main)
