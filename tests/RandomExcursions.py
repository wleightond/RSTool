# William Leighton Dawson
# Center for Cyber Security
# New York University - Abu Dhabi
# Implementation of the NIST Randomness Test Suite
# 14. Random Excursions Test

from helpers import LengthError, pi_k
from cephes import igam as igamc
from sys import stderr


def RandomExcursions(e):
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
    idx = 0
    cycles = []
    for step in xrange(1, len(S)):
        if S[step] == 0:
            J += 1
            cycles.append(S[idx:step + 1])
            idx = step
    run_test = True
    outstr = 'Random Excursions Test:\n' # potential BUG
    outstr += 'n = %d\n' % n
    outstr += 'J = %d\n' % J
    if J < 500 :
        run_test = False
    else:
        states = {}
        for state in range(-4, 0) + range(1, 5):
            states[state] = map(lambda x: 0, cycles)  # initialise states
        for idx in xrange(len(cycles)):
            for jdx in cycles[idx]:
                if jdx and -5 < jdx < 5:
                    states[jdx][idx] += 1
        v_k = {}
        for state in range(-4, 0) + range(1, 5):
            v_k[state] = [0*i for i in range(6)]  # initialise v_k
        for idx in xrange(len(cycles)):
            for state in range(-4, 0) + range(1, 5):
                v_k[state][min(states[state][idx], 5)] += 1
        out = {}
        for state in range(-4, 0) + range(1, 5):
            out[state] = {'chi2': 0, 'p': 0}
        for state in out:
            # chi2_obs = 0
            for k in range(6):  # BUG wrong chi2 for state in -3..-1
                term = pow(v_k[state][k] - J * pi_k[abs(state)][k], 2)
                term /= J * pi_k[abs(state)][k]
                out[state]['chi2'] += term
            out[state]['p'] = 1 - igamc(5 / 2.0, out[state]['chi2'] / 2.0)
        outstr += 'State=x\tchi2\tP-value\tConclusion'
        c = ['Random', 'Non-random']
        for state in sorted(out.keys()):
            chi2 = out[state]['chi2']
            p = out[state]['p']
            outstr += '\n%d\t%.6f\t%.6f\t%s\n' % (
                    state, chi2, p, c[p < 0.01])
    if not run_test:
        outstr += 'Test not run: pre-test condition not met: '
        outstr += 'J >= 500\n'
    open("./test_results/RandomExcursions.txt", "w").write(outstr)
    if run_test:
        for x in states:
            if out[x]['p'] < 0.01:
                return False
    return True
