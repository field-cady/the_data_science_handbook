
def fib(n):
  if n < 0: raise Exception
  elif n in [0, 1]: return 1
  else: return n*fib(n-1)
