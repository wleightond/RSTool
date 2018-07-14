# William Leighton Dawson
# Center for Cyber Security
# New York University - Abu Dhabi
# Implementation of the NIST Randomness Test Suite

from math import sqrt, erfc, pi
from cmath import exp as cexp
from numpy.fft import fft
from numpy import array
from sys import stdout, stderr
from random import randint, randrange
from fractions import gcd
#         func_name                         (test_name,                         nargs, {arg1:arg1defaultval, ...}),
func_data = {"Frequency":                   ("Frequency",                           0, {}),
          "BlockFrequency":                 ("Block Frequency",                     0, {'M':"max(20, floor(0.01 * len(e)))"}),
                                                                                           # M>=20 , M>.01n
          "Runs":                           ("Runs",                                0, {}),
          "LongestRunOfOnes":               ("Longest Run Of Ones",                 0, {}),
          "Rank":                           ("Rank",                                0, {}),
          "DiscreteFourierTransform":       ("Discrete Fourier Transform",          0, {}),
          "NonOverlappingTemplateMatching": ("Non-Overlapping Template Matching",   0, {'m':"9"}),
                                                                                           # min 2 max 16, rec 9 or 10 
          "OverlappingTemplateMatching":    ("Overlapping Template Matching",       0, {'m':"9"}),
                                                                                           # min 2 max 16, rec 9 or 10
          "Universal":                      ("Universal",                           0, {}),
          "LinearComplexity":               ("Linear Complexity",                   0, {}),
          "Serial":                         ("Serial",                              0, {}),
          "ApproximateEntropy":             ("Approximate Entropy",                 0, {}),
          "CumulativeSums":                 ("Cumulative Sums",                     0, {}),
          "RandomExcursions":               ("Random Excursions",                   0, {}),
          "RandomExcursionsVariant":        ("Random Excursions Variant",           0, {})
              }


class LengthError(Exception):
    def __init__(self, value='No reason specified'):
        self.value = value

    def __str__(self):
        try:
            return str(self.value)
        except Exception:
            return repr(self.value)


# Pad binary string to desired length
def binpad(inp, length):
    if type(inp) != str:
        raise TypeError()
    if len(inp) <= length:
        return inp
    diff = length - len(inp)
    return "0" * diff + inp


# Read in data and returns list of ints
def read_data(infile):
    with open(infile, 'r') as f:
        datastr = f.read()
    stripped_datastr = datastr.strip().replace("\n", "").replace(" ", "")
    asc = True
    for i in range(48) + range(50, 256):  # check for other than '0' and '1'
        if chr(i) in stripped_datastr:
            asc = False
    if asc:
        datalist = map(int, list(stripped_datastr))
    else:
        cds = map(ord, datastr)
        datalist = []
        for i in xrange(len(cds)):
            byte = binpad(bin(cds[i])[2:], 8)
            bit_l = map(int, byte)
            for bit in bit_l:
                datalist.append(bit)
    return datalist


def get_templates(templen):
    if templen not in range(2, 17):
        raise LengthError('Only templates s.t. 1 < len < 17')
    filename = './templates/template%d' % templen
    templates = []
    with open(filename, 'r') as fo:
        data = fo.read().split('\n')
        for line in data:
            if line:
                templates.append(map(int, line))
    return templates


def split_list(e, m, func=None):
    ce = list(e)
    if not func:
        func = lambda x: x
    out = [func(ce[m*i:m*(i+1)]) for i in xrange(len(ce)/m)]
    return out


def reprint(outstr, prevlen, where=stdout):
    where.write('\b'*prevlen)
    where.write(outstr)
    where.flush()


# 1. Frequency (Monobit) Test
# S_n needed for the test statistic S_obs
def s_n(e):
    ce = list(e)
    for i in xrange(len(ce)):
        if ce[i] == 0:
            ce[i] = -1
    return sum(ce)


# Test statistic S_obs
def s_obs(e):
    S_n = s_n(e)
    n = len(e)
    S_obs = abs(S_n) / sqrt(n)
    return S_obs


# 2. Frequency Test within a Block
# Proportion (pi) of ones within input
def proportion(l):
    return sum(l) / float(len(l))


# 3. Runs Test
# Compute list of run lengths
def run_count(e):
    s = []
    s.append(1)
    for i in xrange(1, len(e)):
        if e[i] == e[i - 1]:
            s[-1] += 1
        else:
            s.append(1)
    return s


