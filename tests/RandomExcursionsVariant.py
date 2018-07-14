# William Leighton Dawson
# Center for Cyber Security
# New York University - Abu Dhabi
# Implementation of the NIST Randomness Test Suite
# 14. Random Excursions Test

from helpers import LengthError, pi_k
from cephes import igam as igamc
from math import erfc, sqrt
from sys import stderr


def RandomExcursionsVariant(e):
    ce = list(e)
    n = len(ce)
    X = map(lambda i: 2 * i - 1, ce)
    S = [0]
    s = 0
    for bit in X:
        s += bit
        S.append(s)
    S.append(0)
    J = -1
    for step in xrange(1, len(S)):
        if S[step] == 0:
            J += 1
    run_test = True
    outstr = 'Random Excursions Variant Test:\n'
    outstr += 'n = %d\n' % n
    outstr += 'J = %d\n' % J
    if J < 500:
        run_test = False
    else:
        states = {}
        for state in range(-9, 0) + range(1, 10):
            states[state] = {'count': 0, 'p': 0}  # initialise states
        for bit in S:
            if bit and -10 < bit < 10:
                states[bit]['count'] += 1
        for x in states:
            count = states[x]['count']
            p = erfc(abs(count - J) / sqrt(2 * J * (4 * abs(x) - 2)))
            states[x]['p'] = p        
        outstr += 'State=x\tCount\tP-value\tConclusion'
        c = ['Random', 'Non-random']
        for x in range(-9, 0) + range(1, 10):
            count = states[x]['count']
            p = states[x]['p']
            outstr += '\n%d\t%d\t%.6f\t%s\n' % (
                    x, count, p, c[p < 0.01])
    if not run_test:
        outstr += 'Test not run: pre-test condition not met: '
        outstr += 'J >= 500\n'
    open("./test_results/RandomExcursionsVariant.txt", "w").write(outstr)
    if run_test:
        for x in states:
            if states[x]['p'] < 0.01:
                return False
    return True
