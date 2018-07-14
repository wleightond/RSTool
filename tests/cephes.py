import math

rel_error = 1E-12

MACHEP = 1.11022302462515654042E-16    # 2**-53
MAXLOG = 7.09782712893383996732224E2  # log(MAXNUM)
MAXNUM = 1.7976931348623158E308      # 2**1024*(1-MACHEP)
PI     = 3.14159265358979323846      # pi, duh!

big = 4.503599627370496e15
biginv =  2.22044604925031308085e-16

sgngam = 0


def polevl(x, coef, N):
  j = 0
  p = coef[j]
  ans = p
  j += 1
  p = coef[j]
  i = N - 1
  while i > 0:
    i -= 1
    ans = ans * x + p
    j += 1
    p = coef[j]
  return ans


def p1evl(x, coef, N):
  j = 0
  p = coef[j]
  ans = x + p
  j += 1
  p = coef[j]
  i = N - 1 - 1
  while i:
    i -= 1
    ans = ans * x + p
    j += 1
    p = coef[j]
  return ans


def normal(x):
  sqrt2 = 1.414213562373095048801688724209698078569672
  if x > 0:
    arg = x / sqrt2
    result = 0.5 * (1 + math.erf(arg))
  else:
    arg = -x / sqrt2
    result = 0.5 * (1 - math.erf(arg))
  return result


def erf(x):
  two_sqrtpi = 1.128379167095512574
  x_sum = x
  term = x
  xsqr = x * x
  j = 1
  if math.fabs(x) > 2.2:
    return 1.0 - erfc(x)
  term *= xsqr / j
  x_sum -= term / (2 * j + 1)
  j += 1
  term *= xsqr / j
  x_sum += term/(2 * j + 1)
  j += 1
  while math.fabs(term) / x_sum > rel_error:
    term *= xsqr / j
    x_sum -= term/(2 * j + 1)
    j += 1
    term *= xsqr / j
    x_sum += term/(2 * j + 1)
    j += 1
  return two_sqrtpi * x_sum


def erfc(x):
  one_sqrtpi = 0.564189583547756287
  a = 1
  b = x
  c = x
  d = x * x + 0.5
  q2 = b / d
  n = 1.0
  if math.fabs(x) < 2.2:
    return 1.0 - erf(x)
  if x < 0:
    return 2.0 - erfc(-x)
  t = a * n + b * x
  a = b
  b = t
  t = c * n + d * x
  c = d
  d = t
  n += 0.5
  q1 = q2
  q2 = b / d
  while math.fabs(q1 - q2) / q2 > rel_error:
    t = a * n + b * x
    a = b
    b = t
    t = c * n + d * x
    c = d
    d = t
    n += 0.5
    q1 = q2
    q2 = b / d
  return one_sqrtpi * math.exp(-x * x) * q2


def igamc(a, x):
  if (x <= 0) or ( a <= 0):
    return 1.0
  if (x < 1.0) or (x < a):
    return 1.0 - igam(a,x)
  ax = a * math.log(x) - x - lgam(a)
  if ax < -MAXLOG:
    # print "igamc: UNDERFLOW\n"
    return 0.0
  ax = math.exp(ax)
  # continued fraction
  y = 1.0 - a
  z = x + y + 1.0
  c = 0.0
  pkm2 = 1.0
  qkm2 = x
  pkm1 = x + 1.0
  qkm1 = z * x
  ans = pkm1 / qkm1
  c += 1.0
  y += 1.0
  z += 2.0
  yc = y * c
  pk = pkm1 * z  -  pkm2 * yc
  qk = qkm1 * z  -  qkm2 * yc
  if qk != 0:
    r = pk / qk
    t = math.fabs((ans - r) / r)
    ans = r
  else:
    t = 1.0
  pkm2 = pkm1
  pkm1 = pk
  qkm2 = qkm1
  qkm1 = qk
  if math.fabs(pk) > big:
    pkm2 *= biginv
    pkm1 *= biginv
    qkm2 *= biginv
    qkm1 *= biginv
  while t > MACHEP:
    c += 1.0
    y += 1.0
    z += 2.0
    yc = y * c
    pk = pkm1 * z  -  pkm2 * yc
    qk = qkm1 * z  -  qkm2 * yc
    if qk != 0:
      r = pk / qk
      t = math.fabs((ans - r) / r)
      ans = r
    else:
      t = 1.0
    pkm2 = pkm1
    pkm1 = pk
    qkm2 = qkm1
    qkm1 = qk
    if math.fabs(pk) > big:
      pkm2 *= biginv
      pkm1 *= biginv
      qkm2 *= biginv
      qkm1 *= biginv
  return ans * ax


