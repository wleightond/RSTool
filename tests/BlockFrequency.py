# William Leighton Dawson
# Center for Cyber Security
# New York University - Abu Dhabi
# Implementation of the NIST Randomness Test Suite
# 2. Frequency Test within a Block

from helpers import proportion, split_list, LengthError
from cephes import igam
from sys import stderr

def igamc(a, x):
  return 1 - igam(a, x)


def BlockFrequency(e, M=10):
    M = 10
    ce = list(e)
    ce = ce[:len(ce) - (len(ce) % M)]
    n = len(ce)
    N = n / M
    run_test = True
    outstr = "Frequency Test within a Block:\n"
    outstr += "n = %d\n" % n
    outstr += "M = %d\n" % M
    outstr += "N = %d\n" % N
    if n < 100:
        run_test = False
    else:
        Pi_l = split_list(ce, M, proportion)
        Chi2_obs = 4 * M * sum([pow((i - 0.5), 2) for i in Pi_l])
        p = igamc(N / 2.0, Chi2_obs / 2.0)
        outstr = "Frequency Test within a Block:\n"
        outstr += "n = %d\n" % n
        outstr += "M = %d\n" % M
        outstr += "N = %d\n" % N
        outstr += "Chi^2_obs = %.6f\n" % Chi2_obs
        outstr += "P-value = %.6f\n" % p
    if not run_test:
        outstr += 'Test not run: pre-test condition not met: '
        outstr += 'n >= 100\n'
    open("./test_results/BlockFrequency.txt", "w").write(outstr)
    if run_test:
        if p < 0.01:
            return False
    return True
