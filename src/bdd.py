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
    n -= 1
    while i >= 0:
        result[i] = (n % 2 == 1)
        n = n // 2
        i -= 1

    return result

def something():

    x = [None] * 8
    x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7] = map(bddvar, ['x0', 'x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7'])

    y = [None] * 8
    y[0], y[1], y[2], y[3], y[4], y[5], y[6], y[7] = map(bddvar, ['y0', 'y1', 'y2', 'y3', 'y4', 'y5', 'y6', 'y7'])
    
    c = [None] * 8
    c[0], c[1], c[2], c[3], c[4], c[5], c[6], c[7] = map(bddvar, ['c0', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7'])

    for prime in primes:
        isPrime[prime] = True
        i = 1
        while i + prime <= 256:
            try:
                linked[i].append(i + prime)
            except KeyError:
                linked[i] = [i + prime]
            i += 1

    i = 15
    while i <= 256:
        try:
            if i - 15 > 0 and i - 15 not in linked[i]:
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


    bddR = None

    for key in sorted(linked.keys()):
        keyBool = toBool(key)


        curExpression = None

        for link in linked[key]:
            i = 0
            for b in keyBool:
                if b:
                    if curExpression == None:
                        curExpression = x[i]
                    else:
                        curExpression = curExpression & x[i]
                else:
                    if curExpression == None:
                        curExpression = ~x[i]
                    else:
                        curExpression = curExpression & ~x[i]
                i += 1

            i = 0

            for b in toBool(link):
                if b:
                    curExpression = curExpression & y[i]
                else:
                    curExpression = curExpression & ~y[i]
                i += 1


            if(bddR == None):
                bddR = curExpression
            else:
                bddR = bddR | curExpression

            curExpression = None

    print(bddR)

    # bddR0 = bddR.compose({x[0]: x[0+8*0], x[1]: x[1+8*0], x[2]: x[2+8*0], x[3]: x[3+8*0], x[4]: x[4+8*0], x[5]: x[5+8*0], x[6]: x[6+8*0], x[7]: x[7+8*0], y[0]: y[0+8*0], y[1]: y[1+8*0], y[2]: y[2+8*0], y[3]: y[3+8*0], y[4]: y[4+8*0], y[5]: y[5+8*0], y[6]: y[6+8*0], y[7]: y[7+8*0]})
    # bddR1 = bddR.compose({x[0]: x[0+8], x[1]: x[1+8], x[2]: x[2+8], x[3]: x[3+8], x[4]: x[4+8], x[5]: x[5+8], x[6]: x[6+8], x[7]: x[7+8], y[0]: y[0+8], y[1]: y[1+8], y[2]: y[2+8], y[3]: y[3+8], y[4]: y[4+8], y[5]: y[5+8], y[6]: y[6+8], y[7]: y[7+8]})
    # bddR2 = bddR.compose({x[0]: x[0+8*2], x[1]: x[1+8*2], x[2]: x[2+8*2], x[3]: x[3+8*2], x[4]: x[4+8*2], x[5]: x[5+8*2], x[6]: x[6+8*2], x[7]: x[7+8*2], y[0]: y[0+8*2], y[1]: y[1+8*2], y[2]: y[2+8*2], y[3]: y[3+8*2], y[4]: y[4+8*2], y[5]: y[5+8*2], y[6]: y[6+8*2], y[7]: y[7+8*2]})
    # bddR3 = bddR.compose({x[0]: x[0+8*3], x[1]: x[1+8*3], x[2]: x[2+8*3], x[3]: x[3+8*3], x[4]: x[4+8*3], x[5]: x[5+8*3], x[6]: x[6+8*3], x[7]: x[7+8*3], y[0]: y[0+8*3], y[1]: y[1+8*3], y[2]: y[2+8*3], y[3]: y[3+8*3], y[4]: y[4+8*3], y[5]: y[5+8*3], y[6]: y[6+8*3], y[7]: y[7+8*3]})
    # bddR4 = bddR.compose({x[0]: x[0+8*4], x[1]: x[1+8*4], x[2]: x[2+8*4], x[3]: x[3+8*4], x[4]: x[4+8*4], x[5]: x[5+8*4], x[6]: x[6+8*4], x[7]: x[7+8*4], y[0]: y[0+8*4], y[1]: y[1+8*4], y[2]: y[2+8*4], y[3]: y[3+8*4], y[4]: y[4+8*4], y[5]: y[5+8*4], y[6]: y[6+8*4], y[7]: y[7+8*4]})
    # bddR5 = bddR.compose({x[0]: x[0+8*5], x[1]: x[1+8*5], x[2]: x[2+8*5], x[3]: x[3+8*5], x[4]: x[4+8*5], x[5]: x[5+8*5], x[6]: x[6+8*5], x[7]: x[7+8*5], y[0]: y[0+8*5], y[1]: y[1+8*5], y[2]: y[2+8*5], y[3]: y[3+8*5], y[4]: y[4+8*5], y[5]: y[5+8*5], y[6]: y[6+8*5], y[7]: y[7+8*5]})

    i = 0

    bddR6 = bddR

    print("rand", bddR6.restrict({x[0]: 1, x[1]: 1, x[2]: 0, x[3]: 1, x[4]: 1, x[5]: 1, x[6]: 0, x[7]: 1, y[0]: 1, y[1]: 1, y[2]: 0, y[3]: 1, y[4]: 1, y[5]: 1, y[6]: 1, y[7]: 1}))
    print("rand", bddR6.restrict({x[0]: 1, x[1]: 1, x[2]: 0, x[3]: 1, x[4]: 1, x[5]: 1, x[6]: 0, x[7]: 1, y[0]: 1, y[1]: 1, y[2]: 0, y[3]: 0, y[4]: 1, y[5]: 1, y[6]: 1, y[7]: 0}))

    bddR1 = bddR.compose({x[0]: c[0], x[1]: c[1], x[2]: c[2], x[3]: c[3], x[4]: c[4], x[5]: c[5], x[6]: c[6], x[7]: c[7]})



    while i < 7:
        print("Created checker for loop size ", i)
        print("Currently, there are ", bddR6.satisfy_count(), " solutions to the bddr")
        bddR6 = bddR6.compose({y[0]: c[0], y[1]: c[1], y[2]: c[2], y[3]: c[3], y[4]: c[4], y[5]: c[5], y[6]: c[6], y[7]: c[7]})
        bddR6 = bddR6 & bddR1

        bddR6 = bddR6.smoothing(c[0])
        bddR6 = bddR6.smoothing(c[1])
        bddR6 = bddR6.smoothing(c[2])
        bddR6 = bddR6.smoothing(c[3])
        bddR6 = bddR6.smoothing(c[4])
        bddR6 = bddR6.smoothing(c[5])
        bddR6 = bddR6.smoothing(c[6])
        bddR6 = bddR6.smoothing(c[7])
        # bddR6 =
        # print("***", bddR6.restrict({x[0]: 1, x[1]: 1, x[2]: 1, x[3]: 1, x[4]: 1, x[5]: 1, x[6]: 1, x[7]: 1, y[0]: 1, y[1]: 1, y[2]: 1, y[3]: 1, y[4]: 0, y[5]: 1, y[6]: 1, y[7]: 0}))

        i += 1

    all = bddR6.satisfy_all()

    all = list(all)

    r6 = False


    # for result in all:


    print("Finished")

def test():
    f = expr("f1 & f2 | f1 & f3 | f2 & f3")
    print(f)

    f=expr2bdd(f)

    print(f)

if __name__ == '__main__':
    something()
    # test()