# 4. Test for Longest Run of Ones in a Block
# Find longest run in a given block
def longest_run(b):
    cb = list(b)
    if 1 not in cb:
        return 0
    longest = 1  # there's at least one bit
    current = 1
    for i in xrange(1, len(cb)):
        if cb[i]:
            if cb[i - 1] == cb[i]:
                current += 1
            else:
                current = 1
            if current > longest:
                longest = current
        else:
            current = 0
    return longest


# pi_i values. Key is (K,M)
pi_i = {
    (3, 8): {
        1: 0.2148,
        2: 0.3672,
        3: 0.2305,
        4: 0.1875
    },
    (5, 128): {
        4: 0.1174,
        5: 0.2430,
        6: 0.2493,
        7: 0.1752,
        8: 0.1027,
        9: 0.1124
    },
    (6, 10000): {
        10: 0.0882,
        11: 0.2092,
        12: 0.2483,
        13: 0.1933,
        14: 0.1208,
        15: 0.0675,
        16: 0.0727
    }
}


# 5. Binary Matrix Rank Test
# list -> 2d-matrix (sidelength s)
def make_matrix(e, s):
    if len(e) != pow(s, 2):
        raise LengthError()
    ce = [[0 for row in xrange(s)] for col in xrange(s)]
    for row in xrange(s):
        for col in xrange(s):
            ce[row][col] = e[s * row + col]
    return ce


# swap rows i and k in matrix e
def row_swap(e, i, k):
    tmp = list(e[i])
    e[i] = list(e[k])
    e[k] = list(tmp)


# Forward Row Operations
def forward_row_ops(e):
    m = len(e)
    for i in xrange(0, m-1):
        if e[i][i] == 0:
            k_found = -1
            for k in xrange(i + 1, m):
                if e[k][i] == 1:
                    k_found = k
                    break
            if k_found != -1:
                row_swap(e, i, k)
        if e[i][i] == 1:
            for row in xrange(i + 1, m):
                if e[row][i] == 1:
                    for col in xrange(i, m):
                        e[row][col] = e[row][col] ^ e[i][col]


# Backward Row Operations
def backward_row_ops(e):
    m = len(e)
    for i in xrange(m - 1, -1, -1):
        if e[i][i] == 0:
            k_found = -1
            for k in xrange(i - 1, -1, -1):
                if e[k][i] == 1:
                    k_found = k
                    break
            if k_found != -1:
                row_swap(e, i, k)
        if e[i][i] == 1:
            for row in xrange(i - 1, -1, -1):
                if e[row][i] == 1:
                    for col in xrange(i, 0, -1):
                        e[row][col] = e[row][col] ^ e[i][col]


