# William Leighton Dawson
# Center for Cyber Security
# New York University - Abu Dhabi
# Implementation of the NIST Randomness Test Suite
# 8. The Overlapping Template Matching Test

from sys import stderr, stdout as s
from helpers import LengthError, get_templates, reprint, split_list
from cephes import igam as igamc


def OverlappingTemplateMatching(e, m=6):
    n = len(e)
    # m = 6  # min 2, max 16, rec 9 or 10
    N = 968  # fixed value as per spec
    M = 1032  # fixed, but could be: int(n/float(N))
    outstr = "Overlapping Template Matching Test:\n"
    outstr += "n = %d\n" % n
    outstr += "N = %d\n" % N
    outstr += "M = %d\n" % M
    run_test = True
    if n < 1000000:
        run_test = False
    else:
        ce = list(e)
        ce = ce[:len(ce) - (len(ce) % M)]
        blocks = split_list(ce, M)
        templates = sorted(get_templates(m))[::-1]
        pi = [0.364091, 0.185659, 0.139381, 0.100571, 0.070432, 0.139865]
        p_lambda = (M - m + 1.0) / pow(2, m)
        p_eta = p_lambda / 2.0
        p_l = []
        first = True
        prevlen = 0
        for tidx in xrange(len(templates)):
            B = templates[tidx]
            v = [0, 0, 0, 0, 0, 0]  # given B
            for j in xrange(N):
                block = blocks[j]
                hits = 0
                idx = 0
                while idx < M - m:
                    if block[idx:idx+m] == B:
                        hits += 1
                    idx += 1
                    if block[idx:idx+m] == []:
                        raise LengthError()
                if hits <= 5:
                    v[hits] += 1
                else:
                    v[5] += 1
            pre_Chi2_l = []
            for i in xrange(6):
                pre_Chi2_l.append(pow((v[i] - N * pi[i]), 2) / (N * pi[i]))
            Chi2_obs = sum(pre_Chi2_l)
            p = igamc(5 / 2.0, Chi2_obs / 2.0)
            p_l.append(p)
            if not first:
                outstr += '\n----------------'
            if first:
                outstr += "lambda = %d\n" % p_lambda
                outstr += "%d templates to iterate over:\n" % len(templates)
                first = False
            outstr += "\nB = %s\n" % ''.join([str(i) for i in B])
            outstr += "v = %s\n" % v
            outstr += "Chi2_obs = %.6f\n" % Chi2_obs
            outstr += "P-value = %.6f\n" % p
    if not run_test:
        outstr += 'Test not run: pre-test condition not met: '
        outstr += 'n >= 1000000\n'
    open("./test_results/OverlappingTemplateMatching.txt", "w").write(outstr)
    if run_test:
        for p in p_l:
            if p < 0.01:
                return False
    return True
