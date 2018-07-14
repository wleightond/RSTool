from matplotlib import pyplot as plt


def RandomWalkPlot(e):
  ce = list(e)
  n = len(ce)
  X = map(lambda i: 2 * i - 1, ce)
  S = [0]
  s = 0
  for bit in X:
      s += bit
      S.append(s)
  S.append(0)
  plt.plot(S)
  plt.suptitle('Random Excursions: Random Walk Plot')
  plt.xlabel('Bit in Sequence')
  plt.xlim((0, min(n, 100)))  # set view to first 100 bits
  plt.ylabel('Sum')

  plt.show()
