import gvmagic
import graphviz
from gvmagic import *
from pyeda.inter import *

primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
          31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
          73, 79, 83, 89, 97, 101, 103, 107, 109, 113,
          127, 131, 137, 139, 149, 151, 157, 163, 167, 173,
          179, 181, 191, 193, 197, 199, 211, 223, 227, 229,
          233, 239, 241, 251]

isPrime = [False] * 255

linked = {}
# i on the left j

def toBool(n):
    result = [None] * 8
    i = 7;
    while i >= 0:
        result[i] = (n % 2 == 1)
        n = n // 2
        i -= 1

    return result

def something():

    for prime in primes:
        isPrime[prime] = True
        i = 0
        while i + prime < 256:
            try:
                linked[i].append(i + prime)
            except KeyError:
                linked[i] = [i + prime]
            i += 1

    i = 15
    while i < 256:
        try:
            if i - 15 >= 0 and i - 15 not in linked[i]:
                linked[i].append(i - 15)
        except KeyError:
            linked[i] = [i - 15]
        i += 1

    for i in linked.keys():
        toPrint = ""
        if i / 10 < 1:
            toPrint += " "
        if i / 100 < 1:
            toPrint += " "

        toPrint += str(i) + ": "
        for j in linked[i]:
            if j / 10 < 1:
                toPrint += " "

            if j / 100 < 1:
                toPrint += " "

            toPrint += str(j) + ", "

        print(toPrint)

    a, b, c = map(bddvar, 'abc')
    f = a & b | a & c | b & c
    f.to_dot()

if __name__ == '__main__':
    something()