# 6. Discrete Fourier Transform (Spectral) Test
# Return list of primes < N
def primes_below(N):
    '''From: stackoverflow.com/questions/2068372/
    Input N>=6, Returns a list of primes, 2 <= p < N'''
    correction = N % 6 > 1
    N = {0: N, 1: N - 1, 2: N + 4, 3: N + 3, 4: N + 2, 5: N + 1}[N % 6]
    sieve = [True] * (N // 3)
    sieve[0] = False

    def ls(i):
        return (3 * i + 1) | 1
    for i in range(int(N ** .5) // 3 + 1):
        if sieve[i]:
            k = ls(i)
            s = k * k // 3
            coeff = ((N//6 - (k*k)//6 - 1)//k + 1)
            sieve[s::2*k] = [False] * coeff
            s = (k * k + 4 * k - 2 * k * (i % 2)) // 3
            coeff = N // 6 - (k * k + 4 * k - 2 * k * (i % 2)) // 6 - 1
            coeff //= k
            coeff += 1
            sieve[s::2 * k] = [False] * coeff
    return [2, 3] + [ls(i) for i in range(1, N//3 - correction) if sieve[i]]


# Test deterministically up to 1000^2, then use Miller-Rabin (MR)
def isprime(n, smallprimeset, _smallprimeset, precision=7):
    '''From: http://en.wikipedia.org/wiki/Miller-Rabin_primality_test'''
    if n < 1:
        raise ValueError("Out of bounds, first argument must be > 0")
    elif n <= 3:
        return n >= 2
    elif n % 2 == 0:
        return False
    elif n < _smallprimeset:
        return n in smallprimeset
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for repeat in xrange(precision):
        a = randrange(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for r in xrange(s - 1):
            x = pow(x, 2, n)
            if x == 1:
                return False
            if x == n - 1:
                break
        else:
            return False
    return True


# Pollard-Rho-Brent (PB) factorization algorithm
def pollard_brent(n):
    '''From: comeoncodeon.wordpress.com/2010/09/18/'''
    if n % 2 == 0:
        return 2
    if n % 3 == 0:
        return 3
    y = randint(1, n-1)
    c = randint(1, n-1)
    m = randint(1, n-1)
    g, r, q = 1, 1, 1
    while g == 1:
        x = y
        for i in range(r):
            y = (pow(y, 2, n) + c) % n
        k = 0
        while k < r and g == 1:
            ys = y
            for i in range(min(m, r - k)):
                y = (pow(y, 2, n) + c) % n
                q = q * abs(x - y) % n
            g = gcd(q, n)
            k += m
        r *= 2
    if g == n:
        while True:
            ys = (pow(ys, 2, n) + c) % n
            g = gcd(abs(x - ys), n)
            if g > 1:
                break
    return g


# Factorize n and return a list of its prime factors
def prime_factors(n, sorting=True, setting=True):
    smallprimes = primes_below(1000)
    smallprimeset = set(primes_below(100000))
    _smallprimeset = 100000
    factors = []
    for checker in smallprimes:
        while n % checker == 0:
            factors.append(checker)
            n //= checker
        if checker > n:
            break
    if n < 2:
        return factors
    while n > 1:
        if isprime(n, smallprimeset, _smallprimeset):
            factors.append(n)
            break
        # trial division did not fully factor, switch to pollard-brent
        factor = pollard_brent(n)
        # recurse to factor the not necessarily prime factor returned by PB
        factors.extend(prime_factors(factor))
        n //= factor
    if sorting:
        factors.sort()
    if setting:
        factors = set(factors)
    return factors


# Discrete Fourier Transform (DFT)
def compute_dft_complex(e):
    X = map(lambda i: [-1, 1][i], list(e))
    S = fft(X)
    return S


# Modulus of DFT
def modulus(S):
    M = map(abs, S[:len(S)//2])
    return M


# 9. Maurer's "Universal Statistical" Test
# Relevant values
#              L: [minn,   expectedValue, variance]
universal_l = {2:  [0,          1.5374383, 1.157],
               6:  [387840,     5.2177052, 2.954],
               7:  [904960,     6.1962507, 3.125],
               8:  [2069480,    7.1836656, 3.238],
               9:  [4654080,    8.1764248, 3.311],
               10: [10342400,   9.1723243, 3.356],
               11: [22753280,   10.170032, 3.384],
               12: [49643520,   11.168765, 3.401],
               13: [107560960,  11.68070,  3.410],
               14: [231669760,  13.167693, 3.416],
               15: [496435200,  14.167488, 3.419],
               16: [1059061760, 15.167379, 3.421]}


# Determine L, Q, expectedValue, and variance
def find_LQ(n):
    found = False
    i = 0
    for i in xrange(6, 16 + 1):
        if n >= universal_l[i][0]:
            L = i
            found = True
    if not found:
        L = 2
        Q = 4
    else:
        Q = 10 * pow(2, L)
    expectedValue = universal_l[L][1]
    variance = universal_l[L][2]
    return L, Q, expectedValue, variance


def bin_strings(n):
    out = []
    for i in range(1 << n):
        s = bin(i)[2:]
        s = '0' * (n - len(s)) + s
        out.append(tuple(map(int, list(s))))
    return out


# 14. Random Excursions Test
    # pi_k = [[0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000],
    #         [0.5000, 0.2500, 0.1250, 0.0625, 0.0312, 0.0312],
    #         [0.7500, 0.0625, 0.0469, 0.0352, 0.0264, 0.0791],
    #         [0.8333, 0.0278, 0.0231, 0.0193, 0.0161, 0.0804],
    #         [0.8750, 0.0156, 0.0137, 0.0120, 0.0105, 0.0733],
    #         [0.9000, 0.0100, 0.0090, 0.0081, 0.0073, 0.0656],
    #         [0.9167, 0.0069, 0.0064, 0.0058, 0.0053, 0.0588],
    #         [0.9286, 0.0051, 0.0047, 0.0044, 0.0041, 0.0531]
    # ]

# Values from C test code
pi_k = [
  [0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000],
  [0.5000, 0.2500, 0.1250, 0.0625, 0.03125, 0.03125],
  [0.7500, 0.0625, 0.046875, 0.03515625, 0.0263671875, 0.0791015625],
  [0.8333333333, 0.02777777778, 0.02314814815,
   0.01929012346, 0.01607510288, 0.0803755143],
  [0.8750, 0.015625, 0.013671875, 0.01196289063, 0.0104675293, 0.0732727051],
  [0.9000, 0.0100, 0.0090, 0.0081, 0.0073, 0.0656],
  [0.9167, 0.0069, 0.0064, 0.0058, 0.0053, 0.0588],
  [0.9286, 0.0051, 0.0047, 0.0044, 0.0041, 0.0531]
]
