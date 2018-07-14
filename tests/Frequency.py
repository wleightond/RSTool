# William Leighton Dawson
# Center for Cyber Security
# New York University - Abu Dhabi
# Implementation of the NIST Randomness Test Suite
# 1. The Frequency (Monobit) Test

from helpers import s_n, s_obs
from math import sqrt, erfc


def Frequency(e):
    n = len(e)
    # if n < 100 and not ignore_recommendations:
    #     raise LengthError()
    S_n = s_n(e)
    S_obs = s_obs(e)
    p = erfc(S_obs / sqrt(2))
    outstr = "Frequency (Monobit) Test:\n"
    outstr += "n = %d\n" % n
    outstr += "S_n = %d\n" % S_n
    outstr += "S_obs = %.6f\n" % S_obs
    outstr += "P-value = %.6f\n" % p
    open("./test_results/Frequency.txt", "w").write(outstr)
    if p < 0.01:
        return False
    else:
        return True