def igam(a, x):
  if (x <= 0) or (a <= 0):
    return 0.0
  if (x > 1.0) and (x > a):
    return 1.0 - igamc(a,x)
  # Compute  x**a * exp(-x) / gamma(a)
  ax = a * math.log(x) - x - lgam(a)
  if ax < -MAXLOG:
    # print "igam: UNDERFLOW\n"
    return 0.0
  ax = math.exp(ax)
  # power series
  r = a
  c = 1.0
  ans = 1.0
  r += 1.0
  c *= x / r
  ans += c
  while c / ans > MACHEP:
    r += 1.0
    c *= x / r
    ans += c
  return ans * ax / a



# A[]: Stirling's formula expansion of log gamma
# B[], C[]: log gamma function between 2 and 3
#
A = [
  0x6661,0x2733,0x9850,0x3f4a,
  0xe943,0xb580,0x7fbd,0xbf43,
  0x5ebb,0x20dc,0x019f,0x3f4a,
  0xa5a1,0x16b0,0xc16c,0xbf66,
  0x554b,0x5555,0x5555,0x3fb5
]
B = [
  0x6761,0x8ff3,0x8901,0xc095,
  0xb93e,0x355b,0xf234,0xc0e2,
  0x89e5,0xf890,0x3d73,0xc114,
  0xdb51,0xf994,0xbc82,0xc131,
  0xf20b,0x0219,0x4589,0xc13a,
  0x055e,0x5418,0x0c67,0xc12a
]
C = [
  #0x0000,0x0000,0x0000,0x3ff0,
  0x12b2,0x1cf3,0xfd0d,0xc075,
  0xd757,0x7b89,0xaa0d,0xc0d0,
  0x4c9b,0xb974,0xeb84,0xc10a,
  0x0043,0x7195,0x6286,0xc131,
  0xf34c,0x892f,0x5255,0xc143,
  0xe14a,0x6a11,0xce4b,0xc13e
]

MAXLGM  = 2.556348e305


# Logarithm of gamma function 
def lgam(x):
  sgngam = 1

  if x < -34.0:
    q = -x
    w = lgam(q) # note this modifies sgngam!
    p = math.floor(q)
    if p == q:
      # print "lgam: OVERFLOW\n"
      return sgngam * MAXNUM
    i = int(p)
    if (i & 1) == 0:
      sgngam = -1
    else:
      sgngam = 1
    z = q - p
    if z > 0.5:
      p += 1.0
      z = p - q
    z = q * math.sin(PI * z)
    if z == 0.0:
      # print "lgam: OVERFLOW\n"
      return sgngam * MAXNUM
    #      z = log(PI) - log( z ) - w
    z = math.log(PI) - math.log(z) - w
    return z
  if x < 13.0:
    z = 1.0
    p = 0.0
    u = x
    while  u >= 3.0:
      p -= 1.0
      u = x + p
      z *= u
    while  u < 2.0:
      if u == 0.0:
        # print "lgam: OVERFLOW\n"
        return sgngam * MAXNUM
      z /= u
      p += 1.0
      u = x + p
    if z < 0.0:
      sgngam = -1
      z = -z
    else:
      sgngam = 1
    if u == 2.0:
      return math.log(z)
    p -= 2.0
    x = x + p
    p = x * polevl(x, B, 5) / p1evl(x, C, 6)
    return math.log(z) + p
  if x > MAXLGM:
    # print "lgam: OVERFLOW\n"
    return sgngam * MAXNUM
  q = (x - 0.5) * math.log(x) - x + math.log(math.sqrt(2 * PI))
  if x > 1.0e8:
    return q
  p = 1.0 / (x * x)
  if x >= 1000.0:
    q += ((   7.9365079365079365079365e-4 * p
            - 2.7777777777777777777778e-3) *p
        + 0.0833333333333333333333) / x
  else:
    q += polevl(p, A, 4) / x
  return q
