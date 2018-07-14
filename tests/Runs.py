# William Leighton Dawson
# Center for Cyber Security
# New York University - Abu Dhabi
# Implementation of the NIST Randomness Test Suite
# 3. The Runs Test

from helpers import proportion, run_count
from math import sqrt, erfc
from sys import stderr


def Runs(e):
    ce = list(e)
    n = len(ce)
    tau = 2.0 / sqrt(n)
    pi_e = proportion(ce)
    run_test = True
    outstr = "Runs Test:\n"
    outstr += "n = %d\n" % n
    outstr += "tau = %.6f\n" % tau
    outstr += "pi = %.6f\n" % pi_e
    if abs(pi_e - 0.5) >= tau:  # runs test n/a
        run_test = False
    else:
        run_list = run_count(ce)
        V_n_obs = len(run_list)
        num = abs(V_n_obs - 2 * n * pi_e * (1 - pi_e))
        den = 2 * sqrt(2 * n) * pi_e * (1 - pi_e)
        p = erfc(num / den)
        outstr += "V_n_obs = %d\n" % V_n_obs
        outstr += "P-value = %.6f\n" % p
    if not run_test:
        outstr += "Test not run: pre-test condition was not met:\n"
        outstr += "|pi - 0.5| < tau\n"
    open("./test_results/Runs.txt", "w").write(outstr)
    if run_test:
        if p < 0.01:
            return False
    return True
