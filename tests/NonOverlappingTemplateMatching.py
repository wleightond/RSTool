# William Leighton Dawson
# Center for Cyber Security
# New York University - Abu Dhabi
# Implementation of the NIST Randomness Test Suite
# 7. The Non-overlapping Template Matching Test

from math import floor
from helpers import LengthError, get_templates, split_list
from cephes import igam as igamc
from sys import stderr

# m = 9 or m = 10 recommended
def NonOverlappingTemplateMatching(e, m=6):
    n = len(e)
    # m = 6  # min 2, max 16, rec 9 or 10
    N = 8  # fixed value as per spec
    M = int(n/float(N))
    ce = list(e)
    ce = ce[:len(ce) - (len(ce) % M)]
    blocks = split_list(ce, M)
    templates = sorted(get_templates(m))
    outstr = "Non-Overlapping Template Matching Test:\n"
    outstr += "n = %d\n" % n
    outstr += "N = %d\n" % N
    outstr += "M = %d\n" % M
    outstr += "%d templates to iterate over:\n" % len(templates)
    p_l = []
    first = True
    for B in templates:
        W = map(int, xrange(N))
        for j in xrange(N):
            block = blocks[j]
            hits = 0
            idx = 0
            while idx < M - m:
                if block[idx:idx+m] == B:
                    hits += 1
                    increment = m
                else:
                    increment = 1
                idx += increment
                if block[idx:idx+m] == []:
                    raise LengthError()
            W[j] = hits
        mu = float(M - m + 1) / pow(2, m)
        sigma2 = M * (1.0 / pow(2, m) - float(2 * m - 1) / pow(2, (2 * m)))
        pre_Chi2_l = map(lambda j: pow((W[j] - mu), 2) / sigma2, xrange(N))
        Chi2_obs = sum(pre_Chi2_l)
        p = igamc(N / 2.0, Chi2_obs / 2.0)
        if not first:
            outstr += '\n----------------'
        else:
            first = False
        outstr += "\nB = %s\n" % ''.join(map(str, B))
        outstr += "mu = %.6f\n" % mu
        outstr += "sigma2 = %.6f\n" % sigma2
        outstr += "Chi2_obs = %.6f\n" % Chi2_obs
        outstr += "W = %s\n" % W
        outstr += "P-value = %.6f\n" % p
        p_l.append(p)
    open("./test_results/NonOverlappingTemplateMatching.txt", "w").write(outstr)
    for j in xrange(len(p_l)):
        p = p_l[j]
        if p < 0.01:
            return False
    return True


# Given: M > 0.01 n
# Given: N = _n/M_
# n - M < 8 M
# 8 M <= n < 9 M
# M <= n/8 < 9/8 M
# Rough Conclusion: M = _n/8